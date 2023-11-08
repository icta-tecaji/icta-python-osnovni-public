"""

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


@attr.s
class PubSubMessage:
    instance_name = attr.ib()
    message_id = attr.ib(repr=False)
    hostname = attr.ib(repr=False, init=False)
    restarted = attr.ib(repr=False, default=False)
    saved = attr.ib(repr=False, default=False)

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


async def consume(queue):
    while True:
        # Yay! Note that we still do use await with the msg = await queue.get() because we can’t do
        # anything further until we actually have a message. But restart_host and save do not need to
        # block each other, nor do they need to block the loop from consuming another message.
        msg = await queue.get()
        logging.info(f"Consumed {msg}")
        # We can see that although it doesn’t block the event loop, await save(msg) blocks await
        # restart_host(msg), which blocks the consumption of future messages. But, perhaps we
        # don’t need to await these two coroutines one right after another. These two tasks
        # don’t necessarily need to depend on one another – completely side-stepping the
        # potential concern/complexity of “should we restart a host if we fail to add the
        # message to the database”.

        # So let’s treat them as such. Instead of awaiting them, we can make use asyncio.create_task
        # again to have them scheduled on the loop, basically chucking it over to the loop for
        # it to execute when it next can.
        asyncio.create_task(save(msg))
        asyncio.create_task(restart_host(msg))


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
