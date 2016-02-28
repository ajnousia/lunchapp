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
