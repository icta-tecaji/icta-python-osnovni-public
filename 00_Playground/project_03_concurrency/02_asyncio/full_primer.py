from __future__ import annotations

import asyncio
import os
import random
import signal
import string
import uuid

from loguru import logger


class PubSubMessage:
    """A message object that is sent via Pub/Sub."""

    def __init__(self, instance_name: str, message_id: str, hostname: str | None = None) -> None:
        """Initialize a PubSubMessage."""
        self.instance_name: str = instance_name
        self.message_id: str = message_id
        self.hostname: str | None = hostname
        self.restarted: bool = False
        self.saved: bool = False
        self.acked: bool = False
        if hostname is None:
            self.hostname = f"{self.instance_name}.example.net"

    def __str__(self) -> str:
        """Return a string representation of the PubSubMessage."""
        return f"PubSubEvent(instance_name={self.instance_name}, message_id={self.message_id})"


class RestartFailedError(Exception):
    """An exception indicating that the host restart failed."""


async def save(msg: PubSubMessage) -> None:
    """Save the message to a database."""
    # Simulate saving a message to a database by waiting for a random amount of time
    await asyncio.sleep(random.random())  # noqa: S311
    if random.randint(1, 20) == 5:
        raise Exception("Could not process message")
    msg.saved = True
    logger.info(f"Saved {msg.hostname} to the database")


async def restart_host(msg: PubSubMessage) -> None:
    """Restart a given host."""
    # Simulate restarting a host by waiting for a random amount of time
    await asyncio.sleep(random.random())  # noqa: S311
    msg.restarted = True
    if random.randint(0, 8) == 5:
        raise RestartFailedError(f"Could not restart {msg.hostname}")
    logger.info(f"Restarted {msg.hostname}")


async def cleanup(msg: PubSubMessage) -> None:
    """Perform cleanup tasks."""
    # Simulate cleanup by waiting for a random amount of time
    await asyncio.sleep(random.random())  # noqa: S311
    msg.acked = True
    logger.success(f"Done. Acked {msg}")


def handle_results(results, msg: PubSubMessage) -> None:
    """Handle the results of the message processing."""
    for result in results:
        if isinstance(result, RestartFailedError):
            logger.error(f"Restart failed for host {msg.hostname}")
        elif isinstance(result, Exception):
            logger.error(f"Handling general error: {result}")


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
