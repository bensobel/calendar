import requests
import datetime
import dateutil
import dateutil.relativedelta
import dateutil.parser
import time

WIDENER_ID = '1567'

def get_lib_hours(today,lib_id=WIDENER_ID):
	start_day = today - dateutil.relativedelta.relativedelta(weekday=6, weeks=1)



	#start day must be sunday
	 

	#end day must be saturay
	end_day = today + dateutil.relativedelta.relativedelta(weekday=5)



	if start_day > end_day:
		end_day += dateutil.relativedelta.relativedelta(weeks=1)

	start_formatted = time.strftime('%Y-%m-%d',start_day.timetuple())

	end_formatted = time.strftime('%Y-%m-%d',end_day.timetuple())

	today_formatted = time.strftime('%Y-%m-%d',today.timetuple())

	URL='http://library.harvard.edu/opening_hours/instances?from_date={0}&to_date={1}&nid={2}'.format(start_formatted,end_formatted,lib_id)

	r = requests.get(URL)

	json = r.json()

	#find today in the json. if no today, then wid is closed

	closed = True

	for day in json:
		if day['date'] == today_formatted:
			hours = "{0}-{1}".format(day['start_time'], day['end_time'])
			closed = False

	if closed:
		hours = "Closed"

	print "Widener hours: {0}".format(hours)

