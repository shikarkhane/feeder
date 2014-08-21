'''
Created on Aug 21, 2014

@author: nikhil
'''
import urllib2
import json
import settings

class Category(object):
    '''
    category of a post will help us filter the data based on user preference
    If the user is only interested in gossip and discounts, then we will filter using this category
    json for this is simple:
    { 'category_id': 1, 'category_name' : 'discount'}

    '''
    def __init__(self):
        self.field_list = ["category_id", "category_name"]
        self.index_name = 'category'
        self.index_type = 'master_list'
    def add(self, category_id, category_name):
        url = '{0}/{1}/{2}'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name, self.index_type)
        data = {'category_id': category_id, 'category_name' : category_name}
        # have to send the data as JSON
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
    def remove(self, document_id):
        # fetch the document by the id
        url = '{0}/{1}/{2}/{3}'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name, self.index_type, document_id)
        req = urllib2.Request(url)
        req.get_method = lambda: 'DELETE'
        out = urllib2.urlopen(req)
        return out.read()
    def remove_by_category_id(self, category_id):
        r = json.loads(self.get_by_category_id(category_id))
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                document_id = p['_id']
                break
        if not document_id:
            return False
        self.remove(document_id)
    def remove_by_category_name(self, category_name):
        r = json.loads(self.get_by_category_name(category_name))
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                document_id = p['_id']
                break
        if not document_id:
            return False
        self.remove(document_id)
    def get_all(self):
        url = '{0}/{1}/{2}/_search?q=*:*'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name,
                                                     self.index_type)
        req = urllib2.Request(url)
        out = urllib2.urlopen(req)
        return out.read()
    def get(self, document_id):
        # fetch the document by the id
        url = '{0}/{1}/{2}/_search?q=_id:{3}'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name,
                                                     self.index_type, document_id)
        req = urllib2.Request(url)
        out = urllib2.urlopen(req)
        return out.read()
    def get_by_category_id(self, category_id):
        # fetch the document by the id
        url = '{0}/{1}/{2}/_search?q=category_id:{3}'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name,
                                                       self.index_type, category_id)
        req = urllib2.Request(url)
        out = urllib2.urlopen(req)
        return out.read()
    def get_by_category_name(self, category_name):
        # fetch the document by the id
        url = '{0}/{1}/{2}/_search?q=category_name:{3}'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name,
                                                       self.index_type, category_name)
        req = urllib2.Request(url)
        out = urllib2.urlopen(req)
        return out.read()
    def exists_by_category_name(self, category_name):
        r = json.loads(self.get_by_category_name(category_name))
        if r["hits"]["total"] > 0:
            return True
        else:
            return False
    def exists_by_category_id(self, category_id):
        r = json.loads(self.get_by_category_id(category_id))
        if r["hits"]["total"] > 0:
            return True
        else:
            return False