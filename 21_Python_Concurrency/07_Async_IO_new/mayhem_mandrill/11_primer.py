"""
Global Exception Handling
"""
import asyncio
import logging
import random
import signal
import string
import uuid

import attr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


@attr.s
class PubSubMessage:
    instance_name = attr.ib()
    message_id = attr.ib(repr=False)
    hostname = attr.ib(repr=False, init=False)
    restarted = attr.ib(repr=False, default=False)
    saved = attr.ib(repr=False, default=False)
    acked = attr.ib(repr=False, default=False)

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.example.net"


async def save(msg):
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())
    msg.saved = True
    logging.info(f"Saved {msg} into database")


async def restart_host(msg):
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())
    msg.restarted = True
    logging.info(f"Restarted {msg.hostname}")


async def publish(queue):
    choices = string.ascii_lowercase + string.digits

    while True:
        msg_id = str(uuid.uuid4())
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"cattle-{host_id}"
        msg = PubSubMessage(message_id=msg_id, instance_name=instance_name)
        # publish an item
        asyncio.create_task(queue.put(msg))
        logging.debug(f"Published message {msg}")
        # simulate randomness of publishing messages
        await asyncio.sleep(random.random())


async def cleanup(msg):
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())
    msg.acked = True
    logging.info(f"Done. Acked {msg}")


# We’re not handling exceptions appropriately. So to deal with this, as advised in
# the asyncio documentation, we should add a global/default exception handler:
def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    logging.error(f"Caught exception: {msg}")
    logging.info("Shutting down...")
    # Our exception handler function must take in two arguments, loop and context
    # (if you want to give it other arguments, use functools.partial). We’re also going
    # to call our shutdown coroutine function because at this point, something serious is
    # going on where we can’t consume messages, and we should probably fail hard.
    asyncio.create_task(shutdown(loop))


async def handle_message(msg):
    await asyncio.gather(save(msg), restart_host(msg))
    await cleanup(msg)


async def consume(queue):
    while True:
        msg = await queue.get()
        # totally realistic exception
        if random.randrange(1, 5) == 3:
            raise Exception(f"Could not consume {msg}")
        logging.info(f"Consumed {msg}")
        asyncio.create_task(handle_message(msg))


# We’re going to update the shutdown coroutine function so that the signal parameter is
# optional. This is to make it clear that we’re shutting down
# from either “within” or from an external signal.
async def shutdown(loop, signal=None):
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logging.info(f"Received exit signal {signal.name}...")
    logging.info("Closing database connections")
    logging.info("Nacking outstanding messages")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    logging.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    logging.info("Flushing metrics")
    loop.stop()


def main():
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    # We then attached handle_exception to the loop, as well as take the
    # opportunity to update the creating of shutdown tasks with the updated function signature:
    loop.set_exception_handler(handle_exception)
    queue = asyncio.Queue()

    try:
        loop.create_task(publish(queue))
        loop.create_task(consume(queue))
        loop.run_forever()
    finally:
        loop.close()
        logging.info("Successfully shutdown the Mayhem service.")


if __name__ == "__main__":
    main()
