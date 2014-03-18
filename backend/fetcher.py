'''
Created on Mar 18, 2014

@author: nikhil
'''
import urllib2
import json
import settings
from tornado.httpclient import AsyncHTTPClient

def callback(response):
    # do nothing for time being
    print response

class Fetcher():
    '''
    submit a async request for coordinates which didnt get any data feed
    '''
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
    def add(self):
        url = '{0}/location/{1}/{2}/'.format(settings.FETCHER_SERVER_URL, self.lat, self.lng)
        # have to send the data as JSON
        async_client = AsyncHTTPClient()
        async_client.fetch(url, callback)
