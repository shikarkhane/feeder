'''
Created on Oct 22, 2013

@author: nikhil
'''
import re 

class Url_Handler():
    def get_url_from_string(self, string_with_url):
        x = str(string_with_url)
        if x.find("http") == -1:
            return None
        return str(re.search("""(?P<url>https?://[^\s|"|']+)""", x).group("url"))

            