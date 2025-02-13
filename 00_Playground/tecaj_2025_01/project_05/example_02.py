import csv
from pathlib import Path

import pandas as pd
from sqlalchemy import Column, Float, Integer, MetaData, String, Table, create_engine, text

MAIN_PATH = Path(__file__).parent
file_path = MAIN_PATH / "gapminder_unfiltered.csv"


engine = create_engine("sqlite+pysqlite:///gapminder.db")
metadata_obj = MetaData()

user_table = Table(
    "countries",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("country", String),
    Column("continent", String),
    Column("year", Integer),
    Column("life_exp", Float),
    Column("population", Integer),
    Column("gdp", Float),
)
metadata_obj.create_all(engine)


def insert_data_raw():
    # Insert data into the table
    with file_path.open("r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        next(reader)  # Skip the header
        for row in reader:
            print(row)
            stmt = user_table.insert().values(
                country=row[0],
                continent=row[1],
                year=int(row[2]),
                life_exp=float(row[3]),
                population=int(row[4]),
                gdp=float(row[5]),
            )
            with engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()


def insert_data_pandas():
    data = pd.read_csv(file_path)
    data.rename(columns={"lifeExp": "life_exp", "pop": "population", "gdpPercap": "gdp"}, inplace=True)
    data.to_sql(
        "countries",
        engine,
        if_exists="replace",
        index=False,
        dtype={
            "country": String,
            "continent": String,
            "year": Integer,
            "life_exp": Float,
            "population": Integer,
            "gdp": Float,
        },
    )


def select_biggest_gdp():
    query = """SELECT country, AVG(gdp) as avg_gdp
                FROM countries
                GROUP BY country
                ORDER BY avg_gdp DESC
                LIMIT 1;"""
    with engine.connect() as conn:
        result = conn.execute(text(query))
        data = result.fetchall()
        print(f"The country with the biggest GDP is {data[0][0]} with an average GDP of {data[0][1]}")


if __name__ == "__main__":
    # insert_data_raw()
    insert_data_pandas()
    select_biggest_gdp()
