'''
Created on Oct 1, 2013

@author: nikhil
'''
import unittest
from backend import feed, subscriber, category
import json
from time import sleep
from common.utility import Random_Data

class Test_subscriber(unittest.TestCase):
    def setUp(self):
        self.email = 'test'
        self.document_id = ''
        self.s = subscriber.Subscribe()
        self.sleep_in_sec = 2 # cause default indexing delay is 1 sec in elasticsearch
    def test_subscriber_add(self):
        rd = Random_Data()
        self.email = '{0}@{1}.com'.format(rd.id_generator(), rd.id_generator())
        r = json.loads(self.s.add(self.email))
        self.assertEqual(r['created'], True)
        self.document_id = r['_id']
        sleep(self.sleep_in_sec)
        self.assertEqual(self.s.exists(self.email), True)
    def test_subscriber_remove(self):
        self.test_subscriber_add()
        sleep(self.sleep_in_sec)
        self.s.remove(self.document_id)
        sleep(self.sleep_in_sec)
        self.assertEqual(self.s.exists(self.email), False)
    def test_subscriber_remove_by_email(self):
        self.test_subscriber_add()
        sleep(self.sleep_in_sec)
        self.s.remove_by_email(self.email)
        sleep(self.sleep_in_sec)
        self.assertEqual(self.s.exists(self.email), False)
    def test_subscriber_get(self):
        self.test_subscriber_add()
        sleep(self.sleep_in_sec)
        r = json.loads(self.s.get(self.document_id))
        e = ''
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                e = p['_source']['email']
        self.assertEqual(self.email, e)
    def test_subscriber_get_by_email(self):
        self.test_subscriber_add()
        sleep(self.sleep_in_sec)
        r = json.loads(self.s.get_by_email(self.email))
        e = ''
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                e = p['_source']['email']
        self.assertEqual(self.email, e)
class Test_category(unittest.TestCase):
    def setUp(self):
        self.category_id = '1221'
        self.category_name = 'test-category-1'
        self.document_id = ''
        self.s = category.Category()
        self.sleep_in_sec = 2 # cause default indexing delay is 1 sec in elasticsearch
    def tearDown(self):
        if self.s.exists_by_category_id(self.category_id):
            self.s.remove_by_category_id(self.category_id)
    def test_category_add(self):
        rd = Random_Data()
        self.category_name = '{0}'.format(rd.id_generator())
        r = json.loads(self.s.add(self.category_id, self.category_name))
        self.assertEqual(r['created'], True)
        self.document_id = r['_id']
        sleep(self.sleep_in_sec)
        self.assertEqual(self.s.exists_by_category_name(self.category_name), True)
    def test_category_remove(self):
        self.test_category_add()
        sleep(self.sleep_in_sec)
        self.s.remove(self.document_id)
        sleep(self.sleep_in_sec)
        self.assertEqual(self.s.exists_by_category_name(self.category_name), False)
    def test_category_remove_by_category_name(self):
        self.test_category_add()
        sleep(self.sleep_in_sec)
        self.s.remove_by_category_name(self.category_name)
        sleep(self.sleep_in_sec)
        self.assertEqual(self.s.exists_by_category_name(self.category_name), False)
    def test_category_get(self):
        self.test_category_add()
        sleep(self.sleep_in_sec)
        r = json.loads(self.s.get(self.document_id))
        e = ''
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                e = p['_source']['category_name']
        self.assertEqual(self.category_name, e)
    def test_category_get_by_category_name(self):
        self.test_category_add()
        sleep(self.sleep_in_sec)
        r = json.loads(self.s.get_by_category_name(self.category_name))
        e = ''
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                e = p['_source']['category_name']
        self.assertEqual(self.category_name, e)
    def test_category_get_by_category_id(self):
        self.test_category_add()
        sleep(self.sleep_in_sec)
        r = json.loads(self.s.get_by_category_id(self.category_id))
        e = ''
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                e = p['_source']['category_id']
        self.assertEqual(self.category_id, e)
class Test_feed(unittest.TestCase):
    def tearDown(self):
        pass
    def test_feed_index_exists(self):
        f = feed.Feed() 
        data = f.get_indexes() 
        data_json = json.loads(data)
        self.assertGreater(len(data_json),0)
    def test_check_random_feed_data_existence(self):
        f = feed.Feed() 
        data = f.get_random_feed(1389088775204, 0, 10,'min', 10, 0,1)
        data_json = json.loads(data)
        self.assertGreater(data_json["hits"]["total"],0)
    def test_feed_data_around_a_coord(self):
        f = feed.Feed() 
        data = f.get_feed_around_coord(1389088775204, [58.58972357,16.19912264], 0, 10, 'min', 10, 1,1)
        data_json = json.loads(data)
        #print data_json['hits']
        self.assertGreater(int(data_json['hits']['total']),0)
    def test_backoffice_activity(self):
        '''count of posts in the last 24 hours periods'''
        f = feed.Feed()
        data = f.get_last_1day_period_activity()
        data_json = json.loads(data)
        self.assertGreater(len(data_json['facets']['histo1']['entries']), 0)
    def test_get_document_by_id(self):
        ''' in elasticsearch with source disabled, we will select, delete existing and insert new'''
        f = feed.Feed()
        # create document to be deleted
        d_new = self.test_create_document()
        d_id = d_new["_id"]
        sleep(5) # cause default indexing delay is 1 sec in elasticsearch
        res = f.get_by_document_id(d_id)
        found_count = int(json.loads(res)["hits"]["total"])
        self.assertEqual(1, found_count)
    def test_create_document(self):
        ''' in elasticsearch with source disabled, we will select, delete existing and insert new'''
        f = feed.Feed()
        json_data = {"text":"Euw folk i min klass euw","lang":"nl","@timestamp":"2013-10-15T10:27:02.000Z","type":"twitter","post_id":"390061246474911745","up_votes":"0","user_img_url":"http://a0.twimg.com/profile_images/378800000568858024/f8ce9b2482ad43b8cdf13d40517e0ce6_normal.jpeg","content_img_url":"%{[entities][media_url]}","coord":"15.13412991,58.32243012"}
        d_index = "logstash-testing"
        d_doctype = "twitter"
        # get document to be deleted
        res = f.create_document( index_name = d_index, doc_type = d_doctype, document_id = None, json_body = json.dumps(json_data))
        j_res = json.loads(res) 
        self.assertTrue(j_res["created"])
        return j_res
    def test_delete_document_by_id(self):
        ''' in elasticsearch with source disabled, we will select, delete existing and insert new'''
        f = feed.Feed()
        # create document to be deleted
        d_new = self.test_create_document()
        d_id = d_new["_id"]
        d_doctype = d_new["_type"]
        d_index = d_new["_index"]
        #now delete it
        res = f.delete_by_document_id(d_index, d_doctype, d_id)
        self.assertTrue(json.loads(res)["found"])
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()