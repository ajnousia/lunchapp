import unittest
import logging
import sys
import pickle
import datetime

from data_store_classes import PickledRestaurants
from datastore_housekeeping_functions import get_entities_without_date, get_monday_date_from_weeknumber

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestAddDates(unittest.TestCase):

    def test_get_date_from_weeknumber(self):
        self.assertEqual(datetime.date(2016,1,4), get_monday_date_from_weeknumber(2016, 1))
        self.assertEqual(datetime.date(2015,12,28), get_monday_date_from_weeknumber(2015, 53))
        self.assertEqual(datetime.date(2014,12,29), get_monday_date_from_weeknumber(2015, 1))
        self.assertEqual(datetime.date(2015,1,5), get_monday_date_from_weeknumber(2015, 2))
        self.assertEqual(datetime.date(2015,8,10), get_monday_date_from_weeknumber(2015, 33))
        self.assertEqual(datetime.date(2017,1,2), get_monday_date_from_weeknumber(2017, 1))
        self.assertEqual(datetime.date(2018,1,1), get_monday_date_from_weeknumber(2018, 1))





class TestWithPickledRestaurantsData(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger("test_log")
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(
            app_id='e~lunchapp-1058',
            overwrite=True)
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        DataLoader().load_data_from_disk_to_datastore()

    def tearDown(self):
        self.testbed.deactivate()

    def test_test_data(self):
        self.assertEqual(len(DataLoader().load_pickled_entities()), len(PickledRestaurants.query().fetch(100)))

    def test_update_entities(self):
        pass

    def test_get_entities_without_date(self):
        entities_without_date = get_entities_without_date(PickledRestaurants, 50)
        self.assertGreater(len(entities_without_date), 0)
        self.log.info("Entities without date -> " + str(len(entities_without_date)))
        for entity in entities_without_date:
            self.assertIsNone(entity.date, "Date was not none")




class DataLoader:

    def load_pickled_entities(self):
        with open("PickledRestaurants_backup_2016-02-28.pkl", "rb") as input:
            entities = pickle.load(input)
        return entities

    def load_data_from_disk_to_datastore(self):
        entities = self.load_pickled_entities()
        ndb.put_multi(entities)


class TestTestDataLoader(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(
            app_id='e~lunchapp-1058',
            overwrite=True)
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_pickled_entity_is_datastore_entity(self):
        entities = DataLoader().load_pickled_entities()
        self.assertEqual(type(type(entities[0])), ndb.model.MetaModel)

    def test_put(self):
        entities = DataLoader().load_pickled_entities()
        entities[0].put()

    def test_put_multi(self):
        entities = DataLoader().load_pickled_entities()
        ndb.put_multi(entities)
        self.assertEqual(len(entities), len(PickledRestaurants.query().fetch(100)))


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("test_log").setLevel(logging.DEBUG)
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWithPickledRestaurantsData)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAddDates))
    unittest.TextTestRunner(verbosity=1).run(suite)
