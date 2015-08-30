#!/usr/bin/env python
# -- coding: utf-8 --
import json
import urllib2
import webapp2
import datetime

def parse_json(url):
    request = urllib2.urlopen(url)
    
    #encoding = request.headers['content-type'].split('charset=')[-1]
    #ucontent = unicode(content, encoding)
    
    # load the object from a string
    json_obj = json.loads(request.read())
    bolero_menus = json_obj["MenusForDays"]
    menu_string = ""
    
    for menu in bolero_menus:
        date = datetime.datetime.strptime(menu["Date"],'%Y-%m-%dT%H:%M:%S')
        menu_string += "{0}\n\n".format(date.strftime('%A %d.%m.'))
        
        for index, lunch in enumerate(menu["SetMenus"]):
            if lunch["Name"] != None:
                menu_string += "%s\n" % lunch["Name"]
            for component in  lunch["Components"]:
                menu_string += "%s\n" % component
            menu_string += "%s\n\n" % lunch["Price"]

    return menu_string

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        self.response.write('Menus for this week:\n{1}'.format(today, bolero.encode('utf-8')))


today = datetime.date.isoformat(datetime.date.today())
bolero = parse_json('http://www.amica.fi/modules/json/json/Index?costNumber=3121&firstDay=2015-08-25&language=fi')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
