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
    def get(self, q_from=0, q_page_size = 10, q_encoded_tags=None):
        if int(q_page_size) > 50:
            q_page_size = 50
        f = Feed_Content()
        posts = f.get_random_feed_as_json(q_from, q_page_size, q_encoded_tags)
        self.write(json.dumps(posts))
        #self.render("feed.html",next_link = next_link, posts=posts)
class GeoHandler(tornado.web.RequestHandler):
    '''
    handler to find data around coordinates
    '''
    def get(self, q_latitude, q_longitude, q_from=0, q_page_size = 10, q_encoded_tags=None):
        if int(q_page_size) > 50:
            q_page_size = 50
        f = Feed_Content()
        coord = [q_latitude,q_longitude]
        posts = f.get_feed_around_coord_as_json( coord , q_from, q_page_size, q_encoded_tags)
        self.write(json.dumps(posts))
        #self.render("feed.html",next_link = next_link, posts=posts)
        