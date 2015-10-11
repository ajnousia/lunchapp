#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
import jinja2
import datetime
import os
import urllib
import pickle
from google.appengine.api import users

from unclassified_functions import *
from classes import *



# Kun depolyaat appengineen:
# 1. Vaihda USE_DEVELOPMENT_DATA = False
# 2. Vaihda debug=False



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
LATEST_DATA_FETCH_DATE = None
RESTAURANTS = None
USE_DEVELOPMENT_DATA = True

def create_dictionary(handler):
    user = users.get_current_user()
    values = {}
    values["login_url"] = users.create_login_url(handler.request.uri)
    values["user"] = user
    values["logout_url"] = users.create_logout_url(handler.request.uri)
    return values

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        template_values = create_dictionary(self)
        restaurants = refresh_restaurants_data(RESTAURANTS)
        template_values["restaurants"] = restaurants.restaurants
        template = JINJA_ENVIRONMENT.get_template('tab_content.html')
        self.response.write(template.render(template_values))


class AboutPage(webapp2.RequestHandler):

    def get(self):
        template_values = create_dictionary(self)
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render(template_values))


class SettingsPage(webapp2.RequestHandler):

    def get(self):
        if users.get_current_user() != None:
            template_values = create_dictionary(self)
            restaurants = refresh_restaurants_data(RESTAURANTS)
            template_values["restaurants"] = restaurants.restaurants
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            template = JINJA_ENVIRONMENT.get_template('settings.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    (r'/settings', SettingsPage),
    (r'/about', AboutPage),
    ], debug=True)


# Kun depolyaat appengineen:
# 1. Vaihda USE_DEVELOPMENT_DATA = False
# 2. Vaihda debug=False
