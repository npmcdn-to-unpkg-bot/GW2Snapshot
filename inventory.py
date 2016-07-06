import urllib
import urllib2
import json

from listManipulation import compress_list, remove_zero_count
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

def getAllInventory(API2_URL, encoded_key):
    full_url = API2_URL + '/characters?page=0&&' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    characters_data = json.loads(the_page)

    filtered = []
    for character in characters_data:
        for bags in character['bags']:
            for item in bags['inventory']:
                if item != None:
                    filtered.append(item)
                    
    #Filters out everything except 'count' and 'id'
    for attribute in filtered:
        attribute.pop('binding', None)
        attribute.pop('skin', None)
        attribute.pop('upgrades', None)
        attribute.pop('bound_to', None)
        attribute.pop('stats', None)
        attribute.pop('infusions', None)
                 
    #Compress list of items have duplicate id
    compresesd_list = []
    compressed_list = compress_list(filtered)
    return compressed_list

def itemIDToName(API2_URL, walletID):
    scope_url = '/items/'
    full_url = API2_URL + scope_url + str(walletID)
    print full_url
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    currencyJSON = json.loads(the_page)
    return currencyJSON['name']
