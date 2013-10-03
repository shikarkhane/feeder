from social_feed.feed import Feed
import json
import time

class Post():
    '''
    Many posts constitute a feed. 
    '''
    def __init__(self, post_id, text, created, content_img_url, user_img_url, source ):
        self.post_id = post_id
        self.text = text
        self.created = created
        self.content_img_url = content_img_url
        self.user_img_url = user_img_url
        self.source = source

class Feed_Content():
    '''Provides feed content'''
    def get_random_feed(self):
        f = Feed()
        data = []
        result = json.loads(f.get_random_feed())
        for i in result["hits"]["hits"]:
            tweet = i["_source"]
            try:
                data.append(Post( int(tweet["id"]), str(tweet["text"]),  time.strptime(tweet["@timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ'), tweet.get("entities").get("media_url"), tweet.get("user").get("profile_image_url"), "Twitter"))
            except:
                pass # fetcher engine and logstash must ensure clean data gets into elasticsearch which confirms to the Post object
        return data