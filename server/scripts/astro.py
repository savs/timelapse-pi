import requests
import datetime
from dateutil import parser
import pytz
from datetime import datetime, timezone
from util import log

PORTLAND_LAT = '45.5227341'
PORTLAND_LNG = '-122.6759347'

def getUrl(date):
  return f'https://api.sunrise-sunset.org/json?lat={PORTLAND_LAT}&lng={PORTLAND_LNG}&date={date}&formatted=0'

def getDate(date, time):
  return parser.parse(f'{date} {time}')

def getWindow(date):
  url = getUrl(date)
  log(f'Getting sunrise/sunset: {url}')
  r = requests.get(url)
  log(f'Response: {r.json()}', False)
  return r.json()['results']['civil_twilight_begin'], r.json()['results']['civil_twilight_end']

def utcToLocal(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def getTime(date):
  return date.strftime("%H%M%S")

def getTimes(date):
  sunriseString, sunsetString = getWindow(date)
  sunrise = getTime(utcToLocal(getDate(date, sunriseString)))
  sunset = getTime(utcToLocal(getDate(date, sunsetString)))

  log(f'Sunrise: {sunrise}, Sunset: {sunset}')

  return sunrise, sunset

# print(getTimes('2019-12-24'))
