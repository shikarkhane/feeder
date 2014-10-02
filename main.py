import tornado.ioloop
from feed_handler.handler import GeoHandler, PreHandler, BOHandler, HelperHandler, LikeHandler, \
    NewHandler, GoogleHandler, TwitterHandler, FacebookHandler, ShowPostHandler,  \
    DeleteHandler, BOCookiesHandler, PageNotFoundHandler, CategoryHandler, BOCategoryHandler
from user_handler.handler import SubscriberHandler
import settings


application = tornado.web.Application([
    (r"/", PreHandler),
    (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/radius/([0-9]{1,3})/sort/([0-1]?)/filterdays/([0-9]{1,3})/location/(\-?\d+(?:\.\d+)?)/(\-?\d+(?:\.\d+)?)/", GeoHandler),
    (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/radius/([0-9]{1,3})/sort/([0-1]?)/filterdays/([0-9]{1,3})/location/(\-?\d+(?:\.\d+)?)/(\-?\d+(?:\.\d+)?)/tags/(\S+)/", GeoHandler),
    (r"/backoffice/home/", BOHandler),
    (r"/backoffice/cookies/", BOCookiesHandler),
    (r"/backoffice/category/", BOCategoryHandler),
    (r"/backoffice/category/(\S+)/", BOCategoryHandler),
    (r"/we/([a-zA-Z0-9]+)/", HelperHandler),
    (r"/like/(\S+)/(\-?[1-9]{1})/", LikeHandler),
    (r"/delete/(\S+)/", DeleteHandler),
    (r"/new/", NewHandler),
    (r"/post/(\S+)/category/([0-9]+)/", CategoryHandler),
    (r"/post/(\S+)/", ShowPostHandler),
    (r"/login/google/", GoogleHandler),
    (r"/login/facebook/", FacebookHandler),
    (r"/login/twitter/", TwitterHandler),
    (r"/new/location/(\-?\d+(?:\.\d+)?)/(\-?\d+(?:\.\d+)?)/text/(\S+)/place/(\S+)/", NewHandler),

    (r"/subscribe/(\w+[\.]?\w+[@]\w+[\.]\w+)/location/(\-?\d+(?:\.\d+)?)/(\-?\d+(?:\.\d+)?)/", SubscriberHandler),
    (r"/subscribe/(\w+[\.]?\w+[@]\w+[\.]\w+)/", SubscriberHandler),
    (r".*", PageNotFoundHandler),

], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path =  settings.TEMPLATE_PATH,
        cookie_secret=settings.COOKIE_SECRET, login_url="/we/login/",
        twitter_consumer_key=settings.TWITTER_CONSUMER_KEY, twitter_consumer_secret=settings.TWITTER_CONSUMER_SECRET,
        facebook_api_key=settings.FACEBOOK_API_KEY, facebook_secret=settings.FACEBOOK_SECRET)

if __name__ == "__main__":
    #create config file
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
