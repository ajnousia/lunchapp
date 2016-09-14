import unittest
import logging
import sys
import datetime
import pickle

import material_backend.material_app
from tests.test_datastore_housekeeping_functions import DataLoader
import material_backend.model as model
import material_backend.material_app as material_app
import material_backend.datastore_functions as datastore_functions

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestDataToDataStore(unittest.TestCase):

    def load_test_data(self, number_of_weeks):
        entities = DataLoader.load_pickled_entities("PickledRestaurants_backup_2016-07-17.pkl")
        week_menu_list = []
        index_of_Bolero = 0
        for i in range(0, number_of_weeks):
            try:
                week_menu_list.append(entities[i].pickled_restaurants.restaurants[index_of_Bolero].menu_list)
            except IndexError as e:
                break
        return week_menu_list

    def print_DayMenu(self, menu):
        print menu.date
        for course in menu.courses:
            for component in course.components:
                print "\t" + component.name
                print "\t"*2 + component.get_properties_as_string()

    def create_restaurant(self, name):
        restaurant = model.Restaurant(name=name)
        restaurant.put()

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(app_id='e~lunchapp-1058', overwrite=True)
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        self.week_menu_list = self.load_test_data(2)
        self.create_restaurant("Bolero")


    def tearDown(self):
        self.testbed.deactivate()

    # def test_print_day_menu(self):
    #     print "\n"
    #     self.print_DayMenu(self.week_menu_list[0])
    #
    # def test_test_data(self):
    #     self.assertEqual("Paahdettua perunaa ja kasviksia", self.week_menu_list[0].courses[0].components[1].name, msg="Loaded test data was invalid")

    # def test_import_weekmenu_into_datastore(self):
    #     datastore_functions.import_weekmenu_into_datastore(self.week_menu_list, "Bolero")
    #     for daymenu in self.week_menu_list:
    #         datastore_daymenu = model.DayMenu.query(model.DayMenu.date == daymenu.date).get()
    #         self.assertEqual(datastore_daymenu.date, daymenu.date)
    #         for course_pairs in zip(datastore_daymenu.courses, daymenu.courses):
    #             for component_pairs in zip(course_pairs[0].components, course_pairs[1].components):
    #                 self.assertEqual(component_pairs[0].name, component_pairs[1].name)
    #
    # def test_every_course_component_is_in_datastore_by_getting(self):
    #     datastore_functions.import_weekmenu_into_datastore(self.week_menu_list, "Bolero")
    #     for daymenu in self.week_menu_list:
    #         for course in daymenu.courses:
    #             for component in course.components:
    #                 datastore_component = model.Component.query(model.Component.name == component.name).get()
    #                 self.assertEqual(datastore_component.name, component.name)

    def test_every_course_component_has_correct_properties(self):
        datastore_functions.import_weekmenu_list_into_datastore(self.week_menu_list, "Bolero")
        for daymenu in self.week_menu_list[0]:
            for course in daymenu.courses:
                for component in course.components:
                    datastore_component = model.Component.query(model.Component.name == component.name).get()
                    self.assertEqual(datastore_component.properties, component.get_properties_as_string())

    def test_every_course_has_correct_price(self):
        pass







# if __name__ == '__main__':
#     # unittest.main()
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestDataToDataStore)
#     unittest.TextTestRunner(verbosity=1).run(suite)
