from social_feed.feed import Feed
import json
from common.utility import Url, Img, Location, Date, User

class Post():
    '''
    Many posts constitute a feed. 
    Json example of a post:
{
               "text" => "@nollbit @johanni ja, klart det bara blir spekulationer. Men samhllsnyttig infrastruktur br vl vara delvis skyddad mot detta?",
         "@timestamp" => "2014-01-09T10:01:30.449Z",
               "type" => "twitter",
            "post_id" => "418676219430047744",
           "up_votes" => 0,
       "user_mention" => "{\"id\"=>15809255, \"indices\"=>[0, 8], \"id_str\"=>\"15809255\", \"screen_name\"=>\"nollbit\", \"name\"=>\"johan\"},{\"id\"=>16311319, \"indices\"=>[9, 17], \"id_str\"=>\"16311319\", \"screen_name\"=>\"johanni\", \"name\"=>\"Johan Nilsson\"}",
         "place_name" => "Knivsta",
            "user_id" => "14235149",
       "user_img_url" => "http://pbs.twimg.com/profile_images/378800000478670862/88783a59c7c7e5c200627af584781212_normal.jpeg",
    "content_img_url" => "%{[entities][media_url]}",
              "coord" => "59.74596768,17.78693824",
              "username" => "zube23"
}
    '''
    def __init__(self, *args):
        '''allow initizing the object using parameters or a single json '''
        if len(args) == 1:
            self.set_using_json(*args)
        else:
            self.set(*args)
    def set(self, doc_id, post_id, text, created, content_img_url, user_img_url, source, user_id, place_name, coord,
                 username, up_votes =0 ):
        # post_id is the internal _id of elasticsearch store
        self.doc_id = doc_id
        self.post_id = post_id
        self.text = text
        self.created = created
        self.content_img_url = content_img_url
        self.user_img_url = user_img_url
        self.source = source
        self.up_votes = up_votes
        self.user_id = user_id
        self.username = username
        self.place_name = place_name
        self.user_profile_url = User().get_profile_url(userid = user_id, source=source, username=username)
        self.coord = coord
    def set_using_json(self, post_json):
        self.doc_id = post_json["doc_id"]
        self.post_id = post_json["post_id"]
        self.text = post_json["text"]

        if post_json.get('created'):
            self.created = post_json["created"]
        else:
            self.created = post_json["@timestamp"]

        url_util = Url()
        media_url = url_util.get_url_from_string(post_json["content_img_url"])
        if not media_url:
            # see if text field has a url in it
            media_url = url_util.get_url_from_string(post_json["text"].encode("utf-8"))
        self.content_img_url = media_url
        self.user_img_url = post_json["user_img_url"]

        if post_json.get('source'):
            self.source = post_json["source"]
        else:
            self.source = post_json["type"]

        self.up_votes = post_json["up_votes"]
        self.user_id = post_json["user_id"]
        self.username = post_json["username"]
        self.place_name = post_json["place_name"]

        if post_json.get("user_profile_url"):
            self.user_profile_url = post_json["user_profile_url"]
        else:
            self.user_profile_url = User().get_profile_url(userid = self.user_id, source=self.source, username=self.username)

        self.coord = post_json["coord"]
    def get_as_dict(self):
        d = {"doc_id": self.doc_id, "post_id": self.post_id, "text": self.text, "created": self.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
             "content_img_url": self.content_img_url, "user_img_url":self.user_img_url, "source": self.source,
             "up_votes": self.up_votes, "user_id": self.user_id, "place_name": self.place_name,
             "user_profile_url": self.user_profile_url, "coord": self.coord, "username": self.username}
        return d
class Feed_Content():
    '''Provides feed content'''
    def get_random_feed(self, from_datetime, q_from, q_size, encoded_tags, radius, sort):
        f = Feed()
        data = []
        result = json.loads(f.get_random_feed(from_datetime, q_from, q_size, encoded_tags, radius, sort))
        if result["hits"]["total"] > 0:
            for p in result["hits"]["hits"]:
                field = p["fields"]
                try:
                    url_util = Url()
                    media_url = url_util.get_url_from_string(field.get("content_img_url"))
                    if not media_url:
                        # see if text field has a url in it
                        media_url = url_util.get_url_from_string(field["text"].encode("utf-8"))
                    data.append(Post( p["_id"], field.get("post_id"), field["text"].encode("utf-8"),  Date().get_obj(field.get("@timestamp")), media_url,
                                      field.get("user_img_url"), field.get("type"), field.get("user_id"), field.get("place_name"),
                                      field.get("coord"), field.get("username"), field.get("up_votes")))
                except Exception, e:
                    print str(e), p
                    pass # fetcher engine and logstash must ensure clean data gets into elasticsearch which confirms to the Post object
        return data
    def get_random_feed_as_json(self,from_datetime, q_from, q_size, encoded_tags, radius, sort):
        data = self.get_random_feed(from_datetime, q_from, q_size, encoded_tags, radius, sort)
        return [(d.get_as_dict()) for d in data]
    def get_feed_around_coord(self, from_datetime, coord, q_from, q_size, encoded_tags, radius, sort):
        f = Feed()
        data = []
        result = json.loads(f.get_feed_around_coord(from_datetime, coord, q_from, q_size, encoded_tags, radius, sort))
        if result["hits"]["total"] > 0:
            for p in result["hits"]["hits"]:
                field = p["fields"]
                try:
                    url_util = Url()
                    media_url = url_util.get_url_from_string(field.get("content_img_url"))
                    if not media_url:
                        # see if text field has a url in it
                        media_url = url_util.get_url_from_string(field.get("text").encode("utf-8"))
                    data.append(Post( p["_id"], field.get("post_id"), field.get("text").encode("utf-8"), Date().get_obj(field.get("@timestamp")),
                                      media_url, field.get("user_img_url"), field.get("type"), field.get("user_id"),
                                      field.get("place_name"), field.get("coord"), field.get("username"), field.get("up_votes")))
                except Exception, e:
                    print str(e), p
                    pass # fetcher engine and logstash must ensure clean data gets into elasticsearch which confirms to the Post object
        return data
    def get_popular_around_coord(self, from_datetime, coord, q_from, q_size, encoded_tags, radius, sort, source):
        f = Feed()
        data = []
        result = json.loads(f.get_popular_around_coord(from_datetime, coord, q_from, q_size, encoded_tags, radius, sort, source))
        if result["hits"]["total"] > 0:
            for p in result["hits"]["hits"]:
                field = p["fields"]
                try:
                    url_util = Url()
                    media_url = url_util.get_url_from_string(field.get("content_img_url"))
                    if not media_url:
                        # see if text field has a url in it
                        media_url = url_util.get_url_from_string(field.get("text").encode("utf-8"))
                    data.append(Post( p["_id"], field.get("post_id"), field.get("text").encode("utf-8"), Date().get_obj(field.get("@timestamp")),
                                      media_url, field.get("user_img_url"), field.get("type"), field.get("user_id"),
                                      field.get("place_name"), field.get("coord"), field.get("username"), field.get("up_votes")))
                except Exception, e:
                    print str(e), p
                    pass # fetcher engine and logstash must ensure clean data gets into elasticsearch which confirms to the Post object
        return data
    def get_feed_around_coord_as_json(self, from_datetime, coord, q_from, q_size, encoded_tags, radius, sort):
        data = self.get_feed_around_coord(from_datetime, coord, q_from, q_size, encoded_tags, radius, sort)
        return [(d.get_as_dict()) for d in data]
    def get_popular_around_coord_as_json(self, from_datetime, coord, q_from, q_size, encoded_tags, radius, sort, source):
        data = self.get_popular_around_coord(from_datetime, coord, q_from, q_size, encoded_tags, radius, sort, source)
        return [(d.get_as_dict()) for d in data]
    def increment_upvote(self,data, increment):
        '''this method should be removed in future when post object is being passed everywhere'''
        if data.get("up_votes"):
            data["up_votes"] = int(data["up_votes"]) + increment
        else:
            data["up_votes"] = increment
        return data
    def get_post_by_id(self, doc_id):
        d = Feed().get_by_document_id(doc_id)
        if (json.loads(d)["hits"]["total"] == 0):
            return None
        else:
            return json.loads(d)["hits"]["hits"][0]
    def like_post(self, document_id, increment):
        f = Feed()
        data = self.get_post_by_id(document_id)
        if not data:
            return None
        else:
            d_index = data["_index"]
            d_doctype = data["_type"]
            d_id = document_id
            fields = data["fields"]
            fields = self.increment_upvote(fields, increment)
        f.delete_by_document_id(d_index, d_doctype, d_id)
        f.create_document(index_name = d_index, doc_type = d_doctype, document_id = d_id, json_body = json.dumps(fields))
    def delete_post(self, document_id):
        f = Feed()
        data = self.get_post_by_id(document_id)
        if not data:
            return False
        else:
            d_index = data["_index"]
            d_doctype = data["_type"]
            d_id = document_id
        f.delete_by_document_id(d_index, d_doctype, d_id)
        return True
    def put_native_post(self, lat, lon, text, image_data_url, file_extn, cityname):
        f = Feed()
        user_id = 0
        username = 'native'
        current_utc = Date().get_utcnow_str()
        filename = '{0}_{1}.{2}'.format(user_id, Date().get_utcnow_number(), file_extn)
        img_url = '/native/uploads/{0}/'.format(filename)
        uploaded_img_url = '/static/uploads/{0}'.format(filename)
        if Img().save(uploaded_img_url, image_data_url):
            f.create_native_document(user_id, '/static/images/user_placeholder.png', text, lat, lon, current_utc,
                                     cityname, img_url, username)
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
