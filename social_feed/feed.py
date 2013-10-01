'''
Created on Oct 1, 2013

@author: nikhil
'''
import urllib2
import ConfigParser

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
    def get_random_feed(self):
        url = '{0}{1}/logs/_search?q=host:nikhil-desktop'.format(config.get('elasticsearch', 'server-url'), config.get('elasticsearch', 'index-alias'))
        response = urllib2.urlopen(url).read()
        return response
        