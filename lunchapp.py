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
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
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
               Restaurant("Atomitie 5", "Atomitie 5 00370 Helsinki", parse_atomitie5_json(last_monday)),
               Restaurant("Picante", "Valimotie 8 00380 Helsinki", parse_picante_html())]

        template_values = {
            "restaurants": restaurants,
            "today": today
        }

        template = JINJA_ENVIRONMENT.get_template('template.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ], debug=False)
