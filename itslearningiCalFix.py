#!/usr/bin/env python
import urllib.request

import tornado.ioloop
import tornado.web
import tornado.options

from urllib.request import HTTPError, URLError

from tornado.escape import json_encode

from icalendar import Calendar


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """The http GET function"""
        if self.request.uri == "/":
            self.redirect("calendar.ical")
            return
        
        calendarURL = self.get_argument("url", None, True)
        if calendarURL == None:
            self.write("No url provided")
            return

        # Try to download the provided url
        try:
            ical = urllib.request.urlopen(calendarURL.replace("webcal", "http")).read()
        except ValueError as err:
            self.returnError(str(err))
            return

        except HTTPError as err:
            self.returnError(str(err), err.getcode())
            return

        except URLError as err:
            self.returnError(str(err))
            return

        # Try to parse the ical
        try:
            cal = Calendar.from_ical(ical)
        except ValueError as err:
            self.returnError("Not a valid iCalendar file")
            return

        for item in cal.walk('vevent'):
            # Switch SUMMARY and DESCRIPTION to make the calendar usable
            summary = item['SUMMARY']
            item['SUMMARY'] = item['DESCRIPTION']
            item['DESCRIPTION'] = item['DESCRIPTION'] + "\n" + summary

        # Return the "New" iCalendar file
        self.set_header("Content-Type", 'text/calendar; charset="utf-8"')
        self.write(cal.to_ical())

    def returnError(self, err_msg, err_code=400):
        """Return error in json format for easy debugging"""
        res = {
            'success' : 'false',
            'error' : err_msg,
        }
        self.set_status(err_code)
        self.write(json_encode(res)+ "\n")


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/calendar.ical", MainHandler),
])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.xheaders = True
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

