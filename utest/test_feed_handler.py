'''
Created on Oct 3, 2013

@author: nikhil
'''
import unittest
from feed_handler.models import Feed_Content, Post, Category

class Test_Models(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_random_feed_of_post_objects(self):
        fc = Feed_Content()
        data = fc.get_random_feed(1389088775204, 0, 10, None, 10, 1)
        self.assert_(isinstance(data[0], Post))
    def test_categories_get(self):
        r = Category().get()
        print r
        self.assertGreater(len(r), 0)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()