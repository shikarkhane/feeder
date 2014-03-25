'''
Created on Oct 1, 2013

@author: nikhil
'''
import urllib2
import json
import settings

class Feed(object):
    '''
    everything related to user feeds 

    Many posts constitute a feed. 
    Json example of a post:
{
           "username" => "annagereben",
           "up_votes" => 2,
               "text" => "@lindawilhelmsson",
            "post_id" => "655070967730519194_7494078",
       "user_img_url" => "http://images.ak.instagram.com/profiles/profile_7494078_75sq_1384035755.jpg",
         "place_name" => "John Chris",
            "user_id" => "7494078",
              "coord" => "59.331336,18.063978",
    "content_img_url" => "http://instagram.com/p/kXR5MOP7ya/",
         "@timestamp" => "2014-02-19T07:44:19.093Z",
               "type" => "instagram",
       "user_mention" => ""
}
{
               "text" => "k om p mig sjlv  att sitta och rkna upp metanserien som jag lrde mig i ttan.. Att jag kom ig den haha!",
               "lang" => "sv",
         "@timestamp" => "2014-02-19T07:44:44.076Z",
               "type" => "twitter",
            "post_id" => "433998347813535745",
           "up_votes" => 0,
       "user_mention" => "",
         "place_name" => "Sollefte",
            "user_id" => "439237009",
           "username" => "ksdfja",
       "user_img_url" => "http://pbs.twimg.com/profile_images/2578959735/image_normal.jpg",
    "content_img_url" => "%{[entities][media_url]}",
              "coord" => "63.17168396,17.79328865"
}

    '''
    def __init__(self):
        self.field_list = ["user_id", "username", "place_name", "text", "@timestamp", "type", "post_id", "user_img_url",
                           "content_img_url", "coord", "up_votes"]
    def get_indexes(self):
        url = '{0}/_aliases'.format(settings.ELASTICSEARCH_SERVER_URL)
        response = urllib2.urlopen(url).read()
        return response
    def get_last_1day_period_activity(self):
        url = '{0}/{1}/_search'.format(settings.ELASTICSEARCH_SERVER_URL, settings.ELASTICSEARCH_INDEX_ALIAS)
        data = {"size":0,"query":{"filtered":{"filter":{"numeric_range":{"@timestamp":{"gte":"now-1d"}}}}},
                "facets":{"histo1":{"date_histogram":{"field":"@timestamp","interval":"hour"}}}}
        data = json.dumps(data)
        req = urllib2.Request(url, data)
        out = urllib2.urlopen(req)
        return out.read()
    def get_random_feed(self, from_datetime, q_from, q_size, encoded_tags, radius, sort):
        url = '{0}/{1}/_search'.format(settings.ELASTICSEARCH_SERVER_URL, settings.ELASTICSEARCH_INDEX_ALIAS)
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
        url = '{0}/{1}/_search'.format(settings.ELASTICSEARCH_SERVER_URL, settings.ELASTICSEARCH_INDEX_ALIAS)
        sortby = []
        if sort:
            sortby.append({ "up_votes" : {"order" : "desc"}}) 
        sortby.append({ "@timestamp" : {"order" : "desc"}})
        sortby.append({
                                "_geo_distance" : {
                                              "coord" : {
                                                             "lat" : float(coord[0]),
                                                            "lon" : float(coord[1])
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
                        "lat" : float(coord[0]),
                        "lon" : float(coord[1])
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
    def get_popular_around_coord(self, from_datetime, coord, q_from, q_size, encoded_tags, radius, sort, source='instagram'):
        # { "up_votes" : {"order" : "desc"}},
        url = '{0}/{1}/_search'.format(settings.ELASTICSEARCH_SERVER_URL, settings.ELASTICSEARCH_INDEX_ALIAS)
        sortby = []
        if sort:
            sortby.append({ "up_votes" : {"order" : "desc"}})
        sortby.append({ "@timestamp" : {"order" : "desc"}})
        sortby.append({
                                "_geo_distance" : {
                                              "coord" : {
                                                             "lat" : float(coord[0]),
                                                            "lon" : float(coord[1])
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
        source_equals = {
                "term" : {
                    "type" : source
                }
            }
        coord_filter = {
                "geo_distance" : {
                    "distance" : "{0}km".format(radius),
                    "coord" : {
                        "lat" : float(coord[0]),
                        "lon" : float(coord[1])
                    }
                }
            }
        data["query"] = {"filtered":{"filter" :{"bool":{"must":[coord_filter, from_date_filter, source_equals]}}}}

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
        url = '{0}/{1}_search'.format(settings.ELASTICSEARCH_SERVER_URL, settings.ELASTICSEARCH_INDEX_ALIAS)
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
        url = '{0}/{1}/{2}/{3}'.format(settings.ELASTICSEARCH_SERVER_URL, index_name, doc_type, document_id)
        req = urllib2.Request(url)
        req.get_method = lambda: 'DELETE'
        out = urllib2.urlopen(req)
        return out.read()
    def create_document(self, index_name, doc_type, json_body, document_id=None):
        # fetch the document by the id
        if document_id:
            url = '{0}/{1}/{2}/{3}/'.format(settings.ELASTICSEARCH_SERVER_URL, index_name, doc_type, document_id)
        else:
            url = '{0}/{1}/{2}/'.format(settings.ELASTICSEARCH_SERVER_URL, index_name, doc_type)
        req = urllib2.Request(url, json_body)
        req.get_method = lambda: 'POST'
        out = urllib2.urlopen(req)
        return out.read()
    def create_native_document(self, user_id, user_img_url, text, lat, lon, post_time, location_name, content_url,
                               username, index_name = settings.NATIVE_INDEX, doc_type = settings.NATIVE_TYPE):
        # fetch the document by the id
        url = '{0}/{1}/{2}/'.format(settings.ELASTICSEARCH_SERVER_URL, index_name, doc_type)
        json_body = {"text": text, "lang" : "na", "@timestamp" : post_time, "type" : doc_type,
            "post_id" : 0, "up_votes" : 0, "user_mention" : None, "place_name" : location_name,
            "user_id" : user_id, "user_img_url" : user_img_url, "content_img_url" : content_url,
            "coord" : "{0},{1}".format(lat,lon), "username": username}
        req = urllib2.Request(url, json.dumps(json_body))
        req.get_method = lambda: 'POST'
        out = urllib2.urlopen(req)
        return out.read()
