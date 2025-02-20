from __future__ import annotations

import asyncio
from pathlib import Path

from aiofile import async_open
from loguru import logger
from pydantic import BaseModel

demo_data_file_path = Path(__file__).parent / "8001_2022-10-03.txt"
current_buffered_line = []


class MessageData(BaseModel):
    """Data model for the message data."""

    timestamp: int
    uptime: int | None
    ntc_temp: float | None
    bridge_temp: float | None
    target_speed_rpm: int | None
    speed_rpm: int | None
    motor_power_w: int | None


async def calculate_and_save_statistics(message_data: MessageData) -> None:
    """Calculate and save the statistics."""
    # Calculate the statistics and save to db
    await asyncio.sleep(0.2)
    logger.debug(f"Calculating and saving the statistics for: {message_data}")


async def data_parser(line: str) -> dict | None:
    """Parse the incoming data."""
    if not line:
        return
    line = line.strip()
    if "HW_INFO ::: Parameters" in line:
        logger.info("New message detected!")
        current_buffered_line.append(line)
    elif current_buffered_line and len(current_buffered_line) < 7:
        current_buffered_line.append(line)
    elif current_buffered_line and len(current_buffered_line) == 7:
        # Parse the data, save to db, and clear the buffer
        try:
            timestamp = int(current_buffered_line[0].split(" ")[0])
            uptime = int(current_buffered_line[1].split(" : ")[1].split(" ")[0])
            ntc_temp = float(current_buffered_line[2].split(" : ")[1].split(" ")[0]) if "-" not in current_buffered_line[2] else None
            bridge_temp = float(current_buffered_line[3].split(" : ")[1].split(" ")[0])
            target_speed_rpm = int(current_buffered_line[4].split(" : ")[1].split(" ")[0])
            speed_rpm = int(current_buffered_line[5].split(" : ")[1].split(" ")[0])
            motor_power_w = int(current_buffered_line[6].split(" : ")[1].split(" ")[0])
            message_data = MessageData(
                timestamp=timestamp,
                uptime=uptime,
                ntc_temp=ntc_temp,
                bridge_temp=bridge_temp,
                target_speed_rpm=target_speed_rpm,
                speed_rpm=speed_rpm,
                motor_power_w=motor_power_w,
            )
            asyncio.create_task(calculate_and_save_statistics(message_data))
        except Exception as e:
            logger.error(f"Failed to parse the data: {e}: {current_buffered_line}")
            current_buffered_line.clear()

        logger.success(f"New message detected: {message_data}")
        current_buffered_line.clear()


async def data_generator(queue: asyncio.Queue) -> None:
    """Generate fake COM port reads from local file."""
    async with async_open(demo_data_file_path, "r") as afp:
        while True:
            line = await afp.readline()
            # await asyncio.sleep(random.random() / 1000)
            if not line:
                break
            asyncio.create_task(queue.put(line))


async def data_reader(queue: asyncio.Queue) -> None:
    """Read data from the queue."""
    # import aioserial
    # aioserial_instance = aioserial.AioSerial(port="COM1")
    while True:
        # message = await aioserial_instance.read_async().decode(errors="ignore")
        message = await queue.get()
        await data_parser(message)


async def shutdown(loop) -> None:
    """Cleanup tasks tied to the service's shutdown."""
    logger.info("Nacking outstanding messages")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("Flushing metrics")
    loop.stop()


def main() -> None:
    """Run the main program."""
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(data_generator(queue))  # V praksi to generira naprava ki pošilja podatke v serial
        loop.create_task(data_reader(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown(loop))
    finally:
        loop.close()
        logger.success("Successfully shutdown the service")


if __name__ == "__main__":
    main()
