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
        self.hostname = f"{self.instance_name}.example.com"


async def publish(queue):
    choices = string.ascii_lowercase + string.digits

    while True:
        msg_id = str(uuid.uuid4())
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"dev-{host_id}"
        msg = PubSubMessage(message_id=msg_id, instance_name=instance_name)
        asyncio.create_task(queue.put(msg))
        logging.debug(f"Publish message {msg}.")
        await asyncio.sleep(random.random())


async def save(msg):
    # klic za sghranjevanje v bazo
    await asyncio.sleep(random.random())
    msg.saved = True
    logging.info(f"Saved: {msg.hostname} into DB.")


async def restart_host(msg):
    # klicete api za restart
    await asyncio.sleep(random.random())
    msg.restarted = True
    logging.info(f"Restarted: {msg.hostname}.")


async def cleanup(msg):
    await asyncio.sleep(random.random())
    msg.acked = True
    logging.info(f"Done. Acked: {msg}")


async def handle_message(msg):
    await asyncio.gather(save(msg), restart_host(msg))
    await cleanup(msg)


async def consume(queue):
    while True:
        msg = await queue.get()
        logging.info(f"Consumed {msg}")
        asyncio.create_task(handle_message(msg))


async def shutdown(signal, loop):
    logging.info(f"Recieved exit signal {signal.name}")
    # zaprli povezave na bazo in ostale zadeve
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [t.cancel() for t in tasks]
    logging.info(f"Cancelling {len(tasks)} outstanding tasks.")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


def main():
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)

    for s in signals:
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    queue = asyncio.Queue()

    try:
        loop.create_task(publish(queue))
        loop.create_task(consume(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Process interupted")
    finally:
        loop.close()
        logging.info("Successfully shutdown the service.")


if __name__ == "__main__":
    main()
