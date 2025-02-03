from __future__ import annotations

import asyncio
import random
import string
import sys
import uuid

from loguru import logger

# Set logger configuration.
logger.remove()
logger_format = "<white>{time:YYYY-MM-DD HH:mm:ss.SSS}</white> | <level>{level: <8}</level> | <level>{message}</level>"
logger.add(sys.stderr, format=logger_format, level="DEBUG")


class PubSubMessage:
    """A message object that is sent via Pub/Sub."""

    def __init__(self, instance_name: str, message_id: str, hostname: str) -> None:
        """Initialize the message object."""
        self.instance_name: str = instance_name
        self.message_id: str = message_id
        self.hostname: str = hostname
        self.restarted: bool = False
        self.saved: bool = False
        self.acked: bool = False

    def __str__(self) -> str:
        """Return a string representation of the PubSubMessage."""
        return f"PubSubEvent(instance_name={self.instance_name}, message_id={self.message_id})"


async def simulate_publish(queue: asyncio.Queue):
    """Simulate a publisher."""
    choices = string.ascii_lowercase + string.digits

    while True:
        msg_id = str(uuid.uuid4())
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"instance-{host_id}"
        message = PubSubMessage(instance_name, msg_id, host_id)
        await queue.put(message)
        logger.info(f"PUBLISHER: Published message {message}")
        await asyncio.sleep(random.random())


async def restart_host(message: PubSubMessage) -> None:
    """Restart a host."""
    await asyncio.sleep(random.random())
    message.restarted = True
    if random.randrange(1, 5) == 2:
        raise ValueError("Virtual machine not found.")
    logger.debug(f"RESTARTED: {message.instance_name}")


async def save(message: PubSubMessage) -> None:
    """Save the message to the database."""
    await asyncio.sleep(random.random())
    message.saved = True
    if random.randrange(1, 21) == 10:
        raise Exception("Could not process the message.")
    logger.debug(f"SAVED: {message.instance_name}")


async def cleanup(message: PubSubMessage) -> None:
    """Cleanup the message."""
    await asyncio.sleep(random.random())
    message.acked = True
    logger.success(f"Messaged {message.instance_name} has been successfully processed.")


def handle_results(results, msg):
    """Handle the results of the tasks."""
    for result in results:
        if isinstance(result, ValueError):
            logger.warning(f"Error restarting {msg.instance_name}: {result}")
        elif isinstance(result, Exception):
            logger.error(f"Error saving {msg.instance_name}: {result}")


async def handle_message(message: PubSubMessage) -> None:
    """Handle a message."""
    results = await asyncio.gather(restart_host(message), save(message), return_exceptions=True)
    handle_results(results, message)
    await cleanup(message)


async def consume(queue: asyncio.Queue):
    """Consume a message."""
    while True:
        message = await queue.get()
        logger.info(f"CONSUMER: Consumed message {message}")
        asyncio.create_task(handle_message(message))


def handle_exception(loop, context):
    """Handle exceptions."""
    msg = context.get("exception", context["message"])
    logger.error(f"Caught exception: {msg}")
    logger.error("Shutting down the event loop.")
    asyncio.create_task(shutdown(loop))


async def shutdown(loop) -> None:
    """Shutdown the event loop."""
    logger.info("Shutting down the event loop...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logger.info(f"Cancelled {len(tasks)} outstanding tasks.")
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.success("Successfully stopped all tasks.")
    loop.stop()


def main():
    """Main entrypoint of the application."""
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

    try:
        loop.create_task(simulate_publish(queue))
        loop.create_task(consume(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Received a keyboard interrupt. Exiting...")
        loop.run_until_complete(shutdown(loop))
    finally:
        loop.close()
        logger.success("Successfully shutdown the event loop.")


if __name__ == "__main__":
    main()
