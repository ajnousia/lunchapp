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


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
LATEST_DATA_FETCH_DATE = None
RESTAURANTS = None
USE_DEVELOPMENT_DATA = True


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

        template_values = {}
        user = users.get_current_user()
        template_values["login_url"] = users.create_login_url(self.request.uri)

        asdf

        if user:
            pass
        else:
            pass

        template_values["user"] = user

        restaurants = refresh_restaurants_data(RESTAURANTS)

        template_values["restaurants"] = restaurants.restaurants

        template = JINJA_ENVIRONMENT.get_template('tab_content.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ], debug=True)
