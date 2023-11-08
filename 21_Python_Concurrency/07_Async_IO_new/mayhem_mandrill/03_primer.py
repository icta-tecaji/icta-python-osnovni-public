import asyncio
import logging
import random
import string

import attr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


@attr.s
class PubSubMessage:
    # ib Create a new attribute on a class.
    instance_name = attr.ib()
    message_id = attr.ib(repr=False)
    # Include this attribute in the generated __repr__ method.
    # Include this attribute in the generated __init__ method. It is possible to
    # # set this to False and set a default value. In that case this attributed
    # # is unconditionally initialized with the specified default value or factory.
    hostname = attr.ib(repr=False, init=False)

    # If a __attrs_post_init__ method exists on the class, it will be called after the class is fully initialized.
    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.example.net"


# simulating an external publisher of events
async def publish(queue, n):
    choices = string.ascii_lowercase + string.digits

    for x in range(1, n + 1):
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"cattle-{host_id}"
        msg = PubSubMessage(message_id=x, instance_name=instance_name)
        await queue.put(msg)
        logging.info(f"Published {x} of {n} messages")

    await queue.put(None)  # publisher is done


async def consume(queue):
    while True:
        # wait for an item from the publisher
        msg = await queue.get()
        if msg is None:  # publisher is done
            break

        # process the msg
        logging.info(f"Consumed {msg}")
        # unhelpful simulation of i/o work
        await asyncio.sleep(random.random())


def main():
    # We’ve been stopping our service with CTRL-C, a.k.a. SIGINT, a.k.a. KeyboardInterrupt.
    # So let’s wrap our running of the service in a try/catch/finally around that interrupt signal:
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(publish(queue, 5))
        loop.create_task(consume(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interrupted")
    finally:
        loop.close()
        logging.info("Successfully shutdown the Mayhem service.")


if __name__ == "__main__":
    main()
