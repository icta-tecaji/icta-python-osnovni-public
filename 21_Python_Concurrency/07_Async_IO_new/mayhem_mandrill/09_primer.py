"""
Graceful Shutdowns with asyncio

Often, you’ll want your service to gracefully shutdown if it receives a POSIX signal 
of some sort, e.g. clean up open database connections, stop consuming messages, 
finish responding to current requests while not accepting new requests, etc. So, 
if we happen to restart an instance of our own service, we should clean up the “mess” 
we’ve made before exiting out.

We’ve been catching the commonly-known KeyboardInterrupt exception like many
other tutorials and libraries. But there are many common signals that a service
should expect and handled. A few typical ones are (descriptions from man signal):

SIGHUP - Hangup detected on controlling terminal or death of controlling process
SIGQUIT - Quit from keyboard (via ^\)
SIGTERM - Termination signal
SIGINT - Interrupt program

There’s also SIGKILL (i.e. the familiar kill -9) and SIGSTOP, although the standard 
is that they can’t be caught, blocked, or ignored.

Currently, if we quit our service via ^\ or send a signal via something like pkill -TERM -f 
<script path>, our service doesn’t get a chance to clean up:
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


# And let’s add yet another boolean attribute to our PubSubMessage class:
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


async def handle_message(msg):
    await asyncio.gather(save(msg), restart_host(msg))
    await cleanup(msg)


async def consume(queue):
    while True:
        msg = await queue.get()
        logging.info(f"Consumed {msg}")
        asyncio.create_task(handle_message(msg))


# So, instead of catching KeyboardInterrupt, let’s attach some signal handlers to the loop.
# First, we should define the shutdown behavior we want when a signal is caught:
async def shutdown(signal, loop):
    """Cleanup tasks tied to the service's shutdown."""
    # Here I’m just closing that simulated database connections, returning messages to
    # pub/sub as not acknowledged (so they can be redelivered and not dropped), and
    # finally cancelling the tasks. We don’t necessarily need to cancel pending tasks;
    # we could just collect and allow them to finish. We may also want to take this
    # opportunity to flush any collected metrics so they’re not lost.
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
    # Let’s hook this up to the main event loop now. We can also remove the
    # KeyboardInterrupt catch since that’s now taken care of with adding
    # signal.SIGINT as a handled signal.
    loop = asyncio.get_event_loop()
    # May want to catch other signals too
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        # Side note: You might have noticed that within the lambda closure, I binded the s
        # immediately. This is because without that, we end up running into an apparently
        # common gotcha in Python-land: late bindings.
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))
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
