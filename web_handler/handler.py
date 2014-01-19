'''
Created on Oct 3, 2013

@author: nikhil
'''
import tornado.web
import json
from models import Feed_Content, Backoffice_content
import StringIO


class PreHandler(tornado.web.RequestHandler):
    '''
    first load to get the basic template, javascripts etc loaded
    '''
    def get(self):
        self.render("feed.html")
class NewHandler(tornado.web.RequestHandler):
    '''
    native tipoff post
    '''
    def get(self):
        self.render("native-post.html")
    def post(self, q_latitude, q_longitude, q_encoded_text ):
        img_data = self.request.files['image'][0]['body']
        extn = str(self.request.files['image'][0]['content_type']).split('/')[1]
        f = Feed_Content()
        f.put_native_post(q_latitude, q_longitude, q_encoded_text, img_data, extn)
        self.write('Success')
class MainHandler(tornado.web.RequestHandler):
    '''
    non geo handler
    '''
    def get(self, q_from_datetime, q_from=0, q_page_size = 10, q_radius = 10, q_sort=0, q_encoded_tags=None):
        if int(q_page_size) > 50:
            q_page_size = 50
        f = Feed_Content()
        posts = f.get_random_feed_as_json(q_from_datetime, q_from, q_page_size, q_encoded_tags, int(q_radius), int(q_sort))
        self.write(json.dumps(posts))
        #self.render("feed.html",next_link = next_link, posts=posts)
class GeoHandler(tornado.web.RequestHandler):
    '''
    handler to find data around coordinates
    '''
    def get(self, q_from_datetime, q_from=0, q_page_size = 10, q_radius = 10, q_sort=0, q_latitude = 58, q_longitude = 16, q_encoded_tags=None):
        if int(q_page_size) > 50:
            q_page_size = 50
        f = Feed_Content()
        coord = [q_latitude,q_longitude]
        posts = f.get_feed_around_coord_as_json( q_from_datetime, coord , q_from, q_page_size, q_encoded_tags, int(q_radius), int(q_sort))
        self.write(json.dumps(posts))
        #self.render("feed.html",next_link = next_link, posts=posts)
class BackofficeHandler(tornado.web.RequestHandler):
    '''
    tipoff admin page
    '''
    def get(self, secretcode):
        if (int(secretcode) != 7777):
            return None
        bo = Backoffice_content()
        result = bo.get_last_1day_period_activity()
        #self.write(json.dumps(result))
        self.render("backoffice.html", activity=result)
class HelperHandler(tornado.web.RequestHandler):
    '''
    renders static html pages like help, about us, privacy etc
    '''
    def get(self, pagename):
        self.render("{0}.html".format(pagename))

class LikeHandler(tornado.web.RequestHandler):
    '''
    like a tipoff
    '''
    def get(self, document_id):
        m = Feed_Content()
        m.like_post(document_id)
        