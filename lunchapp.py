#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
import jinja2
import datetime
import os
import urllib

from parsefunctions import *
from HTMLParser import HTMLParser


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Restaurant:
    def __init__(self, name, address, weeks_menus):
        self.name = name
        self.address = address
        self.weeks_menus = weeks_menus


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        today = datetime.date.today()
        last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)

        restaurants = [Restaurant("Bolero", "Atomitie 2 c 00370 Helsinki", parse_bolero_json(last_monday)),
               Restaurant("Atomitie 5", "Atomitie 5 00370 Helsinki", parse_atomitie5_json(last_monday))]

        template_values = {
            "restaurants": restaurants,
            "today": today
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

        # self.response.write("""<div class="container"><div class="row">""")
        #
        # for restaurant in restaurants:
        #     self.response.write("""<div class="col-md-4">
        #                                 <div class="panel panel-default">
        #                                     <div class="panel-heading">""")
        #     self.response.write("<h3>" + restaurant.name + "</h3></div>") #panel-heading
        #     self.response.write("""<div class="panel-body">""")
        #     for course in restaurant.weeks_menus[today.weekday()]:
        #         for component in course["Courses"]:
        #             self.response.write(component["Food"] + " <i>" +' '.join(component["Types"]) + "</i><br>")
        #         self.response.write(course["Price"]+ "<br><br>")
        #     self.response.write("</div>") #panel-body
        #     self.response.write("</div>") #panel
        #     self.response.write("</div>") #col
        # self.response.write("</div></div>") #menu-container, row



app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
