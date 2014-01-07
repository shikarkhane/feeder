from social_feed.feed import Feed
import json
import datetime
from common.utility import Url_Handler

class Post():
    '''
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
    def __init__(self, post_id, text, created, content_img_url, user_img_url, source, up_votes =0 ):
        # post_id is the internal _id of elasticsearch store
        self.post_id = post_id
        self.text = text
        self.created = created
        self.content_img_url = content_img_url
        self.user_img_url = user_img_url
        self.source = source
        self.up_votes = up_votes
        #self.coord = coord   
    def get_as_dict(self):
        d = {"post_id": self.post_id, "text": self.text, "created": self.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"), 
             "content_img_url": self.content_img_url, "user_img_url":self.user_img_url, "source": self.source, "up_votes": self.up_votes}
        return d      
class Feed_Content():
    '''Provides feed content'''
    def get_random_feed(self, from_datetime, q_from, q_size, encoded_tags):
        f = Feed()
        data = []
        result = json.loads(f.get_random_feed(from_datetime, q_from, q_size, encoded_tags))
        if result["hits"]["total"] > 0:
            for p in result["hits"]["hits"]:
                field = p["fields"]
                try:
                    url_util = Url_Handler()
                    media_url = url_util.get_url_from_string(field.get("content_img_url"))
                    if not media_url:
                        # see if text field has a url in it
                        media_url = url_util.get_url_from_string(field["text"].encode("utf-8"))
                    data.append(Post( p["_id"], field["text"].encode("utf-8"),  datetime.datetime.strptime(field.get("@timestamp"), '%Y-%m-%dT%H:%M:%S.%fZ'), media_url, field.get("user_img_url"), field.get("type"), field.get("up_votes")))
                except Exception, e:
                    print str(e), p
                    pass # fetcher engine and logstash must ensure clean data gets into elasticsearch which confirms to the Post object
        return data
    def get_random_feed_as_json(self,from_datetime, q_from, q_size, encoded_tags):
        data = self.get_random_feed(from_datetime, q_from, q_size, encoded_tags)
        return [(d.get_as_dict()) for d in data]
    def get_feed_around_coord(self, from_datetime, coord, q_from, q_size, encoded_tags):
        f = Feed()
        data = []
        result = json.loads(f.get_feed_around_coord(from_datetime, coord, q_from, q_size, encoded_tags))
        if result["hits"]["total"] > 0:
            for p in result["hits"]["hits"]:
                field = p["fields"]
                try:
                    url_util = Url_Handler()
                    media_url = url_util.get_url_from_string(field.get("content_img_url"))
                    if not media_url:
                        # see if text field has a url in it
                        media_url = url_util.get_url_from_string(field.get("text").encode("utf-8"))
                    data.append(Post( p["_id"], field.get("text").encode("utf-8"),  datetime.datetime.strptime(field.get("@timestamp"), '%Y-%m-%dT%H:%M:%S.%fZ'), media_url, field.get("user_img_url"), field.get("type"), field.get("up_votes")))
                except Exception, e:
                    print str(e), p
                    pass # fetcher engine and logstash must ensure clean data gets into elasticsearch which confirms to the Post object
        return data
    def get_feed_around_coord_as_json(self, from_datetime, coord, q_from, q_size, encoded_tags):
        data = self.get_feed_around_coord(from_datetime, coord, q_from, q_size, encoded_tags)
        return [(d.get_as_dict()) for d in data]
    def increment_upvote(self,data):
        '''this method should be removed in future when post object is being passed everywhere'''
        if data.get("up_votes"):
            data["up_votes"] = int(data["up_votes"]) + 1
        else:
            data["up_votes"] = 1
        return data
    def like_post(self, document_id):
        f = Feed()
        d = f.get_by_document_id(document_id)
        if (json.loads(d)["hits"]["total"] == 0):
            return None
        else:
            data = json.loads(d)["hits"]["hits"][0]
            d_index = data["_index"]
            d_doctype = data["_type"]
            d_id = document_id
            fields = data["fields"]
            fields = self.increment_upvote(fields)
        f.delete_by_document_id(d_index, d_doctype, d_id)
        f.create_document(index_name = d_index, doc_type = d_doctype, document_id = d_id, json_body = json.dumps(fields))
class Backoffice_content():
    '''administrative and analytics'''
    def get_last_1day_period_activity(self):
        f = Feed()
        data = []
        result = json.loads(f.get_last_1day_period_activity())
        entries = result['facets']['histo1']['entries']
        if len(entries) > 0:
            data = [entry["count"] for entry in entries]
        return data
