from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class City(BaseModel):
    id : int
    name: str
    state: Optional[str]
    country_code: str
    lat: float
    lon: float


class Weather(BaseModel):
    id: int
    city_name: str
    temp: float
    feels_like: float
    datetime: datetime


class WeatherInCurrent(BaseModel):
    dt: int
    temp: float
    feels_like: float


class WeatherIn(BaseModel):
    current: WeatherInCurrent