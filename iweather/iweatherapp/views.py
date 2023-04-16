from django.shortcuts import render
from django.http import HttpResponse
from iweatherapp.models import City
from iweatherapp.helper import get_weather_data
import requests
import json

# Create your views here.
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

    return render(request, 'location.html', context)

def home(request):
    
    if request.method == 'POST':
            print(city)
            weather_data = get_weather_data(city)
    elif request.method == 'GET':
        try:
            city = City.objects.latest('date_added').city
            weather_data = get_weather_data(city)
        except Exception as e:
            weather_data = None

    template_name = 'home.html'
    context = {'weather_data': weather_data}
    return render(request, template_name, context=context)


def history(request):
    template_name = 'history.html'
    cities = City.objects.all().order_by('-date_added')[:5]

    weather_data_list = []
    for city in cities:
        city = city.city
        weather_data_list.append(get_weather_data(city))

    context = {'weather_data_list': weather_data_list}
    return render(request, template_name, context)
