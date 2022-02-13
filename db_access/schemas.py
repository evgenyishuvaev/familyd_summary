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


class WeatherJSONResponse(BaseModel):
    city_name: str
    temp: float
    feels_like: float
    datetime: int


class Weather(BaseModel):
    city_name: str
    temp: float
    feels_like: float
    datetime: datetime

    def for_json_response(self):
        """Return serializeble data, e.g convert datetime -> int"""

        return WeatherJSONResponse(
            city_name=self.city_name,
            temp=self.temp,
            feels_like=self.feels_like,
            datetime= int(datetime.timestamp(self.datetime))
            ).dict()

class WeatherInCurrent(BaseModel):
    dt: int
    temp: float
    feels_like: float


class WeatherIn(BaseModel):
    current: WeatherInCurrent



