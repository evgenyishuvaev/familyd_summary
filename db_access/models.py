from xmlrpc.client import DateTime
from sqlalchemy import Table, Column, String, Integer, Float, DateTime

from .database import metadata


city = Table(
    "city",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("state", String),
    Column("country_code", String),
    Column("lat", Float),
    Column("lon", Float)
)


weather = Table(
    "weather",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("city_name", String),
    Column("temp", Float),
    Column("feels_like", Float),
    Column("datetime", DateTime)
)