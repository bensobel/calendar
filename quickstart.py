from __future__ import print_function
import httplib2
import os

import requests

import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

import json

import feedparser

import settings

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_weather():
    camb_city_id = '4931972'
    bos_city_id = '4930956'
    weather_url = 'http://api.openweathermap.org/data/2.5/forecast?id={0}&cnt=1&units=imperial&APPID={1}'.format(camb_city_id,settings.WEATHER_API_KEY)
    r = requests.get(weather_url)
    return r.json()

def format_weather(j):
    desc = j['list'][0]['weather'][0]['description']
    hi = j['list'][0]['main']['temp_max']
    lo = j['list'][0]['main']['temp_min']
    #sunrise = 
    #sunset = 
    return "{0}. High: {1}, Low: {2}.".format(desc,hi,lo)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_news():
    news_feed = 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305'
    feed = feedparser.parse(news_feed)
    x = 1
    latest_x_stories = []
    count = 0
    while count < x:
        #2017-05-10T11:54:57-04:00
        title = feed.entries[0].title
        story_time = time.strptime(feed.entries[count].updated, '%Y-%m-%dT%H:%M:%S-04:00')
        time_formatted = time.strftime('%I:%M%p',story_time)
        story = feed.entries[count].summary_detail.value
        d = {"title":title,"detail":story,"time":time_formatted}
        latest_x_stories.append(d)
        count +=1
    return latest_x_stories

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    tmrw = (datetime.datetime.utcnow()+datetime.timedelta(days=1)).isoformat() + 'Z'
    local_now = datetime.datetime.now()
    #print(local_now.strftime('%A, %B %d, %Y'))
    #print('Getting the upcoming 10 events')

    #get all calendars
    calendar_list = [item['id'] for item in service.calendarList().list().execute().get('items',[])]

    all_events = []
    #make sure to get all calendars
    for cal in calendar_list:
        eventsResult = service.events().list(
            calendarId=cal, timeMin=now, timeMax=tmrw, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        all_events += events

    if not all_events:
        print('No upcoming events found.')
    for event in all_events:
        location = ""
        try:
            location = "({0})".format(event['location'])
            pass
        #handling keyerror if no location given
        except KeyError:
            pass
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        start_formatted = time.strftime('%I:%M%p',time.strptime(start, '%Y-%m-%dT%H:%M:%S-04:00'))
        end_formatted = time.strftime('%I:%M%p',time.strptime(end, '%Y-%m-%dT%H:%M:%S-04:00'))
        duration = "{0}-{1}".format(start_formatted,end_formatted)
        print("{0}: {1} {2}".format(duration, event['summary'],location))


if __name__ == '__main__':
    main()
    print(format_weather(get_weather()))
    for x in get_news():
        print(x['title'])
    #print(format_weather(get_weather()))
