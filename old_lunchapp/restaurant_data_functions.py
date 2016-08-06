import logging
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from data_store_classes import PickledRestaurants, FetchError
from parsefunctions import *
from restaurant_classes import Restaurants, Restaurant, Address

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

def refresh_and_get_restaurants_data_using_datastore():
    current_week_number = datetime.date.today().isocalendar()[1]
    restaurants_object = fetch_restaurants_data()
    if restaurants_object is None:
        raise TypeError('Restaurants object was expected. Got None instead.')
    fetch_error = FetchError.query().get()
    if fetch_error.was_error == True:
        create_new_fetch_task(fetch_error)
    parent_key = ndb.Key("Parent", "Restaurants")
    restaurants = PickledRestaurants.query(ancestor=parent_key).filter(PickledRestaurants.week_number == current_week_number).get()
    if restaurants is None:
        restaurants = PickledRestaurants(parent=parent_key, pickled_restaurants=restaurants_object, week_number=current_week_number)
    else:
        restaurants.pickled_restaurants = restaurants_object
    restaurants.put()
    return restaurants_object

def fetch_restaurants_data():
    today = datetime.date.today()
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
    restaurants = Restaurants()

    bolero = Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"))
    atomitie5 = Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"))
    picante = Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"))

    parent_datastore_key_for_ancestor_query = ndb.Key("Datastore", "Server properties")
    fetch_error = FetchError.get_or_insert("Fetch error", parent = parent_datastore_key_for_ancestor_query, was_error = False, task_queue_id = 0)
    fetch_error.was_error = False

    try:
        restaurants = add_restaurant_data(restaurants, bolero, parse_bolero_json, last_monday)
    except Exception, e:
        print str(e)
        fetch_error.was_error = True
        pass
    try:
        restaurants = add_restaurant_data(restaurants, atomitie5, parse_atomitie5_json, last_monday)
    except Exception, e:
        print str(e)
        fetch_error.was_error = True
        pass
    try:
        restaurants = add_restaurant_data(restaurants, picante, parse_picante_html)
    except Exception, e:
        print str(e)
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

def create_new_fetch_task(fetch_error):
    try:
        task_name = "new_fetch_" + str(fetch_error.task_queue_id)
        task = taskqueue.Task(name=task_name, url="/worker", countdown=7200)
        task.add()
    except taskqueue.TombstonedTaskError:
        fetch_error.task_queue_id += 1
        fetch_error.put()
        create_new_fetch_task(fetch_error)
    except Exception as e:
        print type(e)
