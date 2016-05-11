
import forecastio
import datetime

api_key = "937134dbfd129ec4ce041e6856e82377"
lat = 38.5284
lng = -90.3562

WEATHER = forecastio.load_forecast(api_key, lat, lng,)


def current_weather():
    """ Get the current temperature. """

    hourly_weather = WEATHER.hourly()

    for data in hourly_weather.data[:1]:
        current_weather.temperature = int(round(data.temperature))
        current_weather.summary = data.summary
        current_weather.icon = data.icon


current_weather()

print
print "Current Temperature: " + str(current_weather.temperature)
print "Current Summary: " + current_weather.summary
print "Weather Icon: " + current_weather.icon
print

'''

def date_time():
    now = datetime.datetime.now()

    date_time.year = now.year
    date_time.month = now.month
    date_time.day = now.day


date_time()

day = mlbgame.day(date_time.year, date_time.month,
                  8, home="Cardinals")

game = day[0]

print ("The " + game.w_team + " beat the " + game.l_team)'''
