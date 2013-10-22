import tornado.ioloop
import config
from web_handler import handler
import settings


application = tornado.web.Application([
    (r"/", handler.MainHandler), (r"/from/([0-9]+)/", handler.MainHandler), (r"/(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)/from/([0-9]+)/", handler.GeoHandler),
], debug=settings.DEBUG, static_path = settings.STATIC_PATH, template_path =  settings.TEMPLATE_PATH)

if __name__ == "__main__":
    #create config file
    config.create_config_file("mainkey","mainvalue")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()