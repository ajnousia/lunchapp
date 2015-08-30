#!/usr/bin/env python
# -- coding: utf-8 --
import json
import urllib2
import webapp2
import datetime
#import dateutil.parser

today = datetime.date.isoformat(datetime.date.today())
bolero_json = 'http://www.amica.fi/modules/json/json/Index?costNumber=3121&firstDay=2015-08-25&language=fi'
mystr = urllib2.urlopen(bolero_json)


def parse_json(url):
    # load the object from a string
    json_obj = json.loads(urllib2.urlopen(url))
    bolero_menus = json_obj["MenusForDays"]
    menu_string = ""
    
    for menu in bolero_menus:
        #date = dateutil.parser.parse(menu["Date"]).date()
        #menu_string += "{0}.{1}.{2}\n".format(date.day, date.month, date.year)
        for index, lunch in enumerate(menu["SetMenus"]):
            menu_string += "Menu %s\n" % str(index)
            for component in  lunch["Components"]:
                menu_string += "%s\n" % component



class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World! It is {0}\nMenus for this week:\n{1}'.format(today, unicode(mystr).encode('utf8')))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
