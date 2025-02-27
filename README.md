## Prequisites

1. Python 3.12.x or later
2. Local PostgreSQL instance
3. A table specified in `table.sql` file

## Setup

1. `git clone https://github.com/ExplodingBanana/weather-or-not.git`
2. `cd weather-or-not`
3. `pip install requirements.txt`
4. `touch .env`
5. Add `API_KEY` ([click to get](https://home.openweathermap.org/api_keys)) and a `DB_PASSWORD`. Also you can specify `DB_NAME` (defaults to `weather`) and USER (defaults to `postgres`)

## Running

It's as simple as `uvicorn app.main:app` and navigating to the provided URL

## Navigation

#### /weather

You'll be presented with a simple form.
Required inputs:
1. City name (only `A-z` and `-` are allowed)
2. Units of measurement

#### /history
A record of recent queries.
Supports paging, you can specify page size with the dropodown

## API Endpoints

#### /docs

Built-in Swagger-like documentaion, feel free to play around

#### /api/weather

Required query params:
1. `city_name`: `string`
2. `units`: `string` (one of `metric`, `imperial`, or `default`)

Response:
See [OpenWeather API](https://openweathermap.org/current#fields_json)

#### /api/history

Required query params:
1. `page`: `int` (will be set to 0 if provided value is negative)
2. `page_size`: `int` (will be clipped if set outside 0..100 range)

Response:
A `list[tuple]`

`tuple` follows `table.sql` structure. Basically columns in order

#### Known Issues

1. `.env` file *must* be in `UTF-8`, not `UTF-8-BOM`
2. If `psycopg2` starts acting up, replace with `psycopg2-binary`