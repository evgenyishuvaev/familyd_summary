from multiprocessing.sharedctypes import Value
import aiohttp
from datetime import datetime

from .exceptions import InvalidApiKey, InvalidDateFormat

from config import load_config

cfg = load_config()

payload={
    "lat": None,
    "lon": None,
    "exclude": "hourly",
    "units": "metric",
    "lang": "ru",
    "appid": cfg.API.KEY,
}


session = aiohttp.ClientSession(cfg.API.URL)

async def check_access_and_valid_data(resp_json: dict, session: aiohttp.ClientSession):
    
    if resp_json.get("cod") == 400:
        await session.close()
        raise InvalidDateFormat(resp_json["cod"])

    if resp_json.get("cod") == 401:
        await session.close()
        raise InvalidApiKey(resp_json["cod"], resp_json["message"])


async def get_weather_from_api(lat: float, lon: float, lang: str, dt: str):


    try:
        time_stamp = int(datetime.strptime(dt, "%Y:%m:%dT%H:%M").timestamp())
        print(time_stamp)
    except ValueError:
        raise InvalidDateFormat(cod=400)
    
    payload["lat"], payload["lon"], payload["lang"], payload["dt"] = lat, lon, lang.lower(), time_stamp

    async with session.get("/data/2.5/onecall/timemachine", params=payload) as resp:
        resp_json = await resp.json()
        print(resp_json)
        await check_access_and_valid_data(resp_json, session)    
    await session.close()
    return resp_json