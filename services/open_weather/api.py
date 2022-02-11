import aiohttp

from config import load_config

cfg = load_config()

payload={
    "lat": 55.45,
    "lon": 37.37,
    "exclude": "hourly",
    "units": "metric",
    "lang": "ru",
    "api_key": cfg.API.KEY,
}


session = aiohttp.ClientSession(cfg.API.URL)

async def get_current_time_weather():
    
    async with session.get("/onecall") as resp:
        resp_json = await resp.json()
        print(resp)   
    session.close()