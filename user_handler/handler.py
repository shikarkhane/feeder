'''
Created on Oct 3, 2013

@author: nikhil
'''
import tornado.web
from models import Subscribe_Updates
import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class SubscriberHandler(tornado.web.RequestHandler):
    '''
    add emails to subscription list, for sending updates and new features info
    '''
    def post(self, email, q_lat=0, q_lon=0):
        try:
            s = Subscribe_Updates()
            r = s.add_email(email, q_lat, q_lon)
            self.write(str(r))
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
    def delete(self, email):
        try:
            s = Subscribe_Updates()
            r = s.remove_email(email)
            self.write(str(r))
        except Exception,e:
            logging.exception(e)
            self.render("oops.html")
