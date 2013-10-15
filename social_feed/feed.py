'''
Created on Oct 1, 2013

@author: nikhil
'''
import urllib2
import ConfigParser
import json

config = ConfigParser.RawConfigParser()
config.read('config.cfg') 
class Feed(object):
    '''
    everything related to user feeds 
    '''
    def __init__(self):
        pass 
    def get_indexes(self):
        url = '{0}_aliases'.format(config.get('elasticsearch', 'server-url'))
        response = urllib2.urlopen(url).read()
        return response
    def get_random_feed(self, q_from, q_size):
        url = '{0}/_search'.format(config.get('elasticsearch', 'server-url'))
        data = {
                "from" : q_from, "size" : q_size,
                   "query": {
                                "match_all": {}
                            }
                }
        # have to send the data as JSON
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
    def get_feed_around_coord(self, coord):
        url = '{0}{1}/log/_search'.format(config.get('elasticsearch', 'server-url'), config.get('elasticsearch', 'index-alias'))
        data = {}
        # have to send the data as JSON
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out
        