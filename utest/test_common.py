'''
Created on Oct 22, 2013

@author: nikhil
'''
import unittest
from common.utility import Url_Handler 

class Test_Utility(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_find_url_in_string(self):
        uh = Url_Handler()
        test_string = """@russian_market: Meanwhile in London!!!! ( h/t @QuantumSquawk) http://t.co/KOKjMXlJab' haha is he phoning while pole sitting?"""
        embedded_url = "http://t.co/KOKjMXlJab"
        data = uh.get_url_from_string(test_string) 
        self.assertEqual(data, embedded_url)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()