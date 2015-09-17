#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
import jinja2
import datetime
import os
import urllib
import pickle

from parsefunctions import *
from classes import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

USE_DEVELOPMENT_DATA = True
LATEST_DATA_FETCH_DATE = None
RESTAURANTS = None 

def refresh_restaurants_data(restaurants):
    current_date = datetime.date.today()
    if USE_DEVELOPMENT_DATA == True:
        path = os.path.join(os.path.dirname(__file__), 'static_files/dummy_restaurant_data.pkl')
        pkl_file = open(path, "rb")
        restaurants = pickle.load(pkl_file)
        pkl_file.close()
        return restaurants
    if LATEST_DATA_FETCH_DATE is None or LATEST_DATA_FETCH_DATE != current_date:
        restaurants = fetch_restaurants_data()
        return restaurants
    else:
        return restaurants

def fetch_restaurants_data():
    today = datetime.date.today()
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)

    restaurants = Restaurants()

    bolero = Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"))
    for menu in parse_bolero_json(last_monday):
        bolero.add_day_menu(menu)

    atomitie5 = Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"))
    for menu in parse_atomitie5_json(last_monday):
        atomitie5.add_day_menu(menu)

    picante = Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"))
    for menu in parse_picante_html():
        picante.add_day_menu(menu)

    restaurants.add_restaurant(bolero)
    restaurants.add_restaurant(atomitie5)
    restaurants.add_restaurant(picante)
    
    LATEST_DATA_FETCH_DATE = today
    
    return restaurants
    
    # TODO sometimes HTTPException is raised 
    

class MainPage(webapp2.RequestHandler):

    def get(self):
    
        self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
        today = datetime.date.today()
        
        restaurants = refresh_restaurants_data(RESTAURANTS)
        
        template_values = {
            "restaurants": restaurants.restaurants
        }

        template = JINJA_ENVIRONMENT.get_template('template.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ], debug=True)
