"""
This might seem obvious to some, but it definitely isn’t to all. We are 
essentially blocking ourselves; first we produce all the messages, one 
by one. Then we consume them, one by one. The loops we have (for x in 
range(1, n+1) in publish(), and while True in consume()) block ourselves 
from moving onto the next message while we await to do something.

While this is technically a working example of a pub/sub-like queue with 
asyncio, it’s not what we want. Whether we are building an event-driven
 service (like this walk through), or a pipeline/batch job, we’re not taking advantage 
 of the concurrency that asyncio can provide.
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

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.example.net"


# Let’s first create a mock publisher that will always be publishing restart
# request messages, and therefore never indicate that it’s done. This also
#  means we’re not providing a set number of messages to publish, so we have to
# rework that a bit, too. Here I’m adding a while True loop since we don’t want
# a finite number of messages to create. I’m also adding the creation of a unique
# ID for each message produced.

# And finally – one of the key parts: I’m no longer using await with queue.put(msg). Instead,
# I’m using asyncio.create_task(queue.put(msg)):
async def publish(queue):
    choices = string.ascii_lowercase + string.digits

    while True:
        msg_id = str(uuid.uuid4())
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"cattle-{host_id}"
        msg = PubSubMessage(message_id=msg_id, instance_name=instance_name)
        # publish an item
        #  If we left the await in here, everything after within the scope of the publish
        # coroutine function will be blocked. This isn’t that much of an issue in our current
        # setup
        # However, it could be if we limited the size of the queue, then that await could be
        # waiting on space to free up in the queue. So using create_task tells the loop
        # to put the message on the queue as soon as it gets a chance, and allows us to
        # continue on publishing messages.
        asyncio.create_task(queue.put(msg))
        logging.info(f"Published message {msg}")
        # simulate randomness of publishing messages
        await asyncio.sleep(random.random())


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
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(publish(queue))
        # preizkusimo samo create task
        # loop.create_task(consume(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interrupted")
    finally:
        loop.close()
        logging.info("Successfully shutdown the Mayhem service.")


if __name__ == "__main__":
    main()

# Let’s ignore that final ERROR line for now; we’ll be addressing it in exception handling.
