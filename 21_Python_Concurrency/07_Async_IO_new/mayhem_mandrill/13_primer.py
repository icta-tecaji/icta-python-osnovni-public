"""
Specific Handlers


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


class RestartFailed(Exception):
    pass


async def save(msg):
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())
    if random.randrange(1, 5) == 3:
        raise Exception(f"Could not save {msg}")
    msg.save = True
    logging.info(f"Saved {msg} into database")


async def restart_host(msg):
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())
    if random.randrange(1, 5) == 3:
        raise RestartFailed(f"Could not restart {msg.hostname}")
    msg.restart = True
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

        await asyncio.sleep(random.random())


async def cleanup(msg):
    # unhelpful simulation of i/o work
    await asyncio.sleep(random.random())
    msg.acked = True
    logging.info(f"Done. Acked {msg}")


def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    logging.error(f"Caught exception: {msg}")
    logging.info("Shutting down...")
    asyncio.create_task(shutdown(loop))


# Of course the global exception handler on the loop handles this, but there is
# something nuanced going on. Within handle_message, we use asyncio.gather where
# the return_exceptions is set to False by default. When it is False,
# which then triggers our global handle_exception function and then the shutdown coroutine.

# Let me reiterate: handle_message will never complete when a message errors.
async def handle_message(msg):
    results = await asyncio.gather(save(msg), restart_host(msg), return_exceptions=True)
    handle_results(results, msg)
    await cleanup(msg)


# To address this, we can pass in return_exceptions=True to asyncio.gather so that
# exceptions get returned as successful results, rather than raised. We’ll then have
# a specific exception handler:
def handle_results(results, msg):
    for result in results:
        if isinstance(result, RestartFailed):
            logging.error(f"Retrying for failure to restart: {msg.hostname}")
        elif isinstance(result, Exception):
            logging.error(f"Handling general error: {result}")


# Remove exception
async def consume(queue):
    while True:
        msg = await queue.get()
        logging.info(f"Consumed {msg}")
        asyncio.create_task(handle_message(msg))


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

# Exceptions will not crash the system - unlike non-asyncio programs.
# And they might go unnoticed, as we saw when return_exceptions=False,
# where we failied to save a message causing us to never hit cleanup.

# Be sure to set some sort of exception handling – either globally with
# loop.set_exception_handler, individually like in our handle_results
# function, or a mix of both (you’ll probably need a mix).

# I personally like using asyncio.gather because the order of the returned
# results are deterministic, but it’s easy to get tripped up with it. By
# default, it will swallow exceptions but happily continue working on the
# other tasks that were given. If an exception is never returned, weird
# behavior can happen like we saw.
