"""
Concurrent consumer
Now comes the time to add concurrency to the consumer bit. For this, the goal is to 
constantly consume messages from the queue and create non-blocking work based off 
of a newly-consumed message; in this case, to restart an instance.

The tricky part is the consumer needs to be written in a way that the consumption 
of a new message from the queue is separate from the work on the message itself. 
In other words, we have to simulate being “event-driven” by regularly pulling for 
a message in the queue since there’s no way to trigger work based off of a new message 
available in the queue (a.k.a. push-based).
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


# Let’s first update the PubSubMessage class definition to add a boolean attribute for easier
# testing in the future:
@attr.s
class PubSubMessage:
    instance_name = attr.ib()
    message_id = attr.ib(repr=False)
    hostname = attr.ib(repr=False, init=False)
    restarted = attr.ib(repr=False, default=False)

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.example.net"


# Now let’s add a coroutine that mocks the restart work that needs to be done on any consumed message:
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


# We’ll stick with our while True loop and await for the next message on the queue,
# and then create a task (and - not obviously - schedule it on the loop) out of
# restart_host rather than just await it.
async def consume(queue):
    while True:
        msg = await queue.get()
        logging.info(f"Consumed {msg}")
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

# Let’s ignore that final ERROR line for now; we’ll be addressing it in exception handling.
