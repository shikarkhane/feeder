'''
Created on Oct 3, 2013

@author: nikhil
'''
import tornado.web
from models import Feed_Content


# class BaseHandler(tornado.web.RequestHandler):
#     def get_current_user(self):
#         pass
# #         user_json = self.get_secure_cookie("chatdemo_user")
# #         if not user_json: return None
# #         return tornado.escape.json_decode(user_json)
    
class MainHandler(tornado.web.RequestHandler):
    '''
    non geo handler
    '''
    def get(self, q_from=0):
        page_size = 10
        link_from = int(q_from) + page_size + 1
        next_link = "/from/{0}/".format(link_from)
        f = Feed_Content()
        posts = f.get_random_feed(q_from, page_size)
        self.render("feed.html",next_link = next_link, posts=posts)
class GeoHandler(tornado.web.RequestHandler):
    '''
    handler to find data around coordinates
    '''
    def get(self, latitude, longitude, q_from=0):
        page_size = 10
        link_from = int(q_from) + page_size + 1
        next_link = "/{1}/{2}/from/{0}/".format(link_from, latitude, longitude)
        f = Feed_Content()
        coord = [latitude,longitude]
        posts = f.get_feed_around_coord( coord , q_from, page_size)
        self.render("feed.html",next_link = next_link, posts=posts)
        