import urllib
import urllib2
import json

from listManipulation import compress_list, removeZero
from pprint import pprint

def getInventory(API2_URL, encoded_key, CHARACTER):
    scope_url = '/characters/' + CHARACTER + '/Inventory'
    inventory_data = []
    full_url = API2_URL + scope_url + '?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    inventory_data = json.loads(the_page)
    inventory_data = inventory_data['bags']
    
    filtered = []
    for bag in inventory_data:
        for item in bag['inventory']:
            if item != None:
                filtered.append(item)
                      
    #Filters out everything except 'count' and 'id'
    for attribute in filtered:
         attribute.pop('binding', None)
         attribute.pop('skin', None)
         attribute.pop('upgrades', None)
         attribute.pop('bound_to', None)
    
    #Compress list of items have duplicate id
    compresesd_list = []
    compressed_list = compress_list(filtered)
    
    return compressed_list