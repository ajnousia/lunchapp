import unittest
import logging
import sys
import pickle
from data_store_classes import PickledRestaurants

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed


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

    def test_update_entity(self):
        pass


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
    unittest.TextTestRunner(verbosity=1).run(suite)
