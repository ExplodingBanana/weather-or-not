import datetime
import psycopg2
from dotenv import get_key

from app.weather_api import Units

PASSWORD = get_key(".env", "API_KEY")
if PASSWORD is None:
    raise Exception("Please set DB_PASSWORD in the .env file")

CONNECTION = psycopg2.connect(f"dbname=weather user=postgres password={PASSWORD}")

CURSOR = CONNECTION.cursor()

def add_record(city_name: str, units: Units, weather: dict):
    """Records a query, an absolute mess inside
    
    Args:
        city_name (str):
        units (Units):
        weather (dict): Basically an OpenWeather API response
    """
    if weather['cod'] == "404":
        CURSOR.execute("INSERT INTO history (time, city, units, successful) VALUES (%s, %s, %s, %s)", (datetime.datetime.now(), city_name, units.value, False))
    elif weather['cod'] == 200:
        # Oof, if only SQL was elegant
        # Kinda dependent on the OpenWeather API response structure, but whatever
        CURSOR.execute("""INSERT INTO history
                       (time, city, units, description, temperature, pressure, humidity, successful)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                       (datetime.datetime.now(), city_name,
                        units.value, weather['weather'][0]['description'],
                        round(weather['main']['temp']), weather['main']['pressure'],
                        weather['main']['humidity'], True))
    else:
        raise Exception("Response invalid. Can't process")
    CONNECTION.commit()
    
    
def get_history(page: int = 0, page_size: int = 10):
    """Retrieves query history from Postgres DB

    Args:
        page (int, optional): Defaults to 0 if unset or less then 0.
        page_size (int, optional): Defaults to 10 if unset, less then 0, or more then 100.

    Returns:
        tuple: SQL query result
    """
    if page < 0:
        page = 0
    if page_size < 0 or page_size > 100:
        page_size = 10
    
    CURSOR.execute(f"SELECT * FROM history OFFSET {page * page_size} LIMIT {page * page_size + page_size}")
    return CURSOR.fetchall()

if __name__ == "__main__":
    print(get_history())