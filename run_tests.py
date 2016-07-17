import unittest
import tests.test_datastore_housekeeping_functions as td

suite = unittest.TestLoader().loadTestsFromTestCase(td.TestWithPickledRestaurantsData)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(td.TestAddDates))
unittest.TextTestRunner(verbosity=2).run(suite)
