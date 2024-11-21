import asyncio
import signal
from pathlib import Path

from aiofile import async_open
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import Float, Integer, insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

demo_data_file_path = Path(__file__).parent / "8001_2022-10-03.txt"
current_buffered_line = []
engine = create_async_engine("sqlite+aiosqlite:///meritve.db", echo=False)
async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    """Base class for database models."""


class MeritveAltTest(Base):
    """Data model for the message data."""

    __tablename__ = "alt_test"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=True)
    uptime: Mapped[int] = mapped_column(Integer, nullable=True)
    ntc_temp: Mapped[float] = mapped_column(Float, nullable=True)
    bridge_temp: Mapped[float] = mapped_column(Float, nullable=True)
    target_speed_rpm: Mapped[int] = mapped_column(Integer, nullable=True)
    speed_rpm: Mapped[int] = mapped_column(Integer, nullable=True)
    motor_power_w: Mapped[int] = mapped_column(Integer, nullable=True)


class MessageData(BaseModel):
    """Data model for the message data."""

    timestamp: int
    uptime: int | None
    ntc_temp: float | None
    bridge_temp: float | None
    target_speed_rpm: int | None
    speed_rpm: int | None
    motor_power_w: int | None


async def data_generator(queue) -> None:
    """Generate fake COM port reads from local file."""
    async with async_open(demo_data_file_path, "r") as afp:
        while True:
            line = await afp.readline()
            if not line:
                break
            asyncio.create_task(queue.put(line))
            # logger.debug(f"Generating new COM port line. Size of queue: {queue.qsize()}")
            # await asyncio.sleep(random.random() / 20)


async def save_to_db(message_data: MessageData) -> None:
    """Save the message data to the database."""
    async with async_session() as session, session.begin():
        stmt = insert(MeritveAltTest).values(message_data.model_dump())
        await session.execute(stmt)
        await session.commit()


async def data_parser(line: str) -> None:
    """Parse the data from the COM port."""
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
            asyncio.create_task(save_to_db(message_data))
        except Exception as e:
            logger.error(f"Failed to parse the data: {e}: {current_buffered_line}")
            current_buffered_line.clear()

        logger.success(f"New message detected: {message_data}")
        current_buffered_line.clear()


async def data_reader(queue) -> None:
    """Read data from the queue and process it."""
    while True:
        line = await queue.get()
        await data_parser(line)


async def shutdown(loop, signal=None) -> None:
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logger.warning(f"Received exit signal {signal.name}...")
    logger.info("Nacking outstanding messages")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    logger.info("Flushing metrics")
    loop.stop()


async def startup() -> None:
    """Prepare the service for startup."""
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.success("Database tables created successfully!")


def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())
    try:
        loop.create_task(data_generator(queue))
        loop.create_task(data_reader(queue))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown(loop, signal.SIGINT))
    finally:
        loop.close()
        logger.success("Successfully shutdown the event loop!")


if __name__ == "__main__":
    main()
