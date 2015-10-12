#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
import jinja2
import datetime
import os
import urllib
import pickle
import logging
from google.appengine.api import users
from google.appengine.ext import ndb

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
VISIBLE_RESTAURANTS = []
VISIBLE_RESTAURANT_NAMES = []
RELOAD_RESTAURANTS = True
USE_DEVELOPMENT_DATA = False

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
        if len(VISIBLE_RESTAURANT_NAMES) > 0:
            logging.debug(VISIBLE_RESTAURANT_NAMES[0])
        restaurants = refresh_restaurants_data(RESTAURANTS)
        restaurants = refresh_restaurants_data_using_datastore(RESTAURANTS, users.get_current_user())
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
            template_values["users_restaurants"] = VISIBLE_RESTAURANT_NAMES
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            template = JINJA_ENVIRONMENT.get_template('settings.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        restaurant_name = self.request.get('restaurant_name').strip(' \t\n\r')
        type = self.request.get('type')
        global VISIBLE_RESTAURANT_NAMES
        user = users.get_current_user()

        query = ndb.gql("SELECT * FROM UserPrefs WHERE user = :1", user)
        results = query.fetch(2)
        if len(results) > 1:
            logging.error("more than one UserPrefs object for user %s", str(user))
        elif len(results) == 0:
            logging.debug("creating UserPrefs object for user %s", str(user))
            VISIBLE_RESTAURANT_NAMES = [restaurant_name]
            userprefs = UserPrefs(user=user, restaurants=[RestaurantEntity(name=restaurant_name)])
            userprefs.put()
        else:
            entity = UserPrefs.query(UserPrefs.user==user).get()
            if type == "add":
                VISIBLE_RESTAURANT_NAMES.append(restaurant_name)
            else:
                VISIBLE_RESTAURANT_NAMES.remove(restaurant_name)
            updated_restaurant_entities = []
            for name in VISIBLE_RESTAURANT_NAMES:
                updated_restaurant_entities.append(RestaurantEntity(name=name))
            entity.restaurants = updated_restaurant_entities
            entity.put()

        logging.debug(VISIBLE_RESTAURANT_NAMES[0])


logging.getLogger().setLevel(logging.DEBUG)
app = webapp2.WSGIApplication([
    ('/', MainPage),
    (r'/settings', SettingsPage),
    (r'/about', AboutPage),
    ], debug=True)


# Kun depolyaat appengineen:
# 1. Vaihda USE_DEVELOPMENT_DATA = False
# 2. Vaihda debug=False
