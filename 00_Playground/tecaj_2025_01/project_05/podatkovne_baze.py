# Relational Databases (SQL DB) - Microsoft SQL Server, Oracle, MariaDB, MySQL, PostgreSQL, SQLite
# NoSQL Databases - MongoDB, CouchDB, Cassandra
# Key-value databases - Redis, Memcached
# Time series databases - InfluxDB, TimescaleDB

from sqlalchemy import Boolean, Column, Integer, MetaData, String, Table, create_engine, insert, select, text

engine = create_engine("sqlite+pysqlite:///primer_demo.db")
metadata_obj = MetaData()

user_table = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
    Column("is_admin", Boolean, default=False),
)

metadata_obj.create_all(engine)

stmt1 = insert(user_table).values(name="Bob", fullname="Bob B", is_admin=True)
stmt2 = insert(user_table).values(name="Kim", fullname="Kim K", is_admin=False)
stmt3 = insert(user_table).values(name="Jim", fullname="Jim J", is_admin=True)
stmt4 = text("INSERT INTO user (name, fullname, is_admin) VALUES ('Pat', 'Pat P', 0)")

select_stmt_1 = select(user_table).where(user_table.c.name == "Bob")
select_stmt_2 = text("SELECT * FROM user WHERE name = 'Kim'")
# print(select_stmt_1)

with engine.connect() as conn:
    # conn.execute(stmt1)
    # conn.execute(stmt2)
    # conn.execute(stmt3)
    # conn.execute(stmt4)
    # conn.commit()
    result = conn.execute(select_stmt_2)
    print(result.fetchall())
