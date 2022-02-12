from typing import Optional
from datetime import datetime

from pydantic import BaseModel


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
    dt_time: datetime