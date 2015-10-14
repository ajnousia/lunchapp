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
USER_RESTAURANTS = None
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
        user = users.get_current_user()
        if RESTAURANTS == None:
            refresh_restaurants_data_using_datastore()
        if user:
            try:
                template_values["restaurants"] = get_user_restaurants(user).restaurants
            except AttributeError:
                template_values["restaurants"] = RESTAURANTS.restaurants
        else:
            template_values["restaurants"] = RESTAURANTS.restaurants
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
            if RESTAURANTS == None:
                refresh_restaurants_data_using_datastore()
            template_values["restaurant_names"] = RESTAURANTS.get_restaurant_names()
            if USER_RESTAURANTS != None:
                template_values["user_restaurant_names"] = USER_RESTAURANTS.get_restaurant_names()
            else:
                template_values["user_restaurant_names"] = []
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            template = JINJA_ENVIRONMENT.get_template('settings.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        restaurant_name = self.request.get('restaurant_name').strip(' \t\n\r')
        list_operation = self.request.get('type')

        global USER_RESTAURANTS
        user = users.get_current_user()

        query = ndb.gql("SELECT * FROM UserPrefs WHERE user = :1", user)
        results = query.fetch(2)
        if len(results) > 1:
            logging.error("more than one UserPrefs object for user %s", str(user))
        elif len(results) == 0:
            logging.debug("creating UserPrefs object for user %s", str(user))
            userprefs = UserPrefs(user=user, restaurants=[RestaurantEntity(name=restaurant_name)])
            userprefs.put()
        else:
            entity = UserPrefs.query(UserPrefs.user==user).get()
            restaurant_obj = RESTAURANTS.get_restaurant_by_name(restaurant_name)
            if list_operation == "add":
                USER_RESTAURANTS.add_restaurant(restaurant_obj)
            else: # "remove"
                USER_RESTAURANTS.remove_restaurant(restaurant_obj)
            updated_restaurant_entities = []
            for name in USER_RESTAURANTS.get_restaurant_names():
                updated_restaurant_entities.append(RestaurantEntity(name=name))
            entity.restaurants = updated_restaurant_entities
            entity.put()



app = webapp2.WSGIApplication([
    ('/', MainPage),
    (r'/settings', SettingsPage),
    (r'/about', AboutPage),
    ], debug=True)


# Kun depolyaat appengineen:
# 1. Vaihda USE_DEVELOPMENT_DATA = False
# 2. Vaihda debug=False
