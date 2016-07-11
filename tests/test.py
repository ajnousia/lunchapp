import unittest
import logging
import sys
import datetime


import material_backend.material_app

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestDataToDataStore(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(app_id='e~lunchapp-1058', overwrite=True)
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_something():
        pass



# if __name__ == '__main__':
#     # unittest.main()
#     suite = unittest.TestLoader().loadTestsFromTestCase(TestDataToDataStore)
#     unittest.TextTestRunner(verbosity=1).run(suite)
