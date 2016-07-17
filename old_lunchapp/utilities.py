import json
import urllib2

def get_json(url):
    request = urllib2.urlopen(url)
    return json.loads(request.read())
