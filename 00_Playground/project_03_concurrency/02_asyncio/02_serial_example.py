import asyncio

import aioserial


async def write_to_db(message):
    asyncio.sleep(0.5)
    print(f"Writing {message} to database")


async def read_and_print(aioserial_instance: aioserial.AioSerial):
    while True:
        message = await aioserial_instance.read_async().decode(errors="ignore")
        print(message)
        await write_to_db(message)


asyncio.run(read_and_print(aioserial.AioSerial(port="COM1")))
