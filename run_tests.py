import unittest
import tests.test_data_to_data_store as my_test
# import tests.test_datastore_housekeeping_functions as td



suite = unittest.TestLoader().loadTestsFromTestCase(my_test.TestDataToDataStore)
# suite.addTests(unittest.TestLoader().loadTestsFromTestCase(td.TestAddDates))
unittest.TextTestRunner(verbosity=2).run(suite)
