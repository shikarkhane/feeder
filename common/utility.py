'''
Created on Oct 22, 2013

@author: nikhil
'''
class Url_Handler():
    def get_url_from_string(self, string_with_url):
        x = str(string_with_url)
        if x.find("http") == -1:
            return None
        e = x.rfind(" ", x.find("http"))
        x = x[x.find("http") : (len(x) if e == -1 else e )]
        return x
