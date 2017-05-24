# Calendar Printer

Project for Raspberry Pi daily calendar printing, based on Google's Quickstart code for the GCal API and Python. Uses Adafruit's thermal printer library for Python (included in repo).

**To-do:**

* Pull out event-getting in main() and make into separate functions that are invoked in main()
* Install dateutil library (https://dateutil.readthedocs.io/en/latest/)
* Set cron job to update dateutil time zone database monthly (run updatezinfo.py script)
* Process all times as tz-aware datetime timestamps; don't roll your own parser. Then convert to easter right when it's time to print.
* ~~Something's weird with the weather API; make sure it's getting the right forecast data.~~ (Edit: looks like it is; I guess it's just a narrow forecast.)



© 2017 Ben Sobel (insofar as any copyright subsists in this code)