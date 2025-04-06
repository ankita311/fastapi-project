from fastapi import FastAPI, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import requests
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")
API_KEY = "d3924a9862061bdd58299ef7ee0e5f42"

cat_votes = 0
dog_votes = 0

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dogs")
def show_dogs(request: Request):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    image_url = response.json()['message']

    return templates.TemplateResponse("animal.html", {"request": request, "image_url": image_url, "title": "Dog Image", "animal": "dog"})

@app.get("/cats")
def show_cats(request: Request):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    image_url = response.json()[0]['url']

    return templates.TemplateResponse("animal.html", {"request": request, "image_url": image_url, "title": "Cat Image", "animal": "cat"})

@app.get("/both")
def show_animals(request: Request):
    r_dog = requests.get('https://dog.ceo/api/breeds/image/random')
    image_dog = r_dog.json()['message']

    r_cat = requests.get('https://api.thecatapi.com/v1/images/search')
    image_cat = r_cat.json()[0]['url']

    return templates.TemplateResponse("both.html", {
        "request": request, 
        "image_dog": image_dog, 
        "image_cat": image_cat,
        "cat_votes": cat_votes,
        "dog_votes": dog_votes})

@app.post("/vote")
def vote(animal: str = Form(...)):
    global cat_votes, dog_votes

    if animal == "cat":
        cat_votes += 1
    elif animal == "dog":
        dog_votes += 1

    return RedirectResponse(url="/both", status_code=303)

@app.get("/weather/", response_class=HTMLResponse)
def show_weather(request: Request, city: Optional[str] = Query(default=None)):
    if city is None:
        return templates.TemplateResponse("weather.html", {
            "request": request,
            "city": None,
            "temp": None,
            "hum": None,
            "sea_level": None,
            "wind_speed": None
        })
    import urllib.parse
    encoded_city = urllib.parse.quote(city)

    coord = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={encoded_city}&limit=1&appid={API_KEY}")
    
    coord_data = coord.json()
    if not coord_data:
        return templates.TemplateResponse("weather.html", {
            "request": request,
            "error": f"No results found for city {city}",
            "city": city
        })
    
    lat = coord_data[0]['lat']
    lon = coord_data[0]['lon']

    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
    weather_data = weather.json()
    
    temp = weather_data['main']['temp']
    hum = weather_data['main']['humidity']
    sea_level = weather_data['main']['sea_level']
    wind_speed = weather_data['wind']['speed']

    return templates.TemplateResponse("weather.html", 
                                      {"request": request, 
                                       "city": city, 
                                       "temp": temp, 
                                       "hum": hum, 
                                       "sea_level": sea_level, 
                                       "wind_speed": wind_speed})

