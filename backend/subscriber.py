'''
Created on Mar 4, 2014

@author: nikhil
'''
import urllib2
import json
import settings

class Subscribe(object):
    '''
    users subscribing to email updates about new features etc
    json for this is simple:
    { 'email' : 'somebody@somemail.com'}

    '''
    def __init__(self):
        self.field_list = ["email"]
        self.index_name = 'subscriber'
        self.index_type = 'email'
    def add(self, email):
        url = '{0}/{1}/{2}'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name, self.index_type)
        data = {'email' : email}
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
    def remove_by_email(self, email):
        r = json.loads(self.get_by_email(email))
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                document_id = p['_id']
                break
        if not document_id:
            return False
        self.remove(document_id)
    def get(self, document_id):
        # fetch the document by the id
        url = '{0}/{1}/{2}/_search?q=_id:{3}'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name, self.index_type, document_id)
        req = urllib2.Request(url)
        out = urllib2.urlopen(req)
        return out.read()
    def get_by_email(self, email):
        # fetch the document by the id
        url = '{0}/{1}/{2}/_search?q=email:{3}'.format(settings.ELASTICSEARCH_SERVER_URL, self.index_name,
                                                       self.index_type, email)
        req = urllib2.Request(url)
        out = urllib2.urlopen(req)
        return out.read()
    def exists(self, email):
        r = json.loads(self.get_by_email(email))
        if r["hits"]["total"] > 0:
            return True
        else:
            return False