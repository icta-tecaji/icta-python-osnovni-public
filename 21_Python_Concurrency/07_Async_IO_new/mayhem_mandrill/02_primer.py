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


# But this is a service, so we don’t want it to just run once, but continually
# consume from a publisher. And unfortunately, there isn’t a decent way to start
# a long-running service that is not an HTTP server in python 3.7. So we’ll stick with
# the pre-3.7 boilerplate.
def main():
    # With that, we’ll create tasks out of the two coroutines using asyncio.create_task,
    # which will schedule them on the loop. And then start the loop, telling it to run forever.
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.create_task(publish(queue, 5))
    loop.create_task(consume(queue))
    loop.run_forever()
    loop.close()
    logging.info("Successfully shutdown the Mayhem service.")


# When running with this updated code, we see that all messages are published and then consumed.
# Then we hang because there is no more work to be done; we only published 5 messages, after all.
# To stop the “hanging” process, we must interrupt it (via ^C or sending a signal like kill -15 <pid>):
if __name__ == "__main__":
    main()
