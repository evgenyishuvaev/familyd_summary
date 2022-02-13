import json
from datetime import datetime

from .database import metadata, engine, database
from .models import city, weather
from .exceptions import CRUDInvalidCityOrCountryCodeName, CRUDInvalidDateFormat


def init_db():
    metadata.create_all(engine)


async def import_json_city_data():

    await database.connect()
    with open("city.list.json", "rb") as file_r:
        lst = file_r.read()
        lst_city = json.loads(lst)

        for _city in lst_city:
            query = city.insert().values(
                id=_city["id"],
                name=_city["name"],
                state=_city["state"],
                country_code=_city["country"],
                lat=_city["coord"]["lat"],
                lon=_city["coord"]["lon"]
                )

            await database.execute(query)
            print(_city)
    await database.disconnect()


async def get_weather_by_name_and_datetime(city_name: str, dt_time: int):
    
    try:
        date_time = datetime.strptime(dt_time, "%Y:%m:%dT%H:%M")
    except ValueError:
        raise CRUDInvalidDateFormat(cod=400)
    
    await database.connect()
    query = weather.select().where(
        weather.c.city_name == city_name,
        weather.c.datetime == date_time
        )
    result = await database.fetch_one(query)
    await database.disconnect()
    return result


async def insert_weather(city_name: str, temp: float, feels_like: float, date_time: int):
    
    await database.connect()
    query = weather.insert().values(
        city_name=city_name,
        temp=temp,
        feels_like=feels_like,
        datetime=datetime.fromtimestamp(date_time)
        )
    result = await database.execute(query)
    await database.disconnect()
    return result


async def get_city_by_name_and_country_code(city_name: str, country_code: str):

    await database.connect()
    query = city.select().where(
        city.c.name == city_name,
        city.c.country_code == country_code
        )
    result = await database.fetch_one(query)
    await database.disconnect()

    if result == None:
        raise CRUDInvalidCityOrCountryCodeName(cod=400, city_name=city_name, cr_code=country_code)
    return result