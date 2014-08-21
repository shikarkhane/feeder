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
from backend.fetcher import Fetcher
import logging
from category.models import Category
# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            l = '/we/login/?next={0}'.format(urllib.quote_plus(str(self.request.uri)))
            self.redirect(l)

class PageNotFoundHandler(tornado.web.RequestHandler):
    '''
    page not found
    '''
    def get(self):
        try:
            self.render("page-not-found.html")
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class PreHandler(tornado.web.RequestHandler):
    '''
    first load to get the basic template, javascripts etc loaded
    '''
    def get(self):
        try:
            self.render("firsttimeuser.html")
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class NewHandler(BaseHandler):
    '''
    native tipoff post
    '''
    def get(self):
        try:
            email = None
            if self.current_user:
                email = tornado.escape.xhtml_escape(self.current_user["email"])
            if not email:
                self.render("must-login.html")
            else:
                self.render("native-post.html")
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
    def post(self, q_latitude, q_longitude, q_encoded_text, q_city_name):
        try:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
            if not email:
                self.render('must-login.html')
            else:
                img_data = self.request.files['image'][0]['body']
                extn = str(self.request.files['image'][0]['content_type']).split('/')[1]
                f = Feed_Content()
                f.put_native_post(q_latitude, q_longitude, q_encoded_text, img_data, extn, q_city_name)
                self.write('Tipoff uploaded!')
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class ShowPostHandler(tornado.web.RequestHandler):
    '''returns json with details of given doc id'''
    def get(self, doc_id):
        try:
            fc = Feed_Content()
            can_delete = False
            try:
                user_json = self.get_secure_cookie("user")
                if user_json:
                    email = tornado.escape.json_decode(user_json)['email']
                    if email in settings.ADMIN_EMAILS:
                        can_delete = True
            except Exception, e:
                logging.exception(e)
                can_delete = False
            d = fc.get_post(doc_id)
            if d:
                self.render('post.html', post=d, can_delete= can_delete, categories = Category().get(),
                            selected_category_label= Category().get_key(d.category_id))
            else:
                self.render('page-not-found.html')
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class MainHandler(tornado.web.RequestHandler):
    '''
    non geo handler
    '''
    def get(self, q_from_datetime, q_from=0, q_page_size = 10, q_radius = 10, q_sort=0, q_filterdays=30, q_encoded_tags=None):
        try:
            if int(q_page_size) > 50:
                q_page_size = 50
            f = Feed_Content()
            posts = f.get_random_feed_as_json(q_from_datetime, q_from, q_page_size, q_encoded_tags, int(q_radius),
                                              int(q_sort), int(q_filterdays))
            self.write(json.dumps(posts))
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class GeoHandler(tornado.web.RequestHandler):
    '''
    handler to find data around coordinates
    '''
    def get(self, q_from_datetime, q_from=0, q_page_size = 10, q_radius = 10, q_sort=0, q_filterdays=30, q_latitude = 58,
            q_longitude = 16, q_encoded_tags=None):
        try:
            if int(q_page_size) > 50:
                q_page_size = 50
            f = Feed_Content()
            coord = [q_latitude,q_longitude]
            posts = f.get_feed_around_coord_as_json( q_from_datetime, coord , q_from, q_page_size, q_encoded_tags,
                                                     int(q_radius), int(q_sort), int(q_filterdays))
            if (len(posts) == 0) and (q_from == 0):
                # register coord with fetcher to fetch data, if for the first page no data was returned
                Fetcher(q_latitude, q_longitude).add()
            self.write(json.dumps(posts))
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

class PopularHandler(tornado.web.RequestHandler):
    '''
    handler to find popular data around coordinates
    '''
    def get(self, q_from_datetime, q_from=0, q_page_size = 10, q_radius = 10, q_sort=0, q_filterdays=30,
            q_latitude = 58, q_longitude = 16, q_source='instagram'):
        try:
            if int(q_page_size) > 50:
                q_page_size = 50
            f = Feed_Content()
            coord = [q_latitude,q_longitude]
            posts = f.get_popular_around_coord_as_json( q_from_datetime, coord , q_from, q_page_size, None,
                                                     int(q_radius), 0, q_source, int(q_filterdays))
            self.write(json.dumps(posts))
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

class BOHandler(BaseHandler):
    '''
    tipoff admin page
    '''
    def get(self):
        try:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
            if email not in settings.ADMIN_EMAILS:
                self.render('denied.html')
            bo = Backoffice_content()
            result = bo.get_last_1day_period_activity()
            #self.write(json.dumps(result))
            self.render("backoffice.html", activity=result)
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

class BOCookiesHandler(BaseHandler):
    '''
    tipoff admin page
    '''
    def get(self):
        try:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
            if email not in settings.ADMIN_EMAILS:
                self.render('denied.html')
            self.render("bo_cookies.html")
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class BOCategoryHandler(BaseHandler):
    '''
    add or remove master list of categories
    '''
    def get(self):
        try:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
            if email not in settings.ADMIN_EMAILS:
                self.render('denied.html')
            c = Category()
            result = c.get()
            #self.write(json.dumps(result))
            self.render("bo_category.html", categories=result)
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
    def post(self):
        try:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
            if email in settings.ADMIN_EMAILS:
                m = Category
                m.add(self.request.files['category_name'])
            self.write('New Category added!')
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
    def delete(self):
        try:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
            if email in settings.ADMIN_EMAILS:
                m = Category
                m.delete(self.request.files['category_name'])
            self.write('Category deleted!')
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class HelperHandler(tornado.web.RequestHandler):
    '''
    renders static html pages like help, about us, privacy etc
    '''
    def get(self, pagename):
        try:
            self.render("{0}.html".format(pagename))
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class LikeHandler(tornado.web.RequestHandler):
    '''
    like a tipoff
    '''
    def get(self, document_id, increment):
        try:
            increment = int(increment)
            m = Feed_Content()
            m.like_post(document_id, increment)
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class DeleteHandler(BaseHandler):
    '''
    delete a tipoff
    '''
    def get(self, document_id):
        try:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
            if email in settings.ADMIN_EMAILS:
                m = Feed_Content()
                m.delete_post(document_id)
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class CategoryHandler(BaseHandler):
    '''
    set a category for a post
    '''
    def post(self, document_id, category_id):
        try:
            email = tornado.escape.xhtml_escape(self.current_user["email"])
            if email in settings.ADMIN_EMAILS:
                m = Feed_Content()
                m.categorize_post(document_id, category_id)
            self.write('Categorized!')
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
class GoogleHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        try:
            if self.get_argument("openid.mode", None):
                self.get_authenticated_user(self.async_callback(self._on_auth))
                return
            self.authenticate_redirect()
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

    def _on_auth(self, user):
        try:
            if not user:
                raise tornado.web.HTTPError(500, "Google auth failed")
            ## set user in cookie
            self.set_secure_cookie('user', tornado.escape.json_encode(user))
            if self.get_cookie("mypagebeforelogin"):
                self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
            else:
                self.redirect('/')
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

class TwitterHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        try:
            if self.get_argument("oauth_token", None):
                self.get_authenticated_user(self.async_callback(self._on_auth))
                return
            self.authenticate_redirect()
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

    def _on_auth(self, user):
        try:
            if not user:
                raise tornado.web.HTTPError(500, "Twitter auth failed")

            ## set identity in cookie
            self.set_secure_cookie('user', tornado.escape.json_encode(user))
            if self.get_cookie("mypagebeforelogin"):
                self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
            else:
                self.redirect('/')
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

class FacebookHandler(tornado.web.RequestHandler, tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        try:
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
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

    def _on_login(self, user):
        # user object looks like this
        # {'picture': {u'data': {u'url': u'https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash3/t5/573505_529255170_1940698750_q.jpg', u'is_silhouette': False}},
        # 'first_name': u'Nikhil', 'last_name': u'Shikarkhane', 'name': u'Nikhil Shikarkhane', 'locale': u'en_US', 'session_expires': ['5183367'],
        # 'access_token': 'CAAC2deiekxkBANnwk5LicmYU8DID5R14hgqF9CDCpkZAgTM1dhESPcJVaX4VeYmco0QrlomZBqrDEcf24jeRKwk0yoHTZAwilfZBRrZC0qQrdlurdYgHj1pMCtDeNvBotnV9L0DWBZCNHSYcho9OEPDZBOCZCqyZBgOa8Gli72fYAWZCJMYhUXS8T6', 'link': u'https://www.facebook.com/shikarkhane', 'id': u'529255170'}
        try:
            if not user:
                raise tornado.web.HTTPError(500, "Facebook auth failed")
            ## set identity in cookie
            self.facebook_request("/me", access_token=user["access_token"], callback=self._save_user_profile)
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")

    def _save_user_profile(self, user):
        try:
            if not user:
                raise tornado.web.HTTPError(500, "Facebook authentication failed.")
            self.set_secure_cookie('user', tornado.escape.json_encode(user))
            if self.get_cookie("mypagebeforelogin"):
                self.redirect(str(urllib2.unquote(self.get_cookie("mypagebeforelogin"))))
            else:
                self.redirect('/')
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
