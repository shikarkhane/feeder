import tornado.ioloop
import config
from web_handler import handler

application = tornado.web.Application([
    (r"/", handler.MainHandler),
], debug=True)

if __name__ == "__main__":
    #create config file
    config.create_config_file("mainkey","mainvalue")
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()