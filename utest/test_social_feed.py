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
        data = f.get_random_feed(0, 10) 
        data_json = json.loads(data)
        self.assertGreater(data_json["hits"]["total"],0)
    def test_feed_data_around_a_coord(self):
        f = feed.Feed() 
        data = f.get_feed_around_coord([17.27853714,60.1796792], 0, 10) 
        data_json = json.loads(data)
        print data_json['hits']
        self.assertGreater(int(data_json['hits']['total']),0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()