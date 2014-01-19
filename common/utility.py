'''
Created on Oct 22, 2013

@author: nikhil
'''
import re
from datetime import datetime 
import settings

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
            with open(img_file_path ,'w') as f:
                f.write(img_data)
                return True
        except Exception as e:
            return False
class Location():
    def lookup_city(self, lat, lon):
        return 'cityname'
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
