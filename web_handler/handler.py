'''
Created on Oct 3, 2013

@author: nikhil
'''
import tornado.web
import json
from models import Feed_Content


# class BaseHandler(tornado.web.RequestHandler):
#     def get_current_user(self):
#         pass
# #         user_json = self.get_secure_cookie("chatdemo_user")
# #         if not user_json: return None
# #         return tornado.escape.json_decode(user_json)
class PreHandler(tornado.web.RequestHandler):
    '''
    first load to get the basic template, javascripts etc loaded
    '''
    def get(self):
        self.render("feed.html")
class MainHandler(tornado.web.RequestHandler):
    '''
    non geo handler
    '''
    def get(self, q_from=0, encoded_tags=None):
        page_size = 10
        f = Feed_Content()
        posts = f.get_random_feed_as_json(q_from, page_size, encoded_tags)
        self.write(json.dumps(posts))
        #self.render("feed.html",next_link = next_link, posts=posts)
class GeoHandler(tornado.web.RequestHandler):
    '''
    handler to find data around coordinates
    '''
    def get(self, latitude, longitude, q_from=0, encoded_tags=None):
        page_size = 10
        f = Feed_Content()
        coord = [latitude,longitude]
        posts = f.get_feed_around_coord_as_json( coord , q_from, page_size, encoded_tags)
        self.write(json.dumps(posts))
        #self.render("feed.html",next_link = next_link, posts=posts)
        