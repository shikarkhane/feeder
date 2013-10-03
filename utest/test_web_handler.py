'''
Created on Oct 3, 2013

@author: nikhil
'''
import unittest
from web_handler.models import Feed_Content, Post

class Test_Models(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_random_feed_of_post_objects(self):
        fc = Feed_Content()
        data = fc.get_random_feed()
        self.assert_(isinstance(data[0], Post))
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()