import urllib
import urllib2
import json

from pprint import pprint

def getSharedInventory(API2_URL, encoded_key):
    full_url = API2_URL + '/account/inventory?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    shared_inventory_data = json.loads(the_page)
    return shared_inventory_data