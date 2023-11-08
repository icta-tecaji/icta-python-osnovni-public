"""
Concurrent work
We may want to do more than one thing per message. For example, we’d like to store the 
message in a database for potentially replaying later as well as initiate a restart of the given host.
"""
import asyncio
import logging
import random
import string
import uuid

import attr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


# Like we did with adding the restart_host functionality, let’s update the PubSubMessage class definition to add
# another boolean attribute for easier testing in the future:
@attr.s
class PubSubMessage:
    instance_name = attr.ib()
    message_id = attr.ib(repr=False)
    hostname = attr.ib(repr=False, init=False)
    restarted = attr.ib(repr=False, default=False)
    saved = attr.ib(repr=False, default=False)

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.example.net"


# And now let’s define a save coroutine function:
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
        # log line in publish to debug so we can see the concurrent consumer work a little easier)
        logging.debug(f"Published message {msg}")
        # simulate randomness of publishing messages
        await asyncio.sleep(random.random())


# Within the consume coroutine function, we could just await on both coroutines serially:
async def consume(queue):
    while True:
        msg = await queue.get()
        logging.info(f"Consumed {msg}")
        # sequential awaits may **not** be what you want
        await save(msg)
        await restart_host(msg)


def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(publish(queue))
        loop.create_task(consume(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interrupted")
    finally:
        loop.close()
        logging.info("Successfully shutdown the Mayhem service.")


if __name__ == "__main__":
    main()

# Let’s ignore that final ERROR line for now; we’ll be addressing it in exception handling.
