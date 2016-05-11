""" Magic Mirror Prototype"""

import datetime
import calendar
import time
import forecastio
from flask import Flask, render_template


# API Key for ForecastIO
api_key = ""

# Latitude and Longitude for desired location
lat = ""
lng = ""

WEATHER = forecastio.load_forecast(api_key, lat, lng,)
HOURLY_WEATHER = WEATHER.hourly()


def date_time():
    """ Get the current date """
    now = datetime.datetime.now()

    weekday = datetime.date.today().strftime("%A")
    month = now.month
    day = str(now.day)

    month_name = calendar.month_name[month]

    current_date = (weekday + ", " + month_name + " " + day)

    return current_date


def current_weather_temp():
    """ Get the current temperature. """

    for data in HOURLY_WEATHER.data[:1]:
        temperature = int(round(data.temperature))
        return temperature


def current_weather_summary():
    """ Get the current weather summary. """

    for data in HOURLY_WEATHER.data[:1]:
        summary = data.summary
        return summary


def current_weather_icon():
    """ Get the current weather icon. """

    for data in HOURLY_WEATHER.data[:1]:
        icon = data.icon.replace(" ", "-")
        wi = "wi-forecast-io-" + icon
        return wi


def current_time():
    """ Get the current time. Used in weather_icon()"""
    current_time.now = time.time()
    return current_time.now

APP = Flask(__name__)


@APP.route('/')
def index():
    """ Create the HTML Page """

    return render_template('index.html', date=date_time(), temp=current_weather_temp(), conditions=current_weather_summary(), wi=current_weather_icon())

if __name__ == '__main__':
    APP.run(debug=True)
