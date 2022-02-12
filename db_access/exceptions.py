

class CRUDInvalidCityName(Exception):
    "Invalid date format was used"

    def __init__(self, cod, city_name):
        self.cod = cod
        self.city_name = city_name
        self.desc = f"Invalid city name was use: '{city_name}' !"
        self.desc_json = {
            "code": cod,
            "message": self.desc
        }

class CRUDInvalidDateFormat(Exception):
    "Invalid date format was used"

    def __init__(self, cod):
        self.cod = cod
        self.desc = "Invalid date format was used. Can use only UTC format time"
        self.desc_json = {
            "code": cod,
            "message": self.desc
        }