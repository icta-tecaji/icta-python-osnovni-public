from __future__ import annotations

import asyncio
import random
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
        if hostname is None:
            self.hostname = f"{self.instance_name}.example.net"

    def __str__(self) -> str:
        """Return a string representation of the PubSubMessage."""
        return f"PubSubEvent(instance_name={self.instance_name}, message_id={self.message_id}, hostname={self.hostname})"


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


async def consume(queue):
    """Consume messages from a Pub/Sub topic."""
    while True:
        msg = await queue.get()
        if msg is None:
            break

        # process the message
        logger.info(f"Consumed {msg}")
        await asyncio.sleep(random.random())

    logger.success("Done consuming!")


def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(publish(queue))
        # loop.create_task(consume(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logger.warning("Received a keyboard interrupt. Shutting down.")
    finally:
        loop.close()
        logger.success("Successfully shutdown the event loop!")


if __name__ == "__main__":
    main()
