import json
import settings
import logging
from backend.category import _Category
from common.utility import Date
import operator

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
class Classify():
    '''simple feature extraction'''
    def __init__(self):
        content = '{}'
        with open(settings.FEATURE_SET, 'r') as ff:
            c = ff.read()
            if c:
                content = c
        self.feature_set = json.loads(content)
    def get_feature_set(self):
        return self.feature_set
    def add_feature_to_category(self, category, feature, weight = 1):
        if not self.feature_set.get(category):
            self.feature_set[category] = {"features":[], "weight":1}
        self.feature_set[category]["features"].append(feature)
        self.feature_set[category]["weight"] = weight
        self.save_feature_set()
    def save_feature_set(self):
        with open(settings.FEATURE_SET, 'w') as ff:
            ff.write(json.dumps(self.feature_set))
    def word_exists_in_category_features(self, category, w):
        if w in self.feature_set[category]["features"]:
            return self.feature_set[category]["weight"]
        else:
            return 0
    def evaluate_category(self, category_score):
        category='gossip'
        if category_score:
            category = max(category_score.iteritems(), key=operator.itemgetter(1))[0]
        return category
    def get_category_for_text(self, text):
        wordlist = text.split(" ")
        category_score = {}
        for word in wordlist:
            for key in self.feature_set.keys():
                wgt = self.word_exists_in_category_features(category=key, w=word)
                if not category_score.get(key):
                    category_score[key] = wgt
                else:
                    category_score[key] = category_score[key] + wgt
        return self.evaluate_category(category_score=category_score)



