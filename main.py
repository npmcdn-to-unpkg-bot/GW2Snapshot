import urllib
import urllib2
import json

import credentials
import filewriter

from pprint import pprint
from listManipulation import compare_list, compress_list, removeZero
from wallet import getWallet
from inventory import getInventory

INVENTORYFILENAME = 'inventoryData.txt'
WALLETFILENAME = 'walletData.txt'
API2_URL = 'https://api.guildwars2.com/v2'
CHARACTER = credentials.CHARACTER
key = credentials.key
encoded_key = urllib.urlencode(key)

#Inventory Data
inventory_data = getInventory(API2_URL, encoded_key, CHARACTER)
inventory_file = filewriter.FileWriter(INVENTORYFILENAME)

try:
    #Try reading previous inventory snapshot
    data = inventory_file.readFromFile()

    #Compare inventory snapshots
    delta_list = []
    delta_list = compare_list(data, inventory_data)
    delta_list = removeZero(delta_list)
    pprint(delta_list)
    
except:
    print "No inventory snapshot found"

#Update the inventory snapshot
inventory_file.writeToFile(inventory_data)

#Wallet Data
wallet_data = getWallet(API2_URL, encoded_key)
wallet_file = filewriter.FileWriter(WALLETFILENAME)
wallet_file.writeToFile(wallet_data)