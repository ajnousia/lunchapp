import datetime
import lunchapp
import logging
import data_store_classes
import pickle


def add_dates_to_datastore_entities():
    pass

def backup_PickledRestaurants_entities_locally(batch_size):
    pickled_restaurants = data_store_classes.PickledRestaurants.query().fetch(batch_size)
    file_name = "PickledRestaurants_backup_" + datetime.date.today().isoformat() + ".pkl"
    with open(file_name, "wb") as output:
        pickle.dump(pickled_restaurants, output, -1)

def get_entities_without_date(DatastoreClass, batch_size):
    return DatastoreClass.query(DatastoreClass.date == None).fetch(batch_size)

def update_entities(entities):
    pass

def get_monday_date_from_weeknumber(year, week_number):
    first_day_of_year = datetime.date(year, 1, 1)
    second_week_first_day = first_day_of_year
    while second_week_first_day.isocalendar()[1] != 2:
        second_week_first_day += datetime.timedelta(days=1)
    return second_week_first_day + datetime.timedelta(weeks=week_number-2)
