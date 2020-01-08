from datetime import datetime
import caldav
from icalendar import Calendar
from caldav.elements import dav, cdav
import requests
from requests.auth import HTTPBasicAuth
import datetime
import vobject

def main():
	user = ""
	passw = ""
    today = datetime.date.today() - datetime.timedelta(hours=12)
    tomorrow = today + datetime.timedelta(days=1)
    client = caldav.DAVClient('https://caldav.fastmail.com/dav/principals/user/ben@bensobel.org/', username=user, password=passw)
    try:
        principal = client.principal()
    except Exception as e:
        print(e)

    calendars = principal.calendars()

    for c in calendars:
    	events = c.date_search(today, tomorrow)
    	for e in events:
    		schedule = Calendar.from_ical(e.data).subcomponents
    		for thing in schedule:
    			start = thing.decoded('dtstart')
    			end = thing.decoded('dtend')
    			summary = thing['summary']
    			loc = thing['location']
    			print "{}-{}: {} ({})".format(, , summary, loc)


main()