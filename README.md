itslearningiCalFix
======================
Fixing itslearning iCalendars, one event at a time.
The itslearning iCalendars are made with a event SUMMARY
containing the name of the calendar, and not the title.
This make all events look the same, and therefore the calendar
is useless.

This simple webserver fixes the provided calendar, and returns
a new and way better one!

Usage
======================
Start server:

     python itslearningiCalFix.py

API for Fixing calendar:

     http://host:8888/calendar.ical?url=yoururl

Replace "yoururl" with the url to the ical calendar.

PS: To make it work; remember to encode the url.


Requirements
======================
[Python](https://www.python.org/), [Tornado](https://pypi.python.org/pypi/tornado) and [iCalendar](https://pypi.python.org/pypi/icalendar)

License
======================
See LICENSE.md
