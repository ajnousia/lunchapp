import unittest
import tests.test_data_to_data_store as my_test
# import tests.test_datastore_housekeeping_functions as td

testSuite = unittest.TestSuite()
testSuite.addTest(my_test.TestDataToDataStore("test_every_course_has_correct_date"))

suite = unittest.TestLoader().loadTestsFromTestCase(my_test.TestDataToDataStore)
# suite.addTests(unittest.TestLoader().loadTestsFromTestCase(td.TestAddDates))

unittest.TextTestRunner(verbosity=3).run(testSuite)
