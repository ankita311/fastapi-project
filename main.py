from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()
API_KEY = "d3924a9862061bdd58299ef7ee0e5f42"

@app.get("/")
def root():
    return {"message": "Welcome to my webpage"}

@app.get("/dogs")
def show_dogs():
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    image_url = response.json()['message']

    html_content = f""" 
    <html>
        <head><title>Random Dog Image</title></head>
        <body>
            <img src="{image_url}" alt='Dog Image' width='300'/>
        </body>
    </html>"""

    return HTMLResponse(content=html_content)

@app.get("/cats")
def show_cats():
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    image_url = response.json()[0]['url']

    html_content = f""" 
    <html>
        <head><title>Random Cat Image</title></head>
        <body>
            <img src="{image_url}" alt='Cat Image' width='300'/>
        </body>
    </html>"""

    return HTMLResponse(content=html_content)

@app.get("/both")
def show_animals():
    print(API_KEY)
    r_dog = requests.get('https://dog.ceo/api/breeds/image/random')
    image_dog = r_dog.json()['message']

    r_cat = requests.get('https://api.thecatapi.com/v1/images/search')
    image_cat = r_cat.json()[0]['url']

    html_content = f""" 
    <html>
        <head><title>Random Cat and Dog Image</title></head>
        <body>
            <h1>This is a cat</h1>
            <img src="{image_cat}" alt='Cat Image' width = '300' />

            <h1>This is a dog</h1>
            <img src="{image_dog}" alt='Dog Image' width='300'/>
        </body>
    </html>"""
    
    return HTMLResponse(content=html_content)


@app.get("/weather/{city}")
def show_weather(city: str):
    coord = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}")
    
    coord_data = coord.json()
    if not coord_data:
        return {"error": "City doesn't exist"}
    
    lat = coord_data[0]['lat']
    lon = coord_data[0]['lon']

    weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric")
    weather_data = weather.json()
    if not weather_data:
        return {"error": "Invalid"}
    
    temp = weather_data['main']['temp']
    hum = weather_data['main']['humidity']
    sea_level = weather_data['main']['sea_level']
    wind_speed = weather_data['wind']['speed']

    html_content = f""" 
    <html>
        <head><title>Weather Forecast</title></head>
        <body>
            <h1>Weather conditions of {city} are:<h1>
            Temperature = {temp} deg C<br>
            Humidity = {hum} % <br>
            Sea Level = {sea_level} Pa<br>
            Wind Speed = {wind_speed} km/h <br>
        </body>
    </html>"""
    
    return HTMLResponse(content=html_content)

