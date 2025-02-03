"""Primer 02 - Analytics."""

import csv
import time
from pathlib import Path

import duckdb as dd
import pandas as pd
import polars as pl
from loguru import logger

MAIN_PATH = Path(__file__).parent


# mean, min, max dc_link_voltage_avrg


def analytics_example_raw_python() -> None:
    """Analytics example raw Python."""
    file_path = MAIN_PATH / "stroj.csv"
    start_time_total = time.time()

    with file_path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)
        start_time = time.time()
        voltages = [float(row["dc_link_voltage_avrg"]) for row in data if row["dc_link_voltage_avrg"]]
        mean_voltage = sum(voltages) / len(voltages)
        min_voltage = min(voltages)
        max_voltage = max(voltages)
        print(f"Mean voltage: {mean_voltage:.2f}, Min voltage: {min_voltage:.2f}, Max voltage: {max_voltage:.2f}")

    logger.info(
        f"[analytics_example_raw_python] Total time elapsed: {time.time() - start_time_total:.4f} s. (Analysis: {time.time() - start_time:.4f} s.)",
    )


def analytics_example_pandas() -> None:
    """Analytics example Pandas."""
    file_path = MAIN_PATH / "stroj.csv"
    start_time_total = time.time()
    df = pd.read_csv(file_path)
    start_time = time.time()
    voltages = df["dc_link_voltage_avrg"].dropna().astype(float)
    mean_voltage = voltages.mean()
    min_voltage = voltages.min()
    max_voltage = voltages.max()
    print(f"Mean voltage: {mean_voltage:.2f}, Min voltage: {min_voltage:.2f}, Max voltage: {max_voltage:.2f}")

    logger.info(
        f"[analytics_example_pandas] Total time elapsed: {time.time() - start_time_total:.4f} s. (Analysis: {time.time() - start_time:.4f} s.)",
    )


def analytics_example_polars() -> None:
    """Analytics example Polars."""
    file_path = MAIN_PATH / "stroj.csv"
    start_time_total = time.time()
    df = pl.read_csv(file_path)
    start_time = time.time()
    voltages = df["dc_link_voltage_avrg"].drop_nulls().cast(pl.Float64)
    mean_voltage = voltages.mean()
    min_voltage = voltages.min()
    max_voltage = voltages.max()
    print(f"Mean voltage: {mean_voltage:.2f}, Min voltage: {min_voltage:.2f}, Max voltage: {max_voltage:.2f}")

    logger.info(
        f"[analytics_example_polars] Total time elapsed: {time.time() - start_time_total:.4f} s. (Analysis: {time.time() - start_time:.4f} s.)",
    )


def analytics_example_duckdb() -> None:
    """Analytics example DuckDB."""
    file_path = MAIN_PATH / "stroj.csv"
    # Convert to DB file
    file_path_db = MAIN_PATH / "stroj.db"
    # df = pd.read_csv(file_path)
    # df.to_sql("data", f"sqlite:///{file_path_db}", index=False)
    # start_time_total = time.time()
    start_time_total = time.time()
    con = dd.connect()
    # con.execute("INSTALL sqlite;")
    # con.execute("LOAD sqlite;")
    con = dd.connect(str(file_path_db))

    start_time = time.time()
    query = """
    SELECT
        AVG(dc_link_voltage_avrg) AS mean_voltage,
        MIN(dc_link_voltage_avrg) AS min_voltage,
        MAX(dc_link_voltage_avrg) AS max_voltage
    FROM data
    """
    result = con.execute(query).fetchall()
    mean_voltage, min_voltage, max_voltage = result[0]
    print(f"Mean voltage: {mean_voltage:.2f}, Min voltage: {min_voltage:.2f}, Max voltage: {max_voltage:.2f}")
    logger.info(
        f"[analytics_example_duckdb] Total time elapsed: {time.time() - start_time_total:.4f} s. (Analysis: {time.time() - start_time:.4f} s.)",
    )


if __name__ == "__main__":
    analytics_example_polars()
    analytics_example_raw_python()
    # analytics_example_pandas()

    # analytics_example_duckdb()
