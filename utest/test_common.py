'''
Created on Oct 22, 2013

@author: nikhil
'''
import unittest
from common.utility import Url, Location, User
import time

class Test_Utility(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_find_url_in_string(self):
        uh = Url()
        test_string = """"s@russian_market: Meanwhile in London!!!! ( h/t @QuantumSquawk) http://t.co/KOKjMXlJab" haha is he phoning while pole sitting?"""
        embedded_url = "http://t.co/KOKjMXlJab"
        data = uh.get_url_from_string(test_string) 
        self.assertEqual(data, embedded_url)
    def test_get_city_for_coord(self):
        r = Location()
        # sublocality is brooklyn
        city = r.lookup_city(40.714224,-73.961452)
        self.assertEqual(city, 'Brooklyn')
    def test_user_native_post_id(self):
        user_id = 0
        first_user = User().get_native_post_id(user_id)
        time.sleep(1)
        second_user = User().get_native_post_id(user_id)
        self.assertNotEqual(first_user, second_user)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()