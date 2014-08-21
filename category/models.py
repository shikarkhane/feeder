import settings
import logging

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class Category():
    LIST = {"Alert" : 1, "Gossip" : 2, "Discount" : 3}
    def get(self):
        return self.LIST
    def get_key(self, value):
        for k, v in self.LIST.items():
            if v == value:
                return k
        return 0