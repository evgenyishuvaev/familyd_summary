from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from db_access.crud import init_db, import_json_city_data

from services.open_weather.api import get_weather_by_time
from services.open_weather.exceptions import InvalidApiKey

app = FastAPI()


@app.exception_handler(InvalidApiKey)
async def invalid_api_handler(request: Request, exc: InvalidApiKey):
    return JSONResponse(status_code=exc.cod, content=exc.msg)


@app.get("/create_db")
async def create_db():
    init_db()

@app.get("/import_json")
async def import_json():
    import_json_city_data()

@app.get("/weather")
async def get_and_return_weather(country_code: str, city: str, date: datetime):
    return JSONResponse(content= await get_weather_by_time(lang=country_code, dt=date))

