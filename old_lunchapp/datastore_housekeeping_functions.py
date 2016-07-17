import datetime
import lunchapp
import logging
import data_store_classes
import pickle

from google.appengine.ext import ndb


def backup_PickledRestaurants_entities_locally(batch_size):
    pickled_restaurants = data_store_classes.PickledRestaurants.query().fetch(batch_size)
    file_name = "PickledRestaurants_backup_" + datetime.date.today().isoformat() + ".pkl"
    with open(file_name, "wb") as output:
        pickle.dump(pickled_restaurants, output, -1)

def update_datastore_entities_without_dates():
    entities = get_entities_without_date(data_store_classes.PickledRestaurants, 50)
    updated_entities = get_updated_entites_with_added_dates(entities)
    try:
        ndb.put_multi(updated_entities)
    except Exception as e:
        print(e)

def get_entities_without_date(DatastoreClass, batch_size):
    entities = DatastoreClass.query().fetch(batch_size)
    entities_without_date = []
    for entity in entities:
        if entity.date == None:
            entities_without_date.append(entity)
    return entities_without_date

def get_updated_entites_with_added_dates(entities):
    updated_entities = []
    year = 2015
    for entity in entities:
        updated_entities.append(add_date_from_year_and_weeknumber(entity, year, entity.week_number))
    return updated_entities

def add_date_from_year_and_weeknumber(entity, year, week_number):
    entity.date = get_monday_date_from_weeknumber(year, week_number)
    return entity

def get_monday_date_from_weeknumber(year, week_number):
    first_day_of_year = datetime.date(year, 1, 1)
    second_week_first_day = first_day_of_year
    while second_week_first_day.isocalendar()[1] != 2:
        second_week_first_day += datetime.timedelta(days=1)
    return second_week_first_day + datetime.timedelta(weeks=week_number-2)
