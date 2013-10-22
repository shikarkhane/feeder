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

    Many posts constitute a feed. 
    Json example of a post:
{
               "text" => "Euw folk i min klass euw",
               "lang" => "nl",
         "@timestamp" => "2013-10-15T10:27:02.000Z",
               "type" => "twitter",
            "post_id" => 390061246474911745,
           "up_votes" => 0,
       "user_img_url" => "http://a0.twimg.com/profile_images/378800000568858024/f8ce9b2482ad43b8cdf13d40517e0ce6_normal.jpeg",
    "content_img_url" => "%{[entities][media_url]}",
              "coord" => "15.13412991,58.32243012",
}

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
                "fields" : ["text", "@timestamp", "type", "post_id", "user_img_url", "content_img_url", "coord"],
                   "query": {
                                "match_all": {}
                            }
                }
        # have to send the data as JSON
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
    def get_feed_around_coord(self, coord, q_from, q_size):
        url = '{0}/_search'.format(config.get('elasticsearch', 'server-url'))
        data = {
                "from" : q_from, "size" : q_size,
                "fields" : ["text", "@timestamp", "type", "post_id", "user_img_url", "content_img_url", "coord"],
                "query": {
                    "filtered" : {
                        "query" : {
                            "match_all" : {}
                        },
                        "filter" : {
                            "geo_distance" : {
                                "distance" : "20km",
                                "coord" : {
                                    "lat" : coord[0],
                                    "lon" : coord[1]
                                }
                            }
                        }
                    }
                 }
                }
        # have to send the data as JSON
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
        