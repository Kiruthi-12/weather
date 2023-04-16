from django.conf import settings
from django.shortcuts import render
import requests

def location(request):
    ip_request = requests.get('https://api.ipify.org?format=json')
    ip_address = ip_request.json()['ip']
    url = 'http://ip-api.com/json/' + ip_address
    geo_request = requests.get(url)
    geo_data = geo_request.json()

    context = {
        'latitude': geo_data.get('lat', 'Unknown'),
        'longitude': geo_data.get('lon', 'Unknown'),
        'city': geo_data.get('city', 'Unknown'),
        'region': geo_data.get('regionName', 'Unknown'),
        'country': geo_data.get('country', 'Unknown')
    }

    # Pass the city to the weather data function
    weather_data = get_weather_data(context['city'])
    if weather_data:
        context.update(weather_data)

    return render(request, 'location.html', context)


def get_weather_data(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': 'a9e23e1a25fedbeabaa41010d1169635',
        'units': 'metric',
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return {}

    json_response = response.json()

    weather_data = {
        'temp': json_response['main']['temp'],
        'temp_min': json_response['main']['temp_min'],
        'temp_max': json_response['main']['temp_max'],
        'city': json_response['name'],
        'country': json_response['sys']['country'],
        'lat': json_response['coord']['lat'],
        'lon': json_response['coord']['lon'],
        'weather': json_response['weather'][0]['main'],
        'weather_desc': json_response['weather'][0]['description'],
        'pressure': json_response['main']['pressure'],
        'humidity': json_response['main']['humidity'],
        'wind_speed': json_response['wind']['speed'],
    }

    return weather_data