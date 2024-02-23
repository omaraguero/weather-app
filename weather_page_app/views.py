from django.shortcuts import render
import requests
import datetime

from collections import defaultdict
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    APIKEY = '5a090215a6c4f655f915938cfc59cc51'
    currentWeatherURL = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecastURL = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}'

    if request.method == "POST":
        city = request.POST['city']
        
        weatherData, dailyForecasts = fetchWeatherAndForecast(city, APIKEY, currentWeatherURL, forecastURL)
        
        context = {
            'weatherData': weatherData,
            'dailyForecasts': dailyForecasts,
        }
        
        return render(request, 'weather_page_app/index.html', context)
        
    else:
        return render(request, 'weather_page_app/index.html')
    
def fetchWeatherAndForecast(city, APIKEY, currentWeatherURL, forecastURL):
    response = requests.get(currentWeatherURL.format(city, APIKEY)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    
    weatherData = {
        'city':city,
        'temperature': round(response['main']['temp']-273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }
    
    forecastResponse = requests.get(forecastURL.format(lat, lon, APIKEY)).json()
    dailyForecasts = defaultdict(list)
    
    for dailyData in forecastResponse['list'][:40]:
        dtTimeStamp = datetime.datetime.fromtimestamp(dailyData['dt'])
        dayOfWeek = dtTimeStamp.strftime('%A')
        
        dailyForecasts[dayOfWeek].append({
            'date': dtTimeStamp.date(),
            'day': dayOfWeek,
            'time': dtTimeStamp.strftime('%H:%M'),
            'min_temp': round(dailyData['main']['temp_min'] - 273.15, 2),
            'max_temp':round(dailyData['main']['temp_max']- 273.15, 2),
            'description': dailyData['weather'][0]['description'],
            'icon': dailyData['weather'][0]['icon'],
        })
        
    return weatherData, dailyForecasts
        
        
    