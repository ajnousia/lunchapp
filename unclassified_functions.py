import datetime
import os
import lunchapp
import logging
from parsefunctions import *
from data_store_classes import *
from google.appengine.api import taskqueue




def fetch_restaurants_data():
    today = datetime.date.today()
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    restaurants = Restaurants()

    bolero = Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"))
    atomitie5 = Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"))
    picante = Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"))

    parent_datastore_key_for_ancestor_query = ndb.Key("Datastore", "Server properties")
    fetch_error = FetchError.get_or_insert("Fetch error", parent = parent_datastore_key_for_ancestor_query, was_error = False)
    fetch_error.was_error = False

    try:
        restaurants = add_restaurant_data(restaurants, bolero, parse_bolero_json, last_monday)
    except Exception:
        fetch_error.was_error = True
        pass
    try:
        restaurants = add_restaurant_data(restaurants, atomitie5, parse_atomitie5_json, last_monday)
    except Exception:
        fetch_error.was_error = True
        pass
    try:
        restaurants = add_restaurant_data(restaurants, picante, parse_picante_html)
    except Exception:
        fetch_error.was_error = True
        pass

    # sellon_ravintolat = ["marian-konditoria", "ravintola-base", "cafe-buffo", "ravintola-retro", "rax-buffet", "glo-grill-kitchen", "chicos"]
    # for name in sellon_ravintolat:
    #     sellon_ravintola = Restaurant(name.replace("-"," ").replace("ravintola","").strip().title(), None)
    #     restaurants = add_restaurant_data(restaurants, sellon_ravintola, parse_sello_html, name, last_monday)

    fetch_error.put()
    return restaurants

def add_restaurant_data(restaurants, restaurant, parse_function, *args):
    try:
        menus = parse_function(*args)
        if len(menus) == 0:
            raise
    except:
        raise
    for menu in menus:
        restaurant.add_day_menu(menu)
    restaurants.add_restaurant(restaurant)
    return restaurants

def refresh_and_get_restaurants_data_using_datastore():
    current_week_number = datetime.date.today().isocalendar()[1]
    restaurants_object = fetch_restaurants_data()
    if restaurants_object is None:
        raise TypeError('Restaurants object was expected. Got None instead.')
    fetch_error = FetchError.query().get()
    if fetch_error.was_error == True:
        task = taskqueue.Task(url="/worker", countdown=7200)
        task.add()
    parent_key = ndb.Key("Parent", "Restaurants")
    restaurants = PickledRestaurants.query(ancestor=parent_key).filter(PickledRestaurants.week_number == current_week_number).get()
    if restaurants is None:
        restaurants = PickledRestaurants(parent=parent_key, pickled_restaurants=restaurants_object, week_number=current_week_number)
    else:
        restaurants.pickled_restaurants = restaurants_object
    restaurants.put()
    return restaurants_object
