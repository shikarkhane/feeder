'''
Created on Oct 22, 2013

@author: nikhil
'''
import re
from datetime import datetime 
import settings
import urllib2
import json
import string
import random

class User():
    def get_profile_url(self, userid, username, source):
        if (source == 'twitter'):
            return '''https://twitter.com/intent/user?user_id={0}'''.format(userid)
        elif (source == 'instagram'):
            return 'http://instagram.com/{0}/'.format(username)
        else:
            return '''/'''
class Url():
    def get_url_from_string(self, string_with_url):
        x = str(string_with_url)
        if x.find("upload") != -1:
            return x
        if x.find("http") == -1:
            return None
        else:
            return str(re.search("""(?P<url>https?://[^\s|"|']+)""", x).group("url"))
class Img():
    def save(self, img_file_path, img_data):
        try:
            with open(settings.DIRNAME + img_file_path ,'w') as f:
                f.write(img_data)
                return True
        except Exception as e:
            return False
class Location():
    def lookup_city(self, lat, lon):
        reverse_api_url = '''http://maps.googleapis.com/maps/api/geocode/json?latlng={0},{1}&sensor=true'''.format(lat, lon)
        req = urllib2.Request(reverse_api_url)
        out = urllib2.urlopen(req)
        result = json.loads(out.read())
        if result["status"] == 'OK':
            subl = [(c["address_components"]) for c in result["results"] if "sublocality" in c["types"]]
            city = [(i["short_name"]) for i in subl[0] if i["types"][0] == "sublocality"][0]
            return city
        else:
            return 'Nearby!'
class Date():
    '''to keep the same format all over the site'''
    def __init__(self):
        self.format = settings.DATE_FORMAT
    def get_utcnow_str(self):
        return datetime.utcnow().strftime(self.format)
    def get_utcnow_number(self):
        return datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    def get_str(self, obj):
        return obj.strftime(self.format)
    def get_obj(self, date_str):
        return datetime.strptime(date_str, self.format) 

class Random_Data():
    '''methods in this class generate random data for testing'''
    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))