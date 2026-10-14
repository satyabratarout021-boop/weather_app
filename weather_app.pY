from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

API_KEY = "fc92cf2efa40b58e6715e5564c912b3d"


HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #4facfe, #00f2fe);
            margin: 0;
            padding: 20px;
            text-align: center;
        }

        .container {
            max-width: 400px;
            margin: 40px auto;
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        input {
            width: 90%;
            padding: 14px;
            border: 1px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
        }

        button {
            margin-top: 15px;
            padding: 13px 25px;
            border: none;
            border-radius: 10px;
            background: #007bff;
            color: white;
            font-size: 16px;
        }

        .weather {
            margin-top: 25px;
        }

        .temp {
            font-size: 45px;
            font-weight: bold;
        }

        .error {
            color: red;
            margin-top: 15px;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🌤️ Weather App</h1>

    <form method="POST">

        <input
            type="text"
            name="city"
            placeholder="Enter city name"
            required
        >

        <br>

        <button type="submit">
            Check Weather
        </button>

    </form>

    {% if weather %}

    <div class="weather">

        <h2>{{ weather.city }}</h2>

        <div class="temp">
            {{ weather.temperature }}°C
        </div>

        <h3>{{ weather.description }}</h3>

        <p>💧 Humidity: {{ weather.humidity }}%</p>

        <p>💨 Wind: {{ weather.wind }} m/s</p>

    </div>

    {% endif %}

    {% if error %}
        <div class="error">
            {{ error }}
        </div>
    {% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None

    if request.method == "POST":

        city = request.form.get("city")

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        try:

            response = requests.get(url, params=params)
            data = response.json()

            if response.status_code == 200:

                weather = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"]
                }

            else:
                error = "City not found!"

        except Exception as e:
            error = "Something went wrong."

    return render_template_string(
        HTML,
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)