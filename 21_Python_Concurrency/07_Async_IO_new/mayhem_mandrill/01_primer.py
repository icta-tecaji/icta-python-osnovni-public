"""
As I mentioned, one of the asyncio services we built is similar to a chaos monkey
to do periodic hard restarts of our entire fleet of instances. We'll build a
simplified version, dubbing it “Mayhem Mandrill” which will listen for a
pub/sub message as a trigger to go ahead and restart a host based off of that message.

This is an event-driven service that consumes from a pub/sub, and initiates a mock 
restart of a host. We could get thousands of messages in seconds, so as we get a 
message, we shouldn't block the handling of the next message we receive.
"""
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


# So far, we don’t have a running service; it’s merely just a pipeline or a batch job right now.
def main():
    queue = asyncio.Queue()
    asyncio.run(publish(queue, 5))
    asyncio.run(consume(queue))


if __name__ == "__main__":
    main()
