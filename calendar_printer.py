#!/usr/bin/python
from __future__ import print_function
import httplib2
import sys
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

import dateutil
import dateutil.parser
import dateutil.tz

from library_api import get_lib_hours

PATH_TO_PRINTER = os.path.join(os.getcwd(),'Python-Thermal-Printer')

LOCAL_TZ = dateutil.tz.tzlocal()

sys.path.append(PATH_TO_PRINTER)

from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/ttyUSB0", 9600, timeout=5)

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
        title = feed.entries[count].title
        story_time = time.strptime(feed.entries[count].updated, '%Y-%m-%dT%H:%M:%S-04:00')
        time_formatted = time.strftime('%I:%M%p',story_time)
        story = feed.entries[count].summary_detail.value
        d = {"title":title,"detail":story,"time":time_formatted}
        latest_x_stories.append(d)
        count +=1
    return latest_x_stories

def printheader(txt,printer=printer):
    printer.setSize('M')
    printer.justify('C')
    printer.underlineOn()
    printer.println(txt)
    printer.underlineOff()
    printer.justify('L')
    printer.setSize('S')
    printer.feed(1)

def main():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.now(LOCAL_TZ)

    start_of_day = datetime.datetime.now(dateutil.tz.tzlocal()).replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + datetime.timedelta(hours=23, minutes=59, seconds = 59)
  
    #get all calendars
    calendar_list = [item['id'] for item in service.calendarList().list().execute().get('items',[])]

    #ID of my Todoist TODO list
    TODO_ID = 'bensobel.com_ipvtvckn2pv1u0tafontcqllks@group.calendar.google.com'

    #initialize lists of events and todos
    all_events = []

    todos = []

    #make sure to get all calendars
    for cal in calendar_list:
        eventsResult = service.events().list(
            calendarId=cal, timeMin=start_of_day.isoformat(),
            timeMax=end_of_day.isoformat(), maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        if cal == TODO_ID:
            todos += events
        else:
            all_events += events

    if (len(all_events) > 0) or (len(todos) > 0):
        output = []

        printer.setDefault() 

        printer.wake() 

        printheader(now.astimezone(LOCAL_TZ).strftime('%a, %b %d, \'%y'))

        printer.println("Weather: {0}".format(format_weather(get_weather())))
        printer.feed(1)

        lib = get_lib_hours(today)

        if lib:
        	if lib['closed']:
        		lib_formatted = "Closed"
	        else:
	        	lib_formatted = "{0}-{1}".format(lib['start_time'],lib['end_time'])
	        printer.println("Widener: {0}".format(lib_formatted))
	        printer.feed(1)


        if (len(all_events) > 0):
            printheader("Calendar:")
            for event in all_events:
                location = ""
                try:
                    location = "{0}".format(event['location']).replace("\n", " ")
                    pass
                #handling keyerror if no location given
                except KeyError:
                    pass
                start = event['start'].get('dateTime', event['start'].get('date'))

                end = event['end'].get('dateTime', event['end'].get('date'))

                #parse start and end time to dt object
                start_parsed = dateutil.parser.parse(start)
            
                end_parsed = dateutil.parser.parse(end)

                if (end_parsed - start_parsed) > (datetime.timedelta(hours=23, minutes=59, seconds = 59)):
                    all_day = True
                else:
                    all_day = False

                if all_day:
                    duration = "All day"
                else:
                    duration = "{0}-{1}".format(time.strftime('%I:%M%p',start_parsed.astimezone(LOCAL_TZ).timetuple()), time.strftime('%I:%M%p',end_parsed.astimezone(LOCAL_TZ).timetuple()))
                    
                d = {"start": start, "end": end, "location": location, "summary":event['summary'].encode('utf-8'), "duration": duration, "all_day":all_day}
                output.append(d)
                #print("{0}: {1} {2}".format(duration, event['summary'],location))
            ordered = sorted(output, key=lambda k: k['start']) 
            for e in ordered:
                printer.println("{0}: {1} ({2})".format(e['duration'], e['summary'],e['location']))
                printer.feed(1)

        #TODO List#
        if len(todos) > 0:
            printheader("To-do:")
            for t in todos:
                printer.println(t['summary'])

        printer.feed(3)
        printer.sleep()

    #else there are no events and todos, so do nothing
    else:
        pass


if __name__ == '__main__':
    main()    
    