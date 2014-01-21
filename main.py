import tornado.ioloop
import config
from web_handler.handler import GeoHandler, MainHandler, PreHandler, BackofficeHandler, HelperHandler, LikeHandler, \
    NewHandler, GoogleHandler
import settings


application = tornado.web.Application([
    (r"/", PreHandler), (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/radius/([0-9]{1})/sort/([0-1]?)/", MainHandler), 
    (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/radius/([0-9]{1,3})/sort/([0-1]?)/tags/(\S+)/", MainHandler), 
    (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/radius/([0-9]{1,3})/sort/([0-1]?)/location/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/", GeoHandler), 
    (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/radius/([0-9]{1,3})/sort/([0-1]?)/location/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/tags/(\S+)/", GeoHandler),
    (r"/backoffice/([0-9]+)/", BackofficeHandler),
    (r"/we/([a-zA-Z0-9]+)/", HelperHandler),
    (r"/like/(\S+)/", LikeHandler),
    (r"/new/", NewHandler),
    (r"/login/google/", GoogleHandler),
    (r"/new/location/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/text/(\S+)/", NewHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path =  settings.TEMPLATE_PATH,
                                      cookie_secret=settings.COOKIE_SECRET, login_url="/we/login/")

if __name__ == "__main__":
    #create config file
    config.create_config_file("mainkey","mainvalue")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
