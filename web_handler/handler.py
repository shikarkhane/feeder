'''
Created on Oct 3, 2013

@author: nikhil
'''
import tornado.web
from models import Feed_Content
import time

# class BaseHandler(tornado.web.RequestHandler):
#     def get_current_user(self):
#         pass
# #         user_json = self.get_secure_cookie("chatdemo_user")
# #         if not user_json: return None
# #         return tornado.escape.json_decode(user_json)
    
class MainHandler(tornado.web.RequestHandler):
    '''
    all the website (non-mobile) handlers are here
    '''
    def get(self):
        f = Feed_Content()
        posts = f.get_random_feed()
        self.render("feed.html", posts=posts)
        
        