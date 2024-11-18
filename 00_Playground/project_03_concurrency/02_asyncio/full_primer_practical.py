from __future__ import annotations

import asyncio
import datetime
import os
import random
import signal
import string
import uuid

import httpx
from loguru import logger
from pydantic import BaseModel

BASE_IP_ENDPOINT_URL = "http://ip-api.com/json"


class IpMetadata(BaseModel):
    """Model for IP metadata."""

    ip: str
    country: str | None
    country_code: str | None
    region: str | None
    region_name: str | None
    city: str | None
    zip: str | None
    lat: float | None
    lon: float | None
    isp: str | None
    organization: str | None
    autonomous_system: str | None


class IpMetadataOperationsError(Exception):
    """An exception indicating an error with the IP metadata operations."""


async def get_metadata_for_ip(ip: str) -> IpMetadata:
    """Get metadata for a given IP address."""
    link = f"{BASE_IP_ENDPOINT_URL}/{ip}"
    logger.info(f"Getting metadata for IP from API: {ip}")
    async with httpx.AsyncClient() as client:
        response = await client.get(link)
        if response.status_code != httpx.codes.OK:
            logger.error(f"Failed to get metadata for IP: {ip}, status code: {response.status_code}, response: {response.text}")
            msg = f"Failed to get metadata for IP: {ip}, code: {response.status_code}"
            raise IpMetadataOperationsError(msg)
        ip_metadata = response.json()
        if "countryCode" not in ip_metadata:
            logger.error(f"Failed to get metadata for IP: {ip}, response: {ip_metadata}")
            msg = f"Failed to get metadata for IP: {ip}, response: {ip_metadata}"
            raise IpMetadataOperationsError(msg)
        ip_metadata["ip"] = ip_metadata.pop("query")
        ip_metadata["country_code"] = ip_metadata.pop("countryCode")
        ip_metadata["region_name"] = ip_metadata.pop("regionName")
        ip_metadata["organization"] = ip_metadata.pop("org")
        ip_metadata["autonomous_system"] = ip_metadata.pop("as")
        return IpMetadata.model_validate(ip_metadata)


class PubSubMessage:
    """A message object that is sent via Pub/Sub."""

    def __init__(self, instance_name: str, message_id: str) -> None:
        """Initialize a PubSubMessage."""
        self.timestamp: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)
        self.instance_name: str = instance_name
        self.message_id: str = message_id
        self.hostname: str = ".".join(str(random.randint(0, 255)) for _ in range(4))  # noqa: S311
        self.restarted: bool = False
        self.saved: bool = False
        self.acked: bool = False

    def __str__(self) -> str:
        """Return a string representation of the PubSubMessage."""
        return f"PubSubEvent(instance_name={self.instance_name}, message_id={self.message_id})"


async def save(msg: PubSubMessage) -> None:
    """Save the message to a database."""
    # Simulate saving a message to a database by waiting for a random amount of time
    await asyncio.sleep(random.random())  # noqa: S311
    msg.saved = True
    logger.info(f"Saved {msg.hostname} to the database")


async def restart_host(msg: PubSubMessage) -> None:
    """Restart a given host."""
    data = await get_metadata_for_ip(msg.hostname)
    msg.restarted = True
    logger.opt(colors=True).info(
        f"<magenta>[{msg.hostname}] Restarted successfully a server in {data.city} ({data.country})</magenta>",
    )


async def cleanup(msg: PubSubMessage) -> None:
    """Perform cleanup tasks."""
    # Simulate cleanup by waiting for a random amount of time
    await asyncio.sleep(random.random())  # noqa: S311
    msg.acked = True
    logger.success(f"Done. Acked {msg}")


def handle_results(results, msg: PubSubMessage) -> None:
    """Handle the results of the message processing."""
    for result in results:
        if isinstance(result, IpMetadataOperationsError):
            logger.warning(f"[{msg.hostname}][IpMetadataOperationsError] An error occurred: {result}")
        elif isinstance(result, Exception):
            logger.error(f"[{msg.hostname}] An error occurred: {type(result).__name__} - {result}")


async def handle_message(msg: PubSubMessage) -> None:
    """Handle a Pub/Sub message."""
    results = await asyncio.gather(save(msg), restart_host(msg), return_exceptions=True)
    handle_results(results, msg)
    await cleanup(msg)


def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception: {msg}")
    logger.warning("Shutting down...")
    asyncio.create_task(shutdown(loop))


async def publish(queue):
    """Publish messages to a Pub/Sub topic."""
    choices = string.ascii_lowercase + string.digits

    while True:
        msg_id = str(uuid.uuid4())
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"instance-{host_id}"
        msg = PubSubMessage(message_id=msg_id, instance_name=instance_name)
        asyncio.create_task(queue.put(msg))
        logger.info(f"Publishing message {msg}")
        await asyncio.sleep(random.random())


async def consume(queue) -> None:
    """Consume messages from a Pub/Sub topic."""
    while True:
        msg = await queue.get()

        logger.info(f"Consumed {msg}")
        asyncio.create_task(handle_message(msg))


async def shutdown(loop, signal=None) -> None:
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logger.warning(f"Received exit signal {signal.name}...")
    logger.info("Nacking outstanding messages")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("Flushing metrics")
    logger.warning("Closing database connections")
    loop.stop()


def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

    if os.name == "nt":
        logger.debug("Windows platform detected.")
        try:
            loop.create_task(publish(queue))
            loop.create_task(consume(queue))
            loop.run_forever()
        except KeyboardInterrupt:
            loop.run_until_complete(shutdown(loop, signal.SIGINT))
        finally:
            loop.close()
            logger.success("Successfully shutdown the event loop!")
    else:
        logger.debug("Unix platform detected.")
        signals = (signal.SIGTERM, signal.SIGINT)
        for s in signals:
            loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(loop, s)))
        try:
            loop.create_task(publish(queue))
            loop.create_task(consume(queue))
            loop.run_forever()
        finally:
            loop.close()
            logger.success("Successfully shutdown the event loop!")


if __name__ == "__main__":
    main()
