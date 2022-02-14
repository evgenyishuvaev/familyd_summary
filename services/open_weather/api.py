from multiprocessing.sharedctypes import Value
import aiohttp
from datetime import datetime

from .exceptions import (
    InvalidApiKey,
    InvalidDateFormat,
    OutOfAllowedRangeDate,
    OutOfAllowedTwoDaysRangeDate
    )

from config import load_config

cfg = load_config()

payload={
    "lat": None,
    "lon": None,
    "exclude": "",
    "units": "metric",
    "lang": "ru",
    "appid": cfg.API.KEY,
}


session = aiohttp.ClientSession(cfg.API.URL)

async def check_access_and_valid_error(resp_json: dict, session: aiohttp.ClientSession):
    
    if resp_json.get("cod") == 400:
        await session.close()
        raise InvalidDateFormat(resp_json["cod"])
    
    if resp_json.get("cod") == 401:
        await session.close()
        raise InvalidApiKey(resp_json["cod"], resp_json["message"])
    
    if resp_json.get("message") == "requested time is out of allowed range of 5 days back":
        await session.close()
        raise OutOfAllowedRangeDate(resp_json["cod"])

async def get_weather_from_api(lat: float, lon: float, lang: str, dt: str):

    try:
        date_time = datetime.strptime(dt, "%Y:%m:%dT%H:%M")
    except ValueError:
        raise InvalidDateFormat(cod=400)

    time_delta = int(date_time.timestamp() - datetime.now().timestamp())

    print(time_delta)

    if time_delta > 169200:
        raise OutOfAllowedTwoDaysRangeDate(cod=400)

    time_stamp = int(date_time.timestamp())
    if time_stamp < datetime.now().timestamp():
        return await get_historical_weather(lat, lon, lang, time_stamp)
    return await get_forecast_weather(lat, lon, lang, time_stamp)


async def get_forecast_weather(lat: float, lon: float, lang: str, dt: int):
    """Request forecast weather data from Open Weather Map API
       from endpoint: https://api.openweathermap.org/data/2.5/onecall
    """
    
    payload["exclude"] = "daily,minutely,current,alerts"
    payload["lat"], payload["lon"], payload["lang"] = lat, lon, lang
    requested_weather = {"current": {}}
    
    async with session.get("/data/2.5/onecall", params=payload) as resp:
        resp_json = await resp.json()
        print(resp_json)
        await check_access_and_valid_error(resp_json, session)
        for weather in resp_json["hourly"]:
            print(weather["dt"], dt)
            if weather["dt"] == dt:
                requested_weather["current"].update(weather)
        return requested_weather 


async def get_historical_weather(lat: float, lon: float, lang: str, dt: int):
    """Request historical weather data from Open Weather Map API
       from endpoint: https://api.openweathermap.org/data/2.5/onecall/timemachine
    """
    
    payload["lat"], payload["lon"], payload["lang"], payload["dt"] = lat, lon, lang.lower(), dt

    async with session.get("/data/2.5/onecall/timemachine", params=payload) as resp:
        resp_json = await resp.json()
        await check_access_and_valid_error(resp_json, session)    
    return resp_json