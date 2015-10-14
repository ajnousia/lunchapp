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

USER_RESTAURANTS = None
USE_DEVELOPMENT_DATA = False

def create_dictionary_with_user_loginURL_and_logoutURL(handler):
    user = users.get_current_user()
    return_dict = {
        "user" : user,
        "login_url" : users.create_login_url(handler.request.uri),
        "logout_url" : users.create_logout_url(handler.request.uri)}
    return return_dict

def get_template_values_for_MainPage():
    template_values = {}
    user = users.get_current_user()
    restaurants = get_restaurants_data()
    if user:
        try:
            template_values["restaurants"] = get_user_restaurants(user).restaurants
        except AttributeError:
            template_values["restaurants"] = restaurants.restaurants
    else:
        template_values["restaurants"] = restaurants.restaurants
    return template_values

def get_restaurants_data():
    if is_uptodate_data_available_in_memory():
        return get_restaurant_data_from_memory()
    else:
        return refresh_and_get_restaurants_data_using_datastore()

def is_uptodate_data_available_in_memory():
    restaurants = fetch_latest_week_restaurants()
    if len(restaurants) == 0:
        return False
    current_week_number = datetime.date.today().isocalendar()[1]
    if restaurants[0].week_number == current_week_number:
        return True
    else:
        return False

def get_restaurant_data_from_memory():
    restaurants = fetch_latest_week_restaurants()
    return restaurants[0].pickled_restaurants

def fetch_latest_week_restaurants():
    parent_datastore_key = ndb.Key("Datastore", "Pickled_restaurants_objects")
    restaurants_query = PickledRestaurants.query(ancestor=parent_datastore_key).order(-PickledRestaurants.week_number)
    return restaurants_query.fetch(1)




class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        template_values = create_dictionary_with_user_loginURL_and_logoutURL(self).copy()
        template_values.update(get_template_values_for_MainPage())
        template = JINJA_ENVIRONMENT.get_template('tab_content.html')
        self.response.write(template.render(template_values))


class AboutPage(webapp2.RequestHandler):

    def get(self):
        template_values = create_dictionary_with_user_loginURL_and_logoutURL(self)
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render(template_values))


class SettingsPage(webapp2.RequestHandler):

    def get(self):
        if users.get_current_user() != None:
            template_values = create_dictionary_with_user_loginURL_and_logoutURL(self)
            restaurants = get_restaurants_data()
            template_values["restaurant_names"] = restaurants.get_restaurant_names()
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
            restaurants = get_restaurants_data()
            entity = UserPrefs.query(UserPrefs.user==user).get()
            restaurant_obj = restaurants.get_restaurant_by_name(restaurant_name)
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
    (r'/about', AboutPage)],
    debug=True)


# Kun depolyaat appengineen:
# 1. Vaihda USE_DEVELOPMENT_DATA = False
# 2. Vaihda debug=False
