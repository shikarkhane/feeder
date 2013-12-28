import tornado.ioloop
import config
from web_handler.handler import GeoHandler, MainHandler, PreHandler
import settings


application = tornado.web.Application([
    (r"/", PreHandler), (r"/from/([0-9]+)/pagesize/([0-9]+)/", MainHandler), (r"/from/([0-9]+)/pagesize/([0-9]+)/tags/(\S+)/", MainHandler), 
    (r"/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/from/([0-9]+)/pagesize/([0-9]+)/", GeoHandler), (r"/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/from/([0-9]+)/pagesize/([0-9]+)/tags/(\S+)/", GeoHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path =  settings.TEMPLATE_PATH)

if __name__ == "__main__":
    #create config file
    config.create_config_file("mainkey","mainvalue")
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()