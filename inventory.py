import urllib
import urllib2
import json

from listManipulation import compress_list, remove_zero_count
from pprint import pprint
from app import models

API2_URL = 'https://api.guildwars2.com/v2'

def getInventory(API2_URL, encoded_key, character):
    character = urllib.quote(character)
    scope_url = '/characters/' + character + '/Inventory'
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
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    currencyJSON = json.loads(the_page)
    return currencyJSON['name']
    
def getCharacterNames(API2_URL, encoded_key):
    scope_url = '/characters/'
    full_url = API2_URL + scope_url + '?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    character_names = json.loads(the_page)
    return character_names

def getAllInventory2(API2_URL, encoded_key, character_names):
    inventory = []
    for character in character_names:
        inventory.append(getInventory(API2_URL, encoded_key, character))
    return inventory


def add_name_to_item(item):
    exists = models.db.session.query(models.Item.name).filter_by(id=item['id']).scalar() is not None
    if exists:
        name = (models.Item.query.filter_by(id=item['id']).first_or_404()).name
        item['name'] = name
    else:
        name = itemIDToName(API2_URL, item['id'])
        db_item = models.Item(item['id'], name)
        models.db.session.add(db_item)
        models.db.session.commit()
        item['name'] = name
    models.db.session.close()
