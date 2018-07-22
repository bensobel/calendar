import datetime
import time
import dateutil
import dateutil.parser
import dateutil.tz

s = '2017-05-24T19:30:00-07:00'
s_ = '2017-05-24'

LOCAL_TZ = dateutil.tz.tzlocal()


def dt_parse(t):
    ret = time.strptime(t[0:19],'%Y-%m-%dT%H:%M:%S')

    dt = datetime.datetime.fromtimestamp(time.mktime(ret))
    if t[19]=='+':
        offset=datetime.timedelta(hours=int(t[20:22]),minutes=int(t[23:]))
    elif t[19]=='-':
    	offset=datetime.timedelta(hours=int(t[20:22]),minutes=int(t[23:]))
    else:
    	offset = datetime.timedelta(hours=0,minutes=0)
    return dt+offset

dt = dateutil.parser.parse(s)

now = datetime.datetime.now(dateutil.tz.tzlocal())
#print dt.timetuple()


print time.strftime('%I:%M%p',now.astimezone(LOCAL_TZ).timetuple())