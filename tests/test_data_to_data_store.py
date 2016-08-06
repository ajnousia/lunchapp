import unittest
import logging
import sys
import datetime
import pickle

import material_backend.material_app
from tests.test_datastore_housekeeping_functions import DataLoader
import material_backend.model as model
import material_backend.material_app as material_app

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestDataToDataStore(unittest.TestCase):

    def load_test_data(self):
        entities = DataLoader.load_pickled_entities("PickledRestaurants_backup_2016-07-17.pkl")
        weeks_menus = entities[0].pickled_restaurants.restaurants[0].menu_list
        return weeks_menus

    def print_DayMenu(self, menu):
        print menu.date
        for course in menu.courses:
            for component in course.components:
                print "\t" + component.name
                print "\t"*2 + component.get_properties_as_string()

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(app_id='e~lunchapp-1058', overwrite=True)
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        self.weeks_menus = self.load_test_data()
        material_app.update_restaurant_data(self.weeks_menus)


    def tearDown(self):
        self.testbed.deactivate()

    def test_print_day_menu(self):
        print "\n"
        self.print_DayMenu(self.weeks_menus[0])

    def test_test_data(self):
        self.assertEqual("Paahdettua perunaa ja kasviksia", self.weeks_menus[0].courses[0].components[1].name, msg="Loaded test data was invalid")

    def test_dataStore_has_restaurant_entity(self):
        restaurant = model.Restaurant.query(model.Restaurant.name == "Bolero").get()
        self.assertEqual(restaurant.name, "Bolero")







# if __name__ == '__main__':
#     # unittest.main()
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestDataToDataStore)
#     unittest.TextTestRunner(verbosity=1).run(suite)
