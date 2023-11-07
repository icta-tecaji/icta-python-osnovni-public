import asyncio
from email.errors import NonASCIILocalPartDefect
import logging
import string
import random

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

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.example.com"


async def publish(queue, n):
    choices = string.ascii_lowercase + string.digits

    for x in range(1, n + 1):
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"dev-{host_id}"
        msg = PubSubMessage(message_id=x, instance_name=instance_name)
        await queue.put(msg)
        logging.info(f"Published {x} of {n} messages.")

    await queue.put(None)


async def consume(queue):
    while True:
        msg = await queue.get()
        if msg is None:
            break
        logging.info(f"Consumed {msg}")
        await asyncio.sleep(random.random())


def main():
    queue = asyncio.Queue()
    asyncio.run(publish(queue, 7))
    asyncio.run(consume(queue))


if __name__ == "__main__":
    main()
