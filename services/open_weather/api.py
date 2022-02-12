from datetime import datetime
import aiohttp

from .exceptions import InvalidApiKey

from config import load_config

cfg = load_config()

payload={
    "lat": 55.45,
    "lon": 37.37,
    "exclude": "hourly",
    "units": "metric",
    "lang": "ru",
    "appid": cfg.API.KEY,
}


session = aiohttp.ClientSession(cfg.API.URL)

async def check_access_and_valid_data(resp_json: dict):
    if resp_json.get("cod") == 401:
        raise InvalidApiKey(resp_json["cod"], resp_json["message"])

async def get_weather_by_time(lang: str, dt: datetime):   
    async with session.get("/data/2.5/onecall", params=payload) as resp:
        resp_json = await resp.json()
        print(resp_json)
        await check_access_and_valid_data(resp_json)
        return resp_json
    await session.close()