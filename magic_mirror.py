""" Magic Mirror Prototype"""

import datetime
import calendar
import requests
import forecastio
import random
from flask import Flask, render_template


# API Key for ForecastIO
api_key = ""

# Latitude and Longitude for desired location for weather
lat =
lng =

# Sonarr IP Address & Port x.x.x.x:xxxx
sonarr_ip =

sonarr_api =


def forecast():
    """Connect to the ForecastIO API and load the hourly and daily weather. This
    information will be used in all other weather related functions and will be
    reloaded on each page refresh (ever 5 minutes) to get the latest information"""

    forecast.weather = forecastio.load_forecast(api_key, lat, lng,)
    forecast.hourly_weather = forecast.weather.hourly()
    forecast.daily_weather = forecast.weather.daily()


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

    for data in forecast.hourly_weather.data[:1]:
        temperature = int(round(data.apparentTemperature))
        return temperature


def current_weather_icon():
    """ Get the current weather icon. """

    for data in forecast.hourly_weather.data[:1]:
        icon = data.icon.replace(" ", "-")
        wi = "wi-forecast-io-" + icon
        return wi


def current_time():
    """ Get the current time. Used in weather_icon()"""

    return datetime.datetime.now()


def sunset():
    """ Determine what time the sun will set """

    for data in forecast.daily_weather.data:
        sunset_time = data.sunsetTime
        return sunset_time


def sunrise():
    """ Determine what time the sun will rise """

    for data in forecast.daily_weather.data:
        sunrise_time = data.sunriseTime
        return sunrise_time


def daily_weather_summary():
    """ Get the current weather summary. """

    for data in forecast.daily_weather.data[:1]:
        summary = data.summary
        return summary


def daily_weather_temperature_high():
    """ Get the high temperature for the day """

    for data in forecast.daily_weather.data[:1]:
        high_temp = int(round(data.apparentTemperatureMax))
        return high_temp


def daily_weather_temperature_low():
    """ Get the low temperature for the day """

    for data in forecast.daily_weather.data[:1]:
        low_temp = int(round(data.apparentTemperatureMin))
        return low_temp


def weekly_weather():
    """ Get the daily weather forecast for the next week. """

    # Create a blank list to store the weather data
    weekly_weather_list = []
    # Only pull data for tomorrow
    for data in forecast.daily_weather.data[1:2]:

        summary = data.summary

        high_temp = str(
            (int(round(data.apparentTemperatureMax))))

        low_temp = str(
            (int(round(data.apparentTemperatureMin))))

        icon = "wi-forecast-io-" + data.icon

        weekly_weather_list.append((summary, high_temp, low_temp, icon))
    print weekly_weather_list
    return weekly_weather_list


def sonarr():

    # Get the current date and time for today and tomorrow and then format to
    # match the API
    today = datetime.datetime.now()
    today = today.strftime("%Y-%m-%d")

    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%Y-%m-%d")

    # Create a new list to house the episode names
    tv_shows = []

    try:
        # Query the Sonarr API for the episodes being downloaded tonight
        show_calendar = requests.get(
            'http://{}/api/calendar?start={}&end={}&apikey={}'.format(sonarr_ip, q today, tomorrow, sonarr_api), timeout=15)

        # Format the API Data correctly
        new_tonight = show_calendar.json()

        # Loop through the API data and pull the TV show names
        for show in new_tonight:
            tv_shows.append(show['series']['title'])

        # Remove Duplicates from the list
        tv_shows = list(set(tv_shows))
    except:
        tv_shows.append('error')

    return tv_shows


def traffic():
    """ Get the travel time from home to work. """

    google_api_key = ''

    origin = ''

    destination = ""

    '''API Request formated for JSON between the orgin and destination with best
    guess traffic conditions if you were to leave now. '''
    driving_directions = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json?origin={}&destination={}&mode=driving&traffic_model=best_guess&departure_time=now&key={}'.format(origin, destination, google_api_key))

    # Format the API get as JSON
    driving_directions = driving_directions.json()

    # Pull out the routes list
    driving_directions = driving_directions['routes']

    for section in driving_directions:
        for section in (section['legs']):
            time = section['duration_in_traffic']

    # Pull the time key, value pair
    time = time['text']

    # Strip 'mins' from the result and remove all spaces
    return time[:-4].strip()

APP = Flask(__name__)


@APP.route('/')
def index():
    """ Create the HTML Page """

    # Connect to the ForecastIO API
    forecast()

    return render_template('index.html', traffic=traffic(), tv=sonarr(), date=date_time(), high=daily_weather_temperature_high(), low=daily_weather_temperature_low(), temp=current_weather_temp(), conditions=daily_weather_summary(), wi=current_weather_icon(), weekly=weekly_weather())

if __name__ == '__main__':
    APP.run(debug=True)
