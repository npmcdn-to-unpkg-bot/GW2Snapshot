import urllib
import urllib2
import json

from pprint import pprint

def getMaterials(API2_URL, encoded_key):
    full_url = API2_URL + '/account/materials?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    material_data = json.loads(the_page)
    
    for attribute in material_data:
         attribute.pop('category', None)
    
    return material_data