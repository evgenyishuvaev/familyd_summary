# Необходимо реализовать сервис, который реализует получение данных погоды по API.

Реализовать GET API /weather, которое в качестве параметров принимает код страны, город и дату со временем.
Сервис должен ответить информацией о погоде, воспользовавшись api OpenWeather (https://openweathermap.org/)
Например: /weather?country_code=RU&city=Moscow&date=< день в диапазоне доступных дат >T12:00
Выдает информацию о погоде для Москвы на 12:00 выбранного дня
Полученную информацию сохранять и при повторном запросе уже возвращать, не обращаясь к api сервиса погоды.

## Технические требования:
* aiohttp или FastAPI
* PostgreSQL или MySQL
* Не использовать готовых сторонних клиентов  для обращения к api OpenWeather (aiohttp httpx можно,  pyowm и pywws нет)

## Будет плюсом:
* Следование DRY, SOLID
* Оформить в Docker
* Покрыть реализацию тестами
