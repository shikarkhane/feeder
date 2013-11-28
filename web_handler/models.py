from social_feed.feed import Feed
import json
import datetime
from common.utility import Url_Handler

class Post():
    '''
    Many posts constitute a feed. 
    Json example of a post:
{
               "text" => "Euw folk i min klass euw",
               "lang" => "nl",
         "@timestamp" => "2013-10-15T10:27:02.000Z",
               "type" => "twitter",
            "post_id" => 390061246474911745,
           "up_votes" => 0,
       "user_img_url" => "http://a0.twimg.com/profile_images/378800000568858024/f8ce9b2482ad43b8cdf13d40517e0ce6_normal.jpeg",
    "content_img_url" => "%{[entities][media_url]}",
              "coord" => "15.13412991,58.32243012",
}
    '''
    def __init__(self, post_id, text, created, content_img_url, user_img_url, source ):
        # post_id is the internal _id of elasticsearch store
        self.post_id = post_id
        self.text = text
        self.created = created
        self.content_img_url = content_img_url
        self.user_img_url = user_img_url
        self.source = source
        #self.coord = coord 
class Feed_Content():
    '''Provides feed content'''
    def get_random_feed(self, q_from, q_size):
        f = Feed()
        data = []
        result = json.loads(f.get_random_feed(q_from, q_size))
        #result = json.loads("""{"took":6,"timed_out":false,"_shards":{"total":1,"successful":1,"failed":0},"hits":{"total":8,"max_score":1.0,"hits":[{"_index":"logstash-2013.11.28","_type":"twitter","_id":"XEj4bP3kRz-Tv7OO8gfYfA","_score":1.0,"fields":{"coord":"59.36463617,17.97595649","content_img_url":"%{[entities][media_url]}","@timestamp":"2013-11-28T11:26:52.152Z","text":"@Superfelle Du kommer inte palla. Tro mig. Jag vet. Satsa psemester istllet. Mer lagom.","user_img_url":"http://pbs.twimg.com/profile_images/378800000396646424/d379545fb4c2f8c26d32539a5e06b8b7_normal.jpeg","type":"twitter","post_id":406020951659515904}},{"_index":"logstash-2013.11.28","_type":"twitter","_id":"VdqdRaNPTV-fXa11tZ1o0g","_score":1.0,"fields":{"coord":"60.61779726,15.64002106","content_img_url":"%{[entities][media_url]}","@timestamp":"2013-11-28T11:33:21.176Z","text":"no more tequila shots ngonsin","user_img_url":"http://pbs.twimg.com/profile_images/378800000689913299/36c7154748b0bc89c3cfd65898cd8ae8_normal.jpeg","type":"twitter","post_id":406022957597995008}},{"_index":"logstash-2013.11.28","_type":"twitter","_id":"gaNFJU4VRVCEJMPjFxPWhw","_score":1.0,"fields":{"coord":"61.7274155,17.12363918","content_img_url":"%{[entities][media_url]}","@timestamp":"2013-11-28T11:35:25.856Z","text":"Vi ska skriva om ett band p musiken och jag frgade en kompis om jag skulle ha broder Daniel eller Ebba grn ocks kom typ en extralrare &gt;","user_img_url":"http://pbs.twimg.com/profile_images/378800000799063369/b3204bb19a028d4951be3911fdcf269e_normal.jpeg","type":"twitter","post_id":406022968763240448}},{"_index":"logstash-2013.11.28","_type":"twitter","_id":"7m-gv8qxTiCfgGpTT0F2cA","_score":1.0,"fields":{"coord":"65.5743726,22.099408","content_img_url":"%{[entities][media_url]}","@timestamp":"2013-11-28T11:36:53.148Z","text":"\"Stinkande chili hejdad i Los Angeles\" http://t.co/uCD1iJ9Qpw via @svtnyheter","user_img_url":"http://pbs.twimg.com/profile_images/378800000792504774/1f6a0dd0d23c26e5d8591a771467554c_normal.jpeg","type":"twitter","post_id":406022976518500352}},{"_index":"logstash-2013.11.28","_type":"twitter","_id":"1B-JS43iSRCYRby_7vo_sQ","_score":1.0,"fields":{"coord":"57.72013216,12.01712647","content_img_url":"%{[entities][media_url]}","@timestamp":"2013-11-28T11:38:54.803Z","text":"Uncle acid &amp; Back Sabbath i fredags, Ghost i tisdags och Horisont p lrdag. r en tvttkta hadegttare!","user_img_url":"http://pbs.twimg.com/profile_images/2998825616/67bf0c7da6ffcf003b763cc6eff9cc33_normal.jpeg","type":"twitter","post_id":406023958497337345}},{"_index":"logstash-2013.11.28","_type":"twitter","_id":"2WP-2M2VRWK4Y_7w92uWBw","_score":1.0,"fields":{"coord":"60.6764418,17.14186737","content_img_url":"%{[entities][media_url]}","@timestamp":"2013-11-28T11:42:22.458Z","text":"Snyggaste jag sett p lnge","user_img_url":"http://pbs.twimg.com/profile_images/378800000720827389/9bd93bc4fde3646adc01cafb7b92e2e0_normal.jpeg","type":"twitter","post_id":406024878064926720}},{"_index":"logstash-2013.11.28","_type":"twitter","_id":"3wBQlduGTBu05VDy7DfBTA","_score":1.0,"fields":{"coord":"62.0392131,14.3555889","content_img_url":"%{[entities][media_url]}","@timestamp":"2013-11-28T11:46:53.610Z","text":"I'd give anything to make people happy\n\n#mtvstars Justin Bieber","user_img_url":"http://pbs.twimg.com/profile_images/378800000766718042/6c47eadb7768426e917232a1ebf40b39_normal.png","type":"twitter","post_id":406025849096658944}},{"_index":"logstash-2013.11.28","_type":"twitter","_id":"iHiNUWlXQhKPSKjPCGF97w","_score":1.0,"fields":{"coord":"57.70005058,11.96351736","content_img_url":"%{[entities][media_url]}","@timestamp":"2013-11-28T11:53:57.156Z","text":"Lyssnade p tv snubbar somdiskuterade vlfrdspol, den ene vnster den andre hger. Alltid lika kul att iaktta sandldeniv.","user_img_url":"http://pbs.twimg.com/profile_images/378800000719001712/a01f8125393c9f4f693db8b7d6d04981_normal.jpeg","type":"twitter","post_id":406027015188676609}}]}}""")
        if result["hits"]["total"] > 0:
            for p in result["hits"]["hits"]:
                field = p["fields"]
                try:
                    url_util = Url_Handler()
                    media_url = url_util.get_url_from_string(field.get("content_img_url"))
                    if not media_url:
                        # see if text field has a url in it
                        media_url = url_util.get_url_from_string(field.get("text"))
                    data.append(Post( p["_id"], field.get("text").encode('utf-8'),  datetime.datetime.strptime(field.get("@timestamp"), '%Y-%m-%dT%H:%M:%S.%fZ'), media_url, field.get("user_img_url"), field.get("type")))
                except Exception, e:
                    print str(e), p
                    pass # fetcher engine and logstash must ensure clean data gets into elasticsearch which confirms to the Post object
        return data
    def get_feed_around_coord(self, coord, q_from, q_size):
        f = Feed()
        data = []
        result = json.loads(f.get_feed_around_coord(coord, q_from, q_size))
        if result["hits"]["total"] > 0:
            for p in result["hits"]["hits"]:
                field = p["fields"]
                try:
                    url_util = Url_Handler()
                    media_url = url_util.get_url_from_string(field.get("content_img_url"))
                    if not media_url:
                        # see if text field has a url in it
                        media_url = url_util.get_url_from_string(field.get("text"))
                    data.append(Post( p["_id"], field.get("text").encode('utf-8'),  datetime.datetime.strptime(field.get("@timestamp"), '%Y-%m-%dT%H:%M:%S.%fZ'), media_url, field.get("user_img_url"), field.get("type")))
                except Exception, e:
                    #print str(e), tweet
                    pass # fetcher engine and logstash must ensure clean data gets into elasticsearch which confirms to the Post object
        return data