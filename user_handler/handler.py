'''
Created on Oct 3, 2013

@author: nikhil
'''
import tornado.web
from models import Subscribe_Updates

class SubscriberHandler(tornado.web.RequestHandler):
    '''
    add emails to subscription list, for sending updates and new features info
    '''
    def post(self, email):
        s = Subscribe_Updates()
        r = s.add_email(email)
        self.write(str(r))
    def delete(self, email):
        s = Subscribe_Updates()
        r = s.remove_email(email)
        self.write(str(r))