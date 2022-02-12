

class InvalidApiKey(Exception):
    "Invalid API key. Please see http://openweathermap.org/faq#error401 for more info"

    def __init__(self, cod, msg):
        self.cod = cod
        self.msg = msg