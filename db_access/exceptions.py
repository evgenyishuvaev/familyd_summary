

class CRUDInvalidCityOrCountryCodeName(Exception):
    "Invalid date format was used"

    def __init__(self, cod, city_name, cr_code):
        self.cod = cod
        self.city_name = city_name
        self.cr_code = cr_code
        self.desc = f"Invalid city or country code name was use: city='{city_name}' country='{cr_code}' !"
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