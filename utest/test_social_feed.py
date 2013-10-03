'''
Created on Oct 1, 2013

@author: nikhil
'''
import unittest
from social_feed import feed
import json
import config

class Test_feed(unittest.TestCase):
    def setUp(self):
        config.create_config_file("mainkey","mainvalue")
    def tearDown(self):
        pass
    def test_feed_index_exists(self):
        f = feed.Feed() 
        data = f.get_indexes() 
        data_json = json.loads(data)
        self.assertGreater(len(data_json),0)
    def test_check_random_feed_data_existence(self):
        f = feed.Feed() 
        data = f.get_random_feed() 
        data_json = json.loads(data)
        #print data_json["hits"]["hits"][0]["_source"]
        self.assertGreater(len(data_json),0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()