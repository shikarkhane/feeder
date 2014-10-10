'''
Created on Oct 10, 2014

@author: nikhil
'''
import unittest
from category.models import Classify
import os
import settings

class Test_Classify(unittest.TestCase):
    def setUp(self):
        with open(settings.FEATURE_SET, 'w') as ff:
            ff.write('{}')
    def tearDown(self):
        os.remove(settings.FEATURE_SET)
    def test_get_feature_set(self):
        c = Classify()
        r = c.get_feature_set()
        self.assertEqual(r, {})
    def test_add_feature_to_category(self):
        c = Classify()
        c.add_feature_to_category(category="gossip", feature="lol", weight=1)
        r = c.get_feature_set()
        self.assertNotEqual(r, {})
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()