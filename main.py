import urllib
import urllib2
import json

import credentials
import filewriter

from pprint import pprint
from listManipulation import compareList, compressList, removeZero
from wallet import getWallet

API2_URL = 'https://api.guildwars2.com/v2'
CHARACTER = credentials.CHARACTER
scope_url = '/characters/' + CHARACTER + '/Inventory'
key = credentials.key
encoded_key = urllib.urlencode(key)
full_url = API2_URL + scope_url + '?' + encoded_key
response = urllib2.urlopen(full_url)
the_page = response.read()
json_data = json.loads(the_page)
bags = json_data['bags']

filtered = []
for bag in bags:
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
compressed_list = compressList(filtered)

file = filewriter.FileWriter('writefile.txt')

try:
    #Try reading previous snapshot
    data = file.readFromFile()

    #Compare snapshots
    delta_list = []
    delta_list = compareList(data, compressed_list)
    delta_list = removeZero(delta_list)
    pprint(delta_list)
    
except:
    print "No snapshot found"

#Update the snapshot
file.writeToFile(compressed_list)

getWallet(API2_URL, key)