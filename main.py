import tornado.ioloop
import config
from web_handler.handler import GeoHandler, MainHandler, PreHandler, BackofficeHandler, HelperHandler, LikeHandler, NewHandler
import settings


application = tornado.web.Application([
    (r"/", PreHandler), (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/", MainHandler), 
    (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/tags/(\S+)/", MainHandler), 
    (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/location/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/", GeoHandler), 
    (r"/time/([0-9]+)/from/([0-9]+)/pagesize/([0-9]+)/location/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/tags/(\S+)/", GeoHandler),
    (r"/backoffice/([0-9]+)/", BackofficeHandler),
    (r"/we/([a-zA-Z0-9]+)/", HelperHandler),
    (r"/like/(\S+)/", LikeHandler),
    (r"/new/", NewHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path =  settings.TEMPLATE_PATH)

if __name__ == "__main__":
    #create config file
    config.create_config_file("mainkey","mainvalue")
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()