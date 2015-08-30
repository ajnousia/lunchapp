#!/usr/bin/env python
# -- coding: utf-8 --
import json
import urllib2
import webapp2
import datetime
from HTMLParser import HTMLParser


HTML_HEADER = """<!DOCTYPE html>
<html>
<link rel="stylesheet" href="/bootstrap/css/bootstrap.css">
<link rel="stylesheet" href="/bootstrap/css/bootstrap-responsive.css">
<link rel="stylesheet" href="/stylesheets/style.css">
<script src="js/jquery.js"></script>
<script src="js/bootstrap.min.js"></script>
  <body>
    <div class="navbar navbar-default navbar-static-top">
    <div class="container">
      <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="#">Bootstrap</a>
      </div>
      <div class="collapse navbar-collapse">
        <ul class="nav navbar-nav navbar-right">
          <li class="active"><a href="#">Home</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </div><!--/.nav-collapse -->
    </div>
  </div>"""

HTML_FOOTER = "</body></html>"

class Restaurant:
    def __init__(self, name, address, weeks_menus):
        self.name = name
        self.address = address
        self.weeks_menus = weeks_menus


def get_json(url):
    request = urllib2.urlopen(url)
    return json.loads(request.read())

def parse_bolero_json(start_date):
    json_string = get_json('http://www.amica.fi/modules/json/json/Index?costNumber=3121&firstDay={0}&language=fi'.format(datetime.date.isoformat(start_date)))
    menus = json_string["MenusForDays"]
    weeks_menus = []
    for menu in menus:
        #date = datetime.datetime.strptime(menu["Date"],'%Y-%m-%dT%H:%M:%S')
        #menu_string += "<h1>{0}</h1>".format(date.strftime('%A %d.%m.'))
        new_lunch = []
        for lunch in menu["SetMenus"]:
            courses = []
            for component in lunch["Components"]:
                new_component = {}
                new_component["Food"] = component[0:component.find('(')-1]
                new_component["Types"] = component[component.find('(')+1:-1].strip().split(',')
                courses.append(new_component)
            new_lunch.append({"Courses": courses, "Price": lunch["Price"]})
        weeks_menus.append(new_lunch)

    return weeks_menus


def parse_atomitie5_json(start_date):
    weeks_menus = []
    for i in range(0,7):
        date = start_date + datetime.timedelta(i)
        json_string = get_json('http://www.sodexo.fi/ruokalistat/output/daily_json/9/{0}/{1}/{2}/fi'.format(str(date.year), str(date.strftime('%m')), str(date.strftime('%d'))))
        new_lunch = []
        for lunch in json_string["courses"]:
            courses = []
            new_component = {}
            new_component["Food"] = lunch["title_fi"]
            new_component["Types"] = lunch["properties"].split(',')
            courses.append(new_component)
            new_lunch.append({"Courses": courses, "Price": lunch["price"]})
        weeks_menus.append(new_lunch)
    return weeks_menus

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        self.response.write(HTML_HEADER)
        today = datetime.date.today()
        last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)

        restaurants = [Restaurant("Bolero", "Atomitie 2 c 00370 Helsinki", parse_bolero_json(last_monday)),
               Restaurant("Atomitie 5", "Atomitie 5 00370 Helsinki", parse_atomitie5_json(last_monday))]
        
        self.response.write("""<div class="menu_container"><div class="row">""")
        
        for restaurant in restaurants:
            self.response.write("""<div class="col-md-4">""")
            self.response.write("<h1>" + restaurant.name + "</h1>")
            
            for course in restaurant.weeks_menus[today.weekday()-3]:
                #self.response.write("<p><i>" +' '.join(course["Courses"]["Food"]) + "</i><br></p>")
                for component in course["Courses"]:
                    self.response.write("<p>" + component["Food"] + " <i>" +' '.join(component["Types"]) + "</i><br></p>")
                self.response.write("<p>" + course["Price"]+ "<br><br></p>")
            self.response.write("</div>")
        self.response.write("</div></div>")

        self.response.write(HTML_FOOTER)


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
