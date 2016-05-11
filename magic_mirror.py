""" Magic Mirror Prototype"""

import datetime
import calendar
import time
import pyowm
from flask import Flask, render_template


CITY = 'Saint Louis, US'

WEATHER = pyowm.OWM('a59738017ea5ee759dcf34f47f5f1d8c')

LOCATION = WEATHER.weather_at_place(CITY)

CURRENT_WEATHER = LOCATION.get_weather()


def current_temperature():
    """ Get the current temperature. """

    temp_stats = CURRENT_WEATHER.get_temperature('fahrenheit')

    for key, value in temp_stats.iteritems():
        if key == "temp":
            temp = round(value)

    return str(int(temp))


def current_weather_conditions():
    """ Get the current status of the weathe (ex. Clear Sky) """
    condition_status = CURRENT_WEATHER.get_detailed_status()

    return condition_status


def date_time():
    """ Get the current date """
    now = datetime.datetime.now()

    weekday = datetime.date.today().strftime("%A")
    month = now.month
    day = str(now.day)

    month_name = calendar.month_name[month]

    current_date = (weekday + ", " + month_name + " " + day)

    return current_date


def current_time():
    """ Get the current time. Used in weather_icon()"""
    current_time.now = time.time()
    return current_time.now


def sunrise():
    """ Get todays sunrise time. Used in weather_icon()"""
    sunrise.time = CURRENT_WEATHER.get_sunrise_time()
    return sunrise.time


def sunset():
    """ Get todays sunset time. Used in weather_icon()"""
    sunset.time = CURRENT_WEATHER.get_sunset_time()
    return sunset.time


def weather_icon():
    """ Get the OWN weather code and the format correctly for the CSS weather
    icons"""

    # Get the weather code from the OpenWeatherAPI
    weather_code = CURRENT_WEATHER.get_weather_code()

    # Replace any spaces with a - for proper HTML formatting
    icon_label = "owf owf-" + str(weather_code)

    # Determine if it is night or day and get the proper prefix

    if sunrise() <= current_time() <= sunset():
        label_suffix = "-d"
    else:
        label_suffix = "-n"

    icon_label = (icon_label + label_suffix)

    return icon_label


APP = Flask(__name__)


@APP.route('/')
def index():
    """ Create the HTHML Page """

    return render_template('index.html', date=date_time(), temp=current_temperature(), conditions=current_weather_conditions(), weather=weather_icon())

if __name__ == '__main__':
    APP.run()
