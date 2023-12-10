from django.http import HttpResponse
from django.shortcuts import render
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import requests
import pytz
from datetime import datetime

# Create your views here.

def index(request):
    try:
        if request.method == 'POST':
            API_KEY = 'f07253201d848e3d31aa62925f3db822'
            
            #getting the city name from the form input
            city_name = request.POST.get('city')

            #locating the city
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(city_name)
            obj = TimezoneFinder()
            result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

            # url for current weather with city name and API key
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
            response = requests.get(url).json()

            # Getting the time of a given timezone
            current_time = datetime.now(pytz.timezone(result))
            format_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")

            city_weather_update = {
                'city' : city_name,
                'description' : response['weather'][0]['description'],
                'icon' : response['weather'][0]['icon'],
                'temperature' : 'Temperature: ' + str(response['main']['temp']) + ' °C',
                'country_code': response['sys']['country'],
                'wind': 'Wind: ' + str(response['wind']['speed']) + 'km/h',
                'humidity': 'Humidity: ' + str(response['main']['humidity']) + '%',
                'time': format_time,
                'timezone' : result
            }
        else:
            city_weather_update = {}

        context = {'city_weather_update': city_weather_update}
        return render(request, 'home.html', context)
    except:
        return render(request, '404.html')
