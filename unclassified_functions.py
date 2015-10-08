import datetime
import os
import lunchapp
from parsefunctions import *


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
