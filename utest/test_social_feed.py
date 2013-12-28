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
        data = f.get_random_feed(0, 10,'min') 
        data_json = json.loads(data)
        self.assertGreater(data_json["hits"]["total"],0)
    def test_feed_data_around_a_coord(self):
        f = feed.Feed() 
        data = f.get_feed_around_coord([58.58972357,16.19912264], 0, 10, 'min') 
        data_json = json.loads(data)
        #print data_json['hits']
        self.assertGreater(int(data_json['hits']['total']),0)
    def test_backoffice_activity(self):
        '''count of posts in the last 24 hours periods'''
        f = feed.Feed()
        data = f.get_last_1day_period_activity()
        data_json = json.loads(data)
        self.assertGreater(len(data_json['facets']['histo1']['entries']), 0)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()