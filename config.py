import ConfigParser

def create_config_file(testkey, testvalue):
    config = ConfigParser.RawConfigParser()
    
    # When adding sections or items, add them in the reverse order of
    # how you want them to be displayed in the actual file.
    # In addition, please note that using RawConfigParser's and the raw
    # mode of ConfigParser's respective set functions, you can assign
    # non-string values to keys internally, but will receive an error
    # when attempting to write to a file or when you get it in non-raw
    # mode. SafeConfigParser does not allow such assignments to take place.
    config.add_section('Test')
    config.set('Test', testkey, testvalue)
    config.add_section('elasticsearch')
    config.set('elasticsearch', 'server-url', 'http://localhost:9200/')
    config.set('elasticsearch', 'index-alias', 'logstash-2013.10.01')
        
    # Writing our configuration file to 'example.cfg'
    with open('config.cfg', 'wb') as configfile:
        config.write(configfile)