'''
Created on Oct 1, 2013

@author: nikhil
'''
import urllib2
import ConfigParser
import json
import settings

config = ConfigParser.RawConfigParser()
config.read('config.cfg') 
class Feed(object):
    '''
    everything related to user feeds 

    Many posts constitute a feed. 
    Json example of a post:
{
               "text" => "@nollbit @johanni ja, klart det bara blir spekulationer. Men samhllsnyttig infrastruktur br vl vara delvis skyddad mot detta?",
               "lang" => "sv",
         "@timestamp" => "2014-01-09T10:01:30.449Z",
               "type" => "twitter",
            "post_id" => 418676219430047744,
           "up_votes" => 0,
       "user_mention" => "{\"id\"=>15809255, \"indices\"=>[0, 8], \"id_str\"=>\"15809255\", \"screen_name\"=>\"nollbit\", \"name\"=>\"johan\"},{\"id\"=>16311319, \"indices\"=>[9, 17], \"id_str\"=>\"16311319\", \"screen_name\"=>\"johanni\", \"name\"=>\"Johan Nilsson\"}",
         "place_name" => "Knivsta",
            "user_id" => "14235149",
       "user_img_url" => "http://pbs.twimg.com/profile_images/378800000478670862/88783a59c7c7e5c200627af584781212_normal.jpeg",
    "content_img_url" => "%{[entities][media_url]}",
              "coord" => "59.74596768,17.78693824"
}
    '''
    def __init__(self):
        self.field_list = ["user_id", "place_name", "text", "@timestamp", "type", "post_id", "user_img_url", "content_img_url", "coord", "up_votes"] 
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
                "fields" : self.field_list,
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
                "fields" : self.field_list,
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
                "fields" : self.field_list
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
    def create_native_document(self, user_id, user_img_url, text, lat, lon, post_time, location_name, index_name = settings.NATIVE_INDEX, doc_type = settings.NATIVE_TYPE):
        # fetch the document by the id
        url = '{0}/{1}/{2}/'.format(config.get('elasticsearch', 'server-url'), index_name, doc_type)
        json_body = {"text": text, "lang" : "na", "@timestamp" : post_time, "type" : doc_type,
            "post_id" : 0, "up_votes" : 0, "user_mention" : None, "place_name" : location_name,
            "user_id" : user_id, "user_img_url" : user_img_url, "content_img_url" : "%{[entities][media_url]}", "coord" : "{0},{1}".format(lat,lon)}
        req = urllib2.Request(url, json.dumps(json_body))
        req.get_method = lambda: 'POST'
        out = urllib2.urlopen(req)
        return out.read()
