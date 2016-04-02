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
from restaurants_classes import *


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/jinja')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_RESTAURANT_NAMES = ["Bolero", "Atomitie 5", "Picante"]


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        template_values = create_dictionary_with_user_loginURL_and_logoutURL(self).copy()
        template_values.update(self.get_template_values_for_MainPage())
        template = JINJA_ENVIRONMENT.get_template('tab_content.html')
        self.response.write(template.render(template_values))

    def get_template_values_for_MainPage(self):
        template_values = {}
        user = get_user()
        restaurants = get_restaurants_data()
        if user:
            try:
                user_restaurants = get_user_restaurant_names(user)
                template_values["restaurants"] = self.get_restaurants_object_from_names(user_restaurants).restaurants
            except AttributeError:
                template_values["restaurants"] = restaurants.restaurants
        else:
            template_values["restaurants"] = self.get_restaurants_object_from_names(DEFAULT_RESTAURANT_NAMES).restaurants
        return template_values

    def get_restaurants_object_from_names(self, name_list):
        restaurants = get_restaurants_data()
        return_restaurants = Restaurants()
        for name in name_list:
            try:
                return_restaurants.add_restaurant(restaurants.get_restaurant_by_name(name))
            except Exception:
                pass
        return return_restaurants


class AboutPage(webapp2.RequestHandler):

    def get(self):
        template_values = create_dictionary_with_user_loginURL_and_logoutURL(self)
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        template = JINJA_ENVIRONMENT.get_template('about.html')
        self.response.write(template.render(template_values))


class SettingsPage(webapp2.RequestHandler):

    def get(self):
        user = get_user()
        if user != False:
            template_values = create_dictionary_with_user_loginURL_and_logoutURL(self)
            restaurants = get_restaurants_data()
            template_values["restaurant_names"] = restaurants.get_restaurant_names()
            template_values["user_restaurant_names"] = get_user_restaurant_names(user)
            self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
            template = JINJA_ENVIRONMENT.get_template('settings.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        restaurant_name = self.request.get('restaurant_name').strip(' \t\n\r')
        list_operation = self.request.get('type')
        user = get_user()
        user_preferences = UserPreferences.query(UserPreferences.user_id==user.user_id()).get()
        user_restaurants = get_user_restaurant_names(user)
        if list_operation == "add":
            user_restaurants.append(restaurant_name)
        else: # "remove"
            user_restaurants.remove(restaurant_name)
        user_preferences.restaurants = user_restaurants
        user_preferences.put()


class FetchData(webapp2.RequestHandler):

    def post(self):
        refresh_and_get_restaurants_data_using_datastore()


def get_user():
    user = users.get_current_user()
    parent_key = ndb.Key("Datastore", "Accounts")
    if user:
        accounts_query = Account.query(ancestor=parent_key).filter(Account.user_id == user.user_id())
        accounts = accounts_query.fetch(2)
        if len(accounts) > 1:
            print "Duplicate user. This shouldn't happen..."
        if len(accounts) > 0:
            return user
        else:
            account = Account(parent = parent_key, user_email = user.email(), user_id = user.user_id())
            account.put()
            return user
    else:
        return False

def create_dictionary_with_user_loginURL_and_logoutURL(handler):
    user = get_user()
    return_dict = {
        "user" : user,
        "login_url" : users.create_login_url(handler.request.uri),
        "logout_url" : users.create_logout_url(handler.request.uri)}
    return return_dict

def get_user_restaurant_names(user):
    restaurants = get_restaurants_data().restaurants
    user_id = user.user_id()
    if has_user_preferences(user_id):
        user_preferences = UserPreferences.query(UserPreferences.user_id == user_id).get()
        return user_preferences.restaurants
    else:
        restaurants_list = DEFAULT_RESTAURANT_NAMES
        user_preferences = UserPreferences(user_id = user_id, restaurants = restaurants_list)
        user_preferences.put()
        return restaurants_list

def has_user_preferences(user_id):
    if UserPreferences.query(UserPreferences.user_id == user_id).get() is None:
        return False
    else:
        return True

def get_restaurants_data():
    if is_uptodate_data_available_in_memory():
        return get_latest_restaurant_datastore_entity().pickled_restaurants
    else:
        return refresh_and_get_restaurants_data_using_datastore()

def is_uptodate_data_available_in_memory():
    try:
        restaurants_datastore_entity = get_latest_restaurant_datastore_entity()
    except IndexError:
        return False
    fetch_error = FetchError.query().get()
    if fetch_error is None:
        return False
    if fetch_error.was_error == True:
        return False
    current_week_number = datetime.date.today().isocalendar()[1]
    if restaurants_datastore_entity.week_number == current_week_number:
        return True
    else:
        return False

def get_latest_restaurant_datastore_entity():
    batch_size = 1
    restaurant_entities = get_latest_week_restaurants_query().fetch(batch_size)
    try:
        restaurants_datastore_entity = restaurant_entities[0]
        return restaurants_datastore_entity
    except IndexError:
        print "No restaurants data in Datastore"
        raise IndexError

def get_latest_week_restaurants_query():
    qry = PickledRestaurants.query(ancestor=ndb.Key("Parent", "Restaurants"))
    qry = qry.order(-PickledRestaurants.date)
    return qry
