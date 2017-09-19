
import sys
import math
import requests

base_url = 'http://api.openweathermap.org/data/2.5/weather'
api_key = 'KEY'  # << Get your API key (APPID) here: http://openweathermap.org/appid
cities = ['Esztergom', 'London, UK']


def get_temperature(city):
  query = base_url + '?q=%s&appid=%s' % (city, api_key)
  try:
    response = requests.get(query)
    # print("[%s] %s" % (response.status_code, response.url))
    if response.status_code != 200:
      response = 'N/A'
      return response
    else:
      weather_data = response.json()
      return weather_data
  except requests.exceptions.RequestException as error:
    print (error)
    sys.exit(1)

def get_weather():
  location = get_temperature('Jalgaon')
  cloud_condition="Condition is "+str(location['weather'][0]['description'])
  temp="  and Temperature is "+str(round((location['main']['temp']-273),2))+" degree celsius"

  r=cloud_condition+temp
  return r
