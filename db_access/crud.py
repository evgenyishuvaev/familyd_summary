import json

from .database import metadata, engine, database
from .models import city, weather

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