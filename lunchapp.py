#!/usr/bin/env python
# -- coding: utf-8 --
import json
import urllib2
import webapp2
import datetime

bootstrap = ["""<link rel="stylesheet" href="/bootstrap/css/bootstrap.css">""",
          """<link rel="stylesheet" href="/bootstrap/css/bootstrap-responsive.css">""",
          """<script src="bootstrap/js/jquery.js"></script>"""]
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
        menu_string += "<h1>{0}</h1>".format(date.strftime('%A %d.%m.'))
        
        for index, lunch in enumerate(menu["SetMenus"]):
            if lunch["Name"] != None:
                menu_string += "<h2>%s</h2><p>" % lunch["Name"]
            for component in  lunch["Components"]:
                menu_string += "%s<br>" % component
            menu_string += "<i>%s</i></p>" % lunch["Price"]

    return menu_string

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.out.write("<html>")
        for style in bootstrap:
            self.response.out.write(style)
        self.response.out.write("<body>")
        self.response.out.write("<html><body>")
        self.response.out.write('Menus for this week:\n{1}'.format(today, bolero.encode('utf-8')))
        self.response.out.write("</body></html>")


today = datetime.date.isoformat(datetime.date.today())
bolero = parse_json('http://www.amica.fi/modules/json/json/Index?costNumber=3121&firstDay=2015-08-25&language=fi')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
