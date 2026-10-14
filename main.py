import customtkinter as ctk
import requests
from datetime import datetime

from datetime import datetime

def update_time():
    now = datetime.now()
    current = now.strftime("%d-%m-%Y | %I:%M:%S %p")
    datetime_label.configure(text=current)
    app.after(1000, update_time)

import os
import customtkinter as ctk
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")




ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def change_background(condition):
    condition = condition.lower()

    if condition == "clear":
        app.configure(fg_color="#87CEEB")
    elif condition == "clouds":
        app.configure(fg_color="#708090")
    elif condition == "rain":
        app.configure(fg_color="#2F4F4F")
    elif condition == "drizzle":
        app.configure(fg_color="#4682B4")
    elif condition == "thunderstorm":
        app.configure(fg_color="#1C1C1C")
    elif condition == "snow":
        app.configure(fg_color="#E6E6FA")
    elif condition in ["mist", "fog", "haze"]:
        app.configure(fg_color="#B0C4DE")
    else:
        app.configure(fg_color="#242424")

def set_weather_icon(condition):
    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️",
        "Haze": "🌫️"
    }

    weather_icon.configure(
        text=icons.get(condition, "🌍")
    )

def get_weather():
    city = search.get().strip()

    if city == "":
        result.configure(text="⚠ Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            condition = data["weather"][0]["main"]
            change_background(condition)
            sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
            sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
            condition = data["weather"][0]["main"]
            set_weather_icon(condition)

            result.configure(
    text=f"📍 City : {data['name']}\n\n"
         f"🌡 Temperature : {data['main']['temp']}°C\n"
         f"🤗 Feels Like : {data['main']['feels_like']}°C\n"
         f"💧 Humidity : {data['main']['humidity']}%\n"
         f"🌬 Wind : {data['wind']['speed']} m/s\n"
         f"📊 Pressure : {data['main']['pressure']} hPa\n"
         f"☁ Weather : {data['weather'][0]['description'].title()}\n"
         f"🌅 Sunrise : {sunrise}\n"
         f"🌇 Sunset : {sunset}"
)
        else:
            result.configure(text="❌ City Not Found")

    except Exception as e:
        result.configure(text=f"Error: {e}")
app = ctk.CTk()
app.title("Live Weather App")
app.geometry("520x760")
app.resizable(False, False)
app.configure(fg_color="#0B1026")



title = ctk.CTkLabel(
    app,
    text="🌤 Live Weather App",
    font=("Segoe UI", 34, "bold"),
    text_color="white"
)
title.pack(pady=(25,10))

datetime_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 14)
)
datetime_label.pack(pady=5)

search = ctk.CTkEntry(
    app,
    width=250,
    height=50,
    corner_radius=25,
    placeholder_text="Enter City Name",
    font=("segoe UI",16)
)
search.pack(pady=15)




button = ctk.CTkButton(
    app,
    text="🔎 Search",
    width=360,
    height=50,
    corner_radius=25,
    font=("Segoe UI",18,"bold"),
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    command=get_weather
)
button.pack(pady=10)

search.bind("<Return>",lambda event:


get_weather())


card = ctk.CTkFrame(
    app,
    width=430,
    height=330,
    corner_radius=30,
    fg_color="#172554",
    border_width=2,
    border_color="#3B82F6"
)
card.pack(pady=30)
weather_icon = ctk.CTkLabel(
    card,
    text="☀️",
    font=("Segoe UI Emoji", 60)
)
weather_icon.pack(pady=(20,10))

result = ctk.CTkLabel(
    card,
    text="Search a city to see weather",
    font=("Segoe UI",18),
    justify="left",
    anchor="w",
    text_color="white"
)
result.pack(padx=25,pady=25)

update_time()

app.mainloop()
