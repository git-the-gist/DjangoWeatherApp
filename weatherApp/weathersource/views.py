from django.shortcuts import render
from pyowm.commons.exceptions import *
from ipstack import GeoLookup  # using ipstack to find the user's exact ip address
import ipinfo  # using ipinfo to retrieve information on the ip's owner
import pyowm  # importing pyowm to receive weather data

owm = pyowm.OWM('0d92fe6673852fd95c9d1ff3a259685a')  # defining pyowm API key

mgr = owm.weather_manager()  # calling PyOWM weather manager

geo_lookup = GeoLookup("1379a525f4c6d711990c5bb322c9f4ea")  # defining our API key for ipstack

location = geo_lookup.get_own_location()  # using the "get_own_location()" method to get the user's location

ip_address = location['ip']  # using the 'ip' key of the location dictionary to retrieve our own ip_address


def index(request):
    if request.method == 'POST':
        city = str(request.POST["city"])  # if the POST method is used, do the following
        try:
            observation = mgr.weather_at_place(city)  # getting weather data from pyowm
            w = observation.weather  # defining the weather object
            temp_dict = w.temperature('celsius')  # calling the temp dictionary from pyowm
            temp = int(temp_dict['temp'])  # accessing the current temp in degrees celsius
            low = int(temp_dict['temp_min'])  # accessing the current low in degrees celsius
            high = int(temp_dict['temp_max'])  # accessing the current high in degrees celsius
            humidity = int(w.humidity)  # accessing the current humidity in percentage
            wind_dict = observation.weather.wind(unit='miles_hour')  # calling the wind dictionary from pyowm
            wind_speed = int(wind_dict['speed'])  # accessing the current wind speed
            wind_degree = int(wind_dict['deg'])  # accessing the current wind degree
            status = w.detailed_status  # accessing the current weather status
            icon = w.weather_icon_url()  # accessing the pyowm weather icon

            def wind_speed_km(speed):  # defining a function to get wind speed in km
                return int(speed * 1.609)

            def wind_direction(wind):  # defining wind direction based on wind degree
                compass = {'1': 'N', '2': 'NE', '3': 'E', '4': 'SE', '5': 'S', '6': 'SW', '7': 'W', '8': 'NW'}
                modulo = (wind % 360)
                round = int(modulo / 45) + 1
                return compass[str(round)]

            def weather_icon(icon):  # returning only the reference number for the weather icon
                att = list(icon.split("/"))
                return att[5][0:3]

            city_weather = {  # defining the values to render in a dictionary
                'city': city.title(),
                'temp': temp,
                'status': status,
                'icon': weather_icon(icon),
                'high': high,
                'low': low,
                'humidity': humidity,
                'wind': f"WIND: {wind_direction(wind_degree)} {wind_speed_km(wind_speed)} km/h"
            }

            context = {'city_weather': city_weather}
            return render(request, 'weathersource/django_index.html', context)

        except APIResponseError or IndexError or BadGatewayError or NotFoundError or InvalidSSLCertificateError:
            return render(request, 'weathersource/django_404.html')  # exception handling

    else:
        try:
            access_token = 'd6a18753dde2ed'  # defining our access_token for ipinfo
            handler = ipinfo.getHandler(access_token)  # defining a handler for our API operations
            details = handler.getDetails()  # using the "getDetails()" method on "ip_address" to get
            # the user's info based on their ip address
            city = details.city  # defining the city for pyowm to find location info
            country = details.country  # defining the country for pyowm to find location info
            observation = mgr.weather_at_place(city + ',' + country)
            w = observation.weather
            temp_dict = w.temperature('celsius')  # calling the temp dictionary from pyowm
            temp = int(temp_dict['temp'])  # accessing the current temp in degrees celsius
            low = int(temp_dict['temp_min'])  # accessing the current low in degrees celsius
            high = int(temp_dict['temp_max'])  # accessing the current high in degrees celsius
            humidity = int(w.humidity)  # accessing the current humidity in percentage
            wind_dict = observation.weather.wind(unit='miles_hour')  # calling the wind dictionary from pyowm
            wind_speed = int(wind_dict['speed'])  # accessing the current wind speed
            wind_degree = int(wind_dict['deg'])  # accessing the current wind degree
            status = w.detailed_status  # accessing the current weather status
            icon = w.weather_icon_url()  # accessing the pyowm weather icon

            def wind_speed_km(speed):  # defining a function to get wind speed in km
                return int(speed * 1.609)

            def wind_direction(wind):  # defining wind direction based on wind degree
                compass = {'1': 'N', '2': 'NE', '3': 'E', '4': 'SE', '5': 'S', '6': 'SW', '7': 'W', '8': 'NW'}
                modulo = (wind % 360)
                round = int(modulo / 45) + 1
                return compass[str(round)]

            def weather_icon(icon):  # returning only the reference number for the weather icon
                att = list(icon.split("/"))
                return att[5][0:3]

            city_weather = {  # defining the values to render in a dictionary
                'city': city.title(),
                'temp': temp,
                'status': status,
                'icon': weather_icon(icon),
                'high': high,
                'low': low,
                'humidity': humidity,
                'wind': f"WIND: {wind_direction(wind_degree)} {wind_speed_km(wind_speed)} km/h"
            }

            context = {'city_weather': city_weather}
            return render(request, 'weathersource/django_index.html', context)

        except APIRequestError or IndexError or BadGatewayError or NotFoundError or InvalidSSLCertificateError:
            return render(request, 'weathersource/django_page_not_found.html')  # exception handling
