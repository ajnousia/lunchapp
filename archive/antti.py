# -- coding: utf-8 --
import datetime
import urllib
import pickle

from parsefunctions import *
from restaurant_classes import *

RESTAURANTS = None

def fetch_restaurants_data():
    today = datetime.date.today()
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)

    restaurants = Restaurants()

    '''print "Bolero"
    bolero = Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"))
    for menu in parse_bolero_json(last_monday):
        bolero.add_day_menu(menu)
        for course in menu.courses:
            print course.components[0].name.encode('utf-8'), course.price
'''
    print "A5"
    atomitie5 = Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"))
    for menu in parse_atomitie5_json(last_monday):
        atomitie5.add_day_menu(menu)
        for course in menu.courses:
            print course.components[0].name.encode('utf-8'), course.price

    print "picante"
    picante = Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"))
    for menu in parse_picante_html():
        picante.add_day_menu(menu)
        for course in menu.courses:
            print course.components[0].name.encode('utf-8'), course.price

    for i in range(5):
        #restaurants.add_restaurant(bolero)
        restaurants.add_restaurant(atomitie5)
        restaurants.add_restaurant(picante)


    return restaurants
    # HTTPException


def create_dymmy_restaurant_data():
    output = open("./static_files/dummy_restaurant_data.pkl", "wb")
    restaurants_data = fetch_restaurants_data()
    pickle.dump(restaurants_data, output)
    output.close()

#create_dymmy_restaurant_data()
fetch_restaurants_data()
