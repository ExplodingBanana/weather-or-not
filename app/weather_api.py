import requests as r
from dotenv import get_key
from enum import Enum

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={key}&units={units}"

API_KEY = get_key(".env", "API_KEY")

if API_KEY is None:
    raise Exception("Please set API_KEY in the .env file")


class Units(str, Enum):
    metric = "metric"
    imperial = "imperial"
    default = "default"

def sanitize_filter(x:str):
    if x.isalpha or x == '-': # only letters and - accepted
        return True
    else:
        return False

def sanitize(name: str) -> str:
    return "".join(filter(sanitize_filter, name))

def get_weather(name: str, units: Units):
    name = sanitize(name) # a precaution, if unnecessary
    t = r.get(BASE_URL.format(city_name=name, key=API_KEY, units=units.value))
    return t.json()


if __name__ == "__main__":
    print(get_weather("Los Angeles", Units.metric)) # should be good
    print(get_weather("GooBoo", Units.metric)) # should return 404