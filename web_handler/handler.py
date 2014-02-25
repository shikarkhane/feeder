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
from models import Feed_Content, Backoffice_content, Post
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
        email = None
        if self.current_user:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
        if not email:
            self.render("must-login.html")
        else:
            self.render("native-post.html")
    def post(self, q_latitude, q_longitude, q_encoded_text, q_city_name):
        email = tornado.escape.xhtml_escape(self.current_user["email"])
        if not email:
            self.render('must-login.html')
        else:
            img_data = self.request.files['image'][0]['body']
            extn = str(self.request.files['image'][0]['content_type']).split('/')[1]
            f = Feed_Content()
            f.put_native_post(q_latitude, q_longitude, q_encoded_text, img_data, extn, q_city_name)
            self.write('Tipoff uploaded!')
class NativeImageHandler(tornado.web.RequestHandler):
    '''renders the image file in a nice frame'''
    def get(self, img_file_name):
        self.render('native-img.html', imgpath='/static/uploads/{0}'.format(img_file_name))
class ShowPostHandler(tornado.web.RequestHandler):
    '''returns json with details of given doc id'''
    def get(self, doc_id):
        fc = Feed_Content()
        can_delete = 0
        data = fc.get_post_by_id(doc_id)
        if data:
            d = data["fields"]
            d["doc_id"] = doc_id
            self.render('post.html', post=Post(d))
        else:
            self.render('page-not-found.html')
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
class PopularHandler(tornado.web.RequestHandler):
    '''
    handler to find popular data around coordinates
    '''
    def get(self, q_from_datetime, q_from=0, q_page_size = 10, q_radius = 10, q_sort=0, q_latitude = 58, q_longitude = 16,
            q_source='instagram'):
        if int(q_page_size) > 50:
            q_page_size = 50
        f = Feed_Content()
        coord = [q_latitude,q_longitude]
        posts = f.get_popular_around_coord_as_json( q_from_datetime, coord , q_from, q_page_size, None,
                                                 int(q_radius), 1, q_source)
        self.write(json.dumps(posts))
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
    def get(self, document_id, increment):
        increment = int(increment)
        m = Feed_Content()
        m.like_post(document_id, increment)
class DeleteHandler(BaseHandler):
    '''
    delete a tipoff
    '''
    def get(self, document_id):
        email = tornado.escape.xhtml_escape(self.current_user["email"])
        if email in settings.ADMIN_EMAILS:
            m = Feed_Content()
            m.delete_post(document_id)
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
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")

        ## set identity in cookie
        self.set_secure_cookie('user', tornado.escape.json_encode(user))
        if self.get_cookie("mypagebeforelogin"):
            self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
        else:
            self.redirect('/')
class FacebookHandler(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
      if self.get_argument("code", False):
          self.get_authenticated_user(
            redirect_uri='{0}/login/facebook/'.format(settings.SERVER_NAME),
            client_id=settings.FACEBOOK_API_KEY,
            client_secret=settings.FACEBOOK_SECRET,
            code=self.get_argument("code"),
            callback=self._on_login)
          return
      self.authorize_redirect(redirect_uri='{0}/login/facebook/'.format(settings.SERVER_NAME),
                              client_id=settings.FACEBOOK_API_KEY,
                              extra_params={"scope": "email"})
    def _on_login(self, user):
        # user object looks like this
        # {'picture': {u'data': {u'url': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t5/573505_529255170_1940698750_q.jpg', u'is_silhouette': False}},
        # 'first_name': u'Nikhil', 'last_name': u'Shikarkhane', 'name': u'Nikhil Shikarkhane', 'locale': u'en_US', 'session_expires': ['5183367'],
        # 'access_token': 'CAAC2deiekxkBANnwk5LicmYU8DID5R14hgqF9CDCpkZAgTM1dhESPcJVaX4VeYmco0QrlomZBqrDEcf24jeRKwk0yoHTZAwilfZBRrZC0qQrdlurdYgHj1pMCtDeNvBotnV9L0DWBZCNHSYcho9OEPDZBOCZCqyZBgOa8Gli72fYAWZCJMYhUXS8T6', 'link': u'https://www.facebook.com/shikarkhane', 'id': u'529255170'}
        if not user:
            raise tornado.web.HTTPError(500, "Facebook auth failed")
        ## set identity in cookie
        self.facebook_request("/me", access_token=user["access_token"], callback=self._save_user_profile)
    def _save_user_profile(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Facebook authentication failed.")
        self.set_secure_cookie('user', tornado.escape.json_encode(user))
        if self.get_cookie("mypagebeforelogin"):
            self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
        else:
            self.redirect('/')
