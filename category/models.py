import json
import settings
import logging
from backend.category import _Category
from common.utility import Date

# Log everything, and send it to stderr.
logging.basicConfig(filename=settings.DEBUG_LOG,level=logging.ERROR,format='%(asctime)s %(message)s')

class Category():
    def __init__(self):
        self.LIST = {}
    def make_list(self, source):
        # convert multiple {u'category_id': u'1221', u'category_name': u'TRHEME'} to { "TRHEME" : 1221, ...}
        self.LIST[source['category_name']] = int(source['category_id'])
    def get_all(self):
        c = _Category()
        r = json.loads(c.get_all())
        e = ''
        if r["hits"]["total"] > 0:
            for p in r["hits"]["hits"]:
                self.make_list(p['_source'])
        return self.LIST
    def get_key(self, value):
        self.get() # todo cache the LIST Object, to reduce elasticsearch calls and dubious calls.
        for k, v in self.LIST.items():
            if v == value:
                return k
        return 0
    def add(self, category_name):
        c = _Category()
        if not c.exists_by_category_name(category_name):
            c.add(Date().get_epoch(), category_name)
    def delete(self, category_name):
        c = _Category()
        if c.exists_by_category_name(category_name):
            c.remove_by_category_name(category_name)
