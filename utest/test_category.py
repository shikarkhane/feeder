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
    def test_add_feature_to_category(self, category = 'gossip', feature='lol'):
        c = Classify()
        c.add_feature_to_category(category=category, feature=feature, weight=1)
        r = c.get_feature_set()
        self.assertNotEqual(r, {})
    def test_word_exists_in_category_features(self):
        c = Classify()
        w = "crazyjackson"
        cat = "gossip"
        c.add_feature_to_category(category=cat, feature=w, weight=1)
        r = c.word_exists_in_category_features(category=cat, w=w)
        self.assertGreater(r, 0)
    def test_evaluate_category(self):
        c = Classify()
        cs = {"gossip":1, "science":3, "concert": 2}
        res = c.evaluate_category(category_score=cs)
        self.assertEqual(res, 'science')
    def test_get_category_for_text(self):
        c = Classify()
        ct = 'gossip'
        f = 'lol'
        ct1 = 'other'
        f1 = 'random'
        text = 'this guy is crazy ' + f
        self.test_add_feature_to_category(category=ct, feature=f)
        self.test_add_feature_to_category(category=ct1, feature=f1)
        c.refresh_feature_set()
        cat = c.get_category_for_text(text=text)
        self.assertEqual(cat, ct)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()