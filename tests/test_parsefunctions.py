import unittest
from old_lunchapp.parsefunctions import get_json

class  TestAtomitieParser(unittest.TestCase):

    def test_get_json(self):
        url = 'http://www.sodexo.fi/ruokalistat/output/daily_json/9/{0}/{1}/{2}/fi'.format(str(date.year), str(date.strftime('%m')), str(date.strftime('%d')))
        request = urllib2.urlopen(url)
        self.assertGreater(len(request), 0)
