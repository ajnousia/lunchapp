#!/usr/bin/env python
# -- coding: utf-8 --
import os
import webapp2
import jinja2

from google.appengine.ext import ndb

from restaurant_classes import Restaurants
from data_store_classes import UserPreferences
from user_functions import *
from restaurant_data_functions import get_restaurants_data

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
