import datetime
import os
import lunchapp
import logging
from parsefunctions import *
from data_store_classes import *


def fetch_restaurants_data():
    today = datetime.date.today()
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    restaurants = Restaurants()

    bolero = Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"))
    restaurants = add_restaurant_data(restaurants, bolero, parse_bolero_json, last_monday)

    atomitie5 = Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"))
    restaurants = add_restaurant_data(restaurants, atomitie5, parse_atomitie5_json, last_monday)

    picante = Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"))
    restaurants = add_restaurant_data(restaurants, picante, parse_picante_html)

    sellon_ravintolat = ["marian-konditoria", "ravintola-base", "cafe-buffo", "ravintola-retro", "rax-buffet", "glo-grill-kitchen", "chicos"]
    for name in sellon_ravintolat:
        sellon_ravintola = Restaurant(name.replace("-"," ").replace("ravintola","").strip().title(), None)
        restaurants = add_restaurant_data(restaurants, sellon_ravintola, parse_sello_html, name, last_monday)
    return restaurants

def add_restaurant_data(restaurants, restaurant, parse_function, *args):
    try:
        for menu in parse_function(*args):
            restaurant.add_day_menu(menu)
        restaurants.add_restaurant(restaurant)
    except Exception as error:
        logging.error('There was an error parsing restaurant data: %s' % error)
        pass
    return restaurants

def refresh_and_get_restaurants_data_using_datastore():
    current_week_number = datetime.date.today().isocalendar()[1]
    restaurants_object = fetch_restaurants_data()
    parent_datastore_key = ndb.Key("Datastore", "Pickled_restaurants_objects")
    restaurants = PickledRestaurants(parent=parent_datastore_key, pickled_restaurants=restaurants_object, week_number=current_week_number)
    restaurants.put()
    return restaurants_object
