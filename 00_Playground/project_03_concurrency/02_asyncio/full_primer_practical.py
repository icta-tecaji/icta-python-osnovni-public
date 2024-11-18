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
from sqlalchemy import DateTime, String, insert, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from tenacity import retry, stop_after_attempt, wait_fixed

BASE_IP_ENDPOINT_URL = "http://ip-api.com/json"
engine = create_async_engine("sqlite+aiosqlite:///full_primer.db", echo=False)
async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    """Base class for database models."""


class RestartedHostsModel(Base):
    """Model for IP metadata."""

    __tablename__ = "restarted_hosts"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    instance_name: Mapped[str] = mapped_column(String(), nullable=False)
    message_id: Mapped[str] = mapped_column(String(), nullable=False)
    hostname: Mapped[str] = mapped_column(String(), nullable=False)
    restarted: Mapped[bool] = mapped_column(String(), nullable=False, default=False)
    acked: Mapped[bool] = mapped_column(String(), nullable=False, default=False)
    country: Mapped[str] = mapped_column(String(), nullable=True)
    city: Mapped[str] = mapped_column(String(), nullable=True)
    organization: Mapped[str] = mapped_column(String(), nullable=True)
    autonomous_system: Mapped[str] = mapped_column(String(), nullable=True)


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


@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(1),
    before_sleep=lambda _: logger.warning("Retrying save..."),
)
async def save(msg: PubSubMessage) -> None:
    """Save the message to a database."""
    msg.saved = True
    async with async_session() as session:
        stmt = insert(RestartedHostsModel).values(
            timestamp=msg.timestamp,
            instance_name=msg.instance_name,
            message_id=msg.message_id,
            hostname=msg.hostname,
            restarted=msg.restarted,
            acked=msg.acked,
        )
        await session.execute(stmt)
        await session.commit()
    logger.opt(colors=True).info(
        f"<magenta>[{msg.hostname}] Saved successfully a server event in the database</magenta>",
    )


@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(1),
    before_sleep=lambda _: logger.warning("Retrying update_restart_data..."),
)
async def update_restart_data(msg: PubSubMessage, data: IpMetadata) -> None:
    """Update the restarted data in the database."""
    msg.restarted = True
    async with async_session() as session:
        stmt = (
            update(RestartedHostsModel)
            .where(RestartedHostsModel.message_id == msg.message_id)
            .values(
                restarted=msg.restarted,
                country=data.country,
                city=data.city,
                organization=data.organization,
                autonomous_system=data.autonomous_system,
            )
        )
        await session.execute(stmt)
        await session.commit()


async def restart_host(msg: PubSubMessage) -> IpMetadata:
    """Restart a given host."""
    data = await get_metadata_for_ip(msg.hostname)
    msg.restarted = True
    logger.opt(colors=True).info(
        f"<magenta>[{msg.hostname}] Restarted successfully a server in {data.city} ({data.country})</magenta>",
    )
    return data


@retry(
    stop=stop_after_attempt(10),
    wait=wait_fixed(1),
    before_sleep=lambda _: logger.warning("Retrying acknowledge..."),
)
async def acknowledge(msg: PubSubMessage) -> None:
    """Perform cleanup tasks."""
    msg.acked = True
    async with async_session() as session:
        stmt = update(RestartedHostsModel).where(RestartedHostsModel.message_id == msg.message_id).values(acked=msg.acked)
        await session.execute(stmt)
        await session.commit()
    logger.success(f"Done. Acked {msg}")


def check_results(results, msg: PubSubMessage) -> bool:
    """Handle the results of the message processing."""
    for result in results:
        if isinstance(result, IpMetadataOperationsError):
            logger.warning(f"[{msg.hostname}][IpMetadataOperationsError] An error occurred: {result}")
            return False
        if isinstance(result, Exception):
            logger.error(f"[{msg.hostname}] An error occurred: {type(result).__name__} - {result}")
            return False
    return True


async def handle_message(msg: PubSubMessage) -> None:
    """Handle a Pub/Sub message."""
    results = await asyncio.gather(save(msg), restart_host(msg), return_exceptions=True)
    if check_results(results, msg) and isinstance(results[1], IpMetadata):
        _, restart_hosts_data = results[0], results[1]
        await update_restart_data(msg, restart_hosts_data)
    await acknowledge(msg)


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


async def startup() -> None:
    """Prepare the service for startup."""
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.success("Database tables created successfully!")


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
    await engine.dispose()
    loop.stop()


def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)
    loop.run_until_complete(startup())

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
