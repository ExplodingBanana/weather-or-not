from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.weather_api import Units, get_weather, sanitize
import app.db as db

app = FastAPI()
templates = Jinja2Templates("templates")


@app.get("/")
def read_root(request: Request):
    """
    Redirects to actual UI
    """
    return RedirectResponse("/weather", status_code=303)

@app.get("/weather")
def display_query_page(request: Request):
    """
    Returns a template with an imnput form
    """
    return templates.TemplateResponse(request=request, name="query_form.jinja")

@app.post("/weather")
def fetch_weather(request: Request, city_name: Annotated[str, Form()], units: Annotated[Units, Form()]):
    """
    Processes the form input
    """
    city_name = sanitize(city_name)
    
    weather = get_weather(city_name, units)
    weather.update({"units": units.value}) # a carry-on
    
    db.add_record(city_name, units, weather)
    
    
    return templates.TemplateResponse(request=request, name="report.jinja", context={"weather": weather})

@app.get("/history")
def history(request: Request, page: int = 0, page_size: int = 10):
    return templates.TemplateResponse(request=request, name="table.jinja", context={"queries": db.get_history(page, page_size)})

@app.get("/api/weather")
def direct_weather(name: str, units: Units | None = None):
    """
    API endpoint for direct fetching
    """
    name = sanitize(name)
    weather = get_weather(name, units)
    db.add_record(name, units, weather)
    return weather

@app.get("/api/history")
def direct_history(page: int = 0, page_size: int = 10):
    """
    API endpoint for direct fetching
    """
    return db.get_history(page, page_size)