'''
Created on Oct 3, 2013

@author: nikhil
'''
import tornado.web
import tornado.auth
import tornado.escape
import json
import urllib2
import urllib
from models import Feed_Content, Backoffice_content
import settings
 
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            l = '/we/login/?next={0}'.format(urllib.quote_plus(str(self.request.uri)))
            self.redirect(l)
 
class PreHandler(tornado.web.RequestHandler):
    '''
    first load to get the basic template, javascripts etc loaded
    '''
    def get(self):
        self.render("feed.html")
class NewHandler(BaseHandler):
    '''
    native tipoff post
    '''
    def get(self):
        email = tornado.escape.xhtml_escape(self.current_user["email"])
        if not email:
            self.render('must-login.html')
        else:
            self.render("native-post.html")
    def post(self, q_latitude, q_longitude, q_encoded_text ):
        email = tornado.escape.xhtml_escape(self.current_user["email"])
        if not email:
            self.render('must-login.html')
        else:
            img_data = self.request.files['image'][0]['body']
            extn = str(self.request.files['image'][0]['content_type']).split('/')[1]
            f = Feed_Content()
            f.put_native_post(q_latitude, q_longitude, q_encoded_text, img_data, extn)
            self.write('Tipoff uploaded!')
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
class BackofficeHandler(BaseHandler):
    '''
    tipoff admin page
    '''
    def get(self):
        email = tornado.escape.xhtml_escape(self.current_user["email"])
        if email not in settings.ADMIN_EMAILS:
            self.render('denied.html')
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

class GoogleHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        ## set user in cookie
        self.set_secure_cookie('user', tornado.escape.json_encode(user))
        if self.get_cookie("mypagebeforelogin"):
            self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
        else:
            self.redirect('/')
class TwitterHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")

        ## set identity in cookie
        self.set_secure_cookie('user', tornado.escape.json_encode(user))
        if self.get_cookie("mypagebeforelogin"):
            self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
        else:
            self.redirect('/')
class FacebookHandler(tornado.web.RequestHandler, tornado.auth.FacebookMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("session", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Facebook auth failed")
        ## set identity in cookie
        self.set_secure_cookie('user', tornado.escape.json_encode(user))
        if self.get_cookie("mypagebeforelogin"):
            self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
        else:
            self.redirect('/')
