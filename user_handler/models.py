from backend.subscriber import Subscribe
import json

class Subscribe_Updates():
    def add_email(self, email):
        s = Subscribe()
        if not s.exists(email):
            r = json.loads(s.add(email))
            return r['ok']
        return False
    def remove_email(self, email):
        s = Subscribe()
        r = json.loads(s.remove_by_email(email))
        return r['ok']



