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
              "coord" =>  "15.13412991,58.32243012",
}

    '''
    def __init__(self):
        pass 
    def get_indexes(self):
        url = '{0}_aliases'.format(config.get('elasticsearch', 'server-url'))
        response = urllib2.urlopen(url).read()
        return response
    def get_last_1day_period_activity(self):
        url = '{0}/_search'.format(config.get('elasticsearch', 'server-url'))
        data = {"size":0,"query":{"filtered":{"filter":{"numeric_range":{"@timestamp":{"gte":"now-1d"}}}}},"facets":{"histo1":{"date_histogram":{"field":"@timestamp","interval":"hour"}}}}
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
    def get_random_feed(self, from_datetime, q_from, q_size, encoded_tags, radius, sort):
        url = '{0}/_search'.format(config.get('elasticsearch', 'server-url'))
        sortby = []
        if sort:
            sortby.append({ "up_votes" : {"order" : "desc"}}) 
        sortby.append({ "@timestamp" : {"order" : "desc"}})
        data = {
                "from" : q_from, "size" : q_size,
                "fields" : ["text", "@timestamp", "type", "post_id", "user_img_url", "content_img_url", "coord", "up_votes"],
                "sort" : sortby
                }
        from_date_filter = {
            "range" : {
               "@timestamp" : {
                  "lte" : from_datetime
               }
            }
         }
        data["query"] = {"filtered":{"filter" :{"bool":{"must":[ from_date_filter]}}}}
        
        if encoded_tags:
            data["query"]["filtered"]["query"]= { 
                              "terms": 
                                {
                                "text" : encoded_tags.split(','),
                                "minimum_should_match" : 1
                                }
                              }
        else:
            data["query"]["filtered"]["query"] = {"match_all" : {}}            
        
        # have to send the data as JSON
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
    def get_feed_around_coord(self, from_datetime, coord, q_from, q_size, encoded_tags, radius, sort):
        # { "up_votes" : {"order" : "desc"}},
        url = '{0}/_search'.format(config.get('elasticsearch', 'server-url'))
        sortby = []
        if sort:
            sortby.append({ "up_votes" : {"order" : "desc"}}) 
        sortby.append({ "@timestamp" : {"order" : "desc"}})
        sortby.append({
                                "_geo_distance" : {
                                              "coord" : {
                                                             "lat" : coord[0],
                                                            "lon" : coord[1]
                                                    },
                                            "order" : "asc",
                                            "unit" : "km"
                                }
                            })
                        
        data = {
                "from" : q_from, "size" : q_size,
                "fields" : ["text", "@timestamp", "type", "post_id", "user_img_url", "content_img_url", "coord", "up_votes"],
                "sort" : sortby
                }
        from_date_filter = {
            "range" : {
               "@timestamp" : {
                  "lte" : from_datetime
               }
            }
         }
        coord_filter = {
                "geo_distance" : {
                    "distance" : "{0}km".format(radius),
                    "coord" : {
                        "lat" : coord[0],
                        "lon" : coord[1]
                    }
                }
            } 
        data["query"] = {"filtered":{"filter" :{"bool":{"must":[coord_filter, from_date_filter]}}}}
        
        if encoded_tags:
            data["query"]["filtered"]["query"]= { 
                              "terms": 
                                {
                                "text" : encoded_tags.split(','),
                                "minimum_should_match" : 1
                                }
                              }
        else:
            data["query"]["filtered"]["query"] = {"match_all" : {}}
       
        # have to send the data as JSON
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
    def get_by_document_id(self, document_id):
        # fetch the document by the id
        url = '{0}/_search'.format(config.get('elasticsearch', 'server-url'))
        data = {
                "fields" : ["text", "@timestamp", "type", "post_id", "user_img_url", "content_img_url", "coord", "up_votes"]
                }
        data["query"] =  {"term":{
                                "_id" : str(document_id)
                                }
                              }
        data = json.dumps(data) 
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
    def delete_by_document_id(self, index_name, doc_type, document_id):
        # fetch the document by the id
        url = '{0}/{1}/{2}/{3}'.format(config.get('elasticsearch', 'server-url'), index_name, doc_type, document_id)
        req = urllib2.Request(url)
        req.get_method = lambda: 'DELETE'
        out = urllib2.urlopen(req)
        return out.read()
    def create_document(self, index_name, doc_type, json_body, document_id=None):
        # fetch the document by the id
        if document_id:
            url = '{0}/{1}/{2}/{3}/'.format(config.get('elasticsearch', 'server-url'), index_name, doc_type, document_id)
        else:
            url = '{0}/{1}/{2}/'.format(config.get('elasticsearch', 'server-url'), index_name, doc_type)
        req = urllib2.Request(url, json_body)
        req.get_method = lambda: 'POST'
        out = urllib2.urlopen(req)
        return out.read()
        