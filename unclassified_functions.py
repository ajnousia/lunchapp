import datetime
import os
import lunchapp
from parsefunctions import *
from data_store_classes import *

def refresh_restaurants_data(restaurants):
    current_date = datetime.date.today()

    if lunchapp.USE_DEVELOPMENT_DATA == True:
        path = os.path.join(os.path.dirname(__file__), 'static_files/dummy_restaurant_data.pkl')
        pkl_file = open(path, "rb")
        restaurants = pickle.load(pkl_file)
        pkl_file.close()
        return restaurants
    if lunchapp.LATEST_DATA_FETCH_DATE is None or lunchapp.LATEST_DATA_FETCH_DATE != current_date:
        restaurants = fetch_restaurants_data()
        return restaurants
    else:
        return restaurants

def fetch_restaurants_data():
    today = datetime.date.today()
    last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)

    restaurants = Restaurants()

    try:
        bolero = Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"))
        for menu in parse_bolero_json(last_monday):
            bolero.add_day_menu(menu)
        restaurants.add_restaurant(bolero)
    except Exception:
        pass

    try:
        atomitie5 = Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"))
        for menu in parse_atomitie5_json(last_monday):
            atomitie5.add_day_menu(menu)
        restaurants.add_restaurant(atomitie5)
    except Exception:
        pass

    try:
        picante = Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"))
        for menu in parse_picante_html():
            picante.add_day_menu(menu)
        restaurants.add_restaurant(picante)
    except Exception:
        pass

    lunchapp.LATEST_DATA_FETCH_DATE = today
    lunchapp.RESTAURANTS = restaurants

    return restaurants


def refresh_restaurants_data_using_datastore(restaurants, user):
    if lunchapp.USE_DEVELOPMENT_DATA == True:
        if restaurants == None:
            path = os.path.join(os.path.dirname(__file__), 'static_files/dummy_restaurant_data.pkl')
            pkl_file = open(path, "rb")
            restaurants = pickle.load(pkl_file)
            pkl_file.close()
    else:
        if lunchapp.LATEST_DATA_FETCH_DATE is None or lunchapp.LATEST_DATA_FETCH_DATE != current_date:
            restaurants = fetch_restaurants_data()

    if user != None:
        visible_restaurants = None
        if lunchapp.VISIBLE_RESTAURANT_NAMES == None:
            try:
                users_restaurants = UserEntity.query(UserEntity.user==user).get().restaurants
                for restaurant in restaurants:
                    for restaurant_entity in users_restaurants:
                        if restaurant.name == restaurant_entity.name:
                            visible_restaurants.append(restaurant)
            except AttributeError:
                return restaurants
        else:
            for restaurant in restaurants:
                if restaurant.name in lunchapp.VISIBLE_RESTAURANT_NAMES:
                    visible_restaurants.append(restaurant)

        lunchapp.VISIBLE_RESTAURANTS = visible_restaurants
        return visible_restaurants
    else:
        return restaurants



#   def add_restaurant_data_to_datastore():
#     today = datetime.date.today()
#     last_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)
#     try:
#         bolero = Restaurant("Bolero", Address("Atomitie", "2", "00370", "Helsinki"))
#         for menu in parse_bolero_json(last_monday):
#             bolero.add_day_menu(menu)
#         restaurants_to_datastore(bolero)
#     except Exception:
#         pass
#
#     try:
#         atomitie5 = Restaurant("Atomitie 5", Address("Atomitie", "5", "00370", "Helsinki"))
#         for menu in parse_atomitie5_json(last_monday):
#             atomitie5.add_day_menu(menu)
#         restaurants_to_datastore(atomitie5)
#     except Exception:
#         pass
#
#     try:
#         picante = Restaurant("Picante", Address("Valimotie", "8", "00380", "Helsinki"))
#         for menu in parse_picante_html():
#             picante.add_day_menu(menu)
#         restaurants_to_datastore(picante)
#     except Exception:
#         pass
#
#     lunchapp.LATEST_DATA_FETCH_DATE = today
#
# def restaurants_to_datastore(restaurant_obj):
#     for days_menu in restaurant_obj.menu_list:
#         for course in days_menu.courses:
#             for component in course.components:
#                 entity = ComponentEntity(restaurant_name=restaurant_obj.name,
#                                         date=days_menu.date,
#                                         course_name=course.name,
#                                         price=course.price,
#                                         component_name=component.name,
#                                         properties=component.properties)
#                 entity.put()
