from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from db_access.crud import (
    init_db,
    import_json_city_data,
    get_weather_by_name_and_datetime,
    get_city_by_name_and_country_code,
    insert_weather
    )
from db_access.schemas import Weather, WeatherIn, WeatherInCurrent, WeatherJSONResponse
from db_access.exceptions import CRUDInvalidCityName, CRUDInvalidDateFormat

from services.open_weather.api import get_historical_weather_from_api
from services.open_weather.exceptions import InvalidApiKey, InvalidDateFormat

app = FastAPI()


@app.exception_handler(InvalidApiKey)
async def invalid_api_handler(request: Request, exc: InvalidApiKey):
    return JSONResponse(status_code=exc.cod, content=exc.desc_json)

@app.exception_handler(InvalidDateFormat)
async def invalid_date_fromat(request: Request, exc: InvalidDateFormat):
    return JSONResponse(status_code=exc.cod, content=exc.desc_json)

@app.exception_handler(CRUDInvalidCityName)
async def invalid_city_name(request: Request, exc: CRUDInvalidCityName):
    return JSONResponse(status_code=400, content= exc.desc_json)

@app.exception_handler(CRUDInvalidDateFormat)
async def invalid_city_name(request: Request, exc: CRUDInvalidDateFormat):
    return JSONResponse(status_code=400, content= exc.desc_json)


@app.get("/create_db")
async def create_db():
    init_db()

@app.get("/import_json")
async def import_json():
    await import_json_city_data()

@app.get("/weather", response_model=WeatherJSONResponse)
async def get_and_return_weather(country_code: str, city: str, date: str):

    db_weather = await get_weather_by_name_and_datetime(city_name=city, dt_time=date)
    
    if db_weather:
        weather = Weather.parse_obj(db_weather)
        return JSONResponse(content=weather.for_json_response())
    
    db_city = await get_city_by_name_and_country_code(city, country_code)

    resp_weather = await get_historical_weather_from_api(
                                            lat=db_city.lat,
                                            lon=db_city.lon,
                                            lang=country_code,
                                            dt=date
                                            )

    weather = WeatherIn.parse_obj(resp_weather)
    await insert_weather(
        city_name=city,
        temp=weather.current.temp,
        feels_like=weather.current.feels_like,
        date_time=weather.current.dt
        )

    return JSONResponse(
        content=WeatherJSONResponse(
            city_name=city,
            temp=weather.current.temp,
            feels_like=weather.current.feels_like,
            datetime=weather.current.dt,
            ).dict()
        )
