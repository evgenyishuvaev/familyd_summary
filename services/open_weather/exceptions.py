

class InvalidApiKey(Exception):
    "Invalid API key. Please see http://openweathermap.org/faq#error401 for more info"

    def __init__(self, cod, msg):
        self.cod = cod
        self.msg = msg
        self.desc_json = {
            "code": cod,
            "message": self.msg
        }

class InvalidDateFormat(Exception):
    "Invalid date format was used"

    def __init__(self, cod):
        self.cod = cod
        self.desc = "Invalid date format was used. Can use only UTC format time"
        self.desc_json = {
            "code": cod,
            "message": self.desc
        }