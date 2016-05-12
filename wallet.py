import urllib
import urllib2
import json
from pprint import pprint

def getWallet(API2_URL, key):
    scope_url = '/account/wallet'
    key = {'access_token' : '028770F7-53E9-A942-915F-6B4EAD3718435768778F-3A5C-4E7B-A870-DDAE02E0E1FB'}
    encoded_key = urllib.urlencode(key)
#    currencies = getCurrency(API2_URL, encoded_key)
    wallet_data = []
    full_url = API2_URL + scope_url + '?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    wallet_data = json.loads(the_page)
    
#    for currency in currencies:
#        full_url = API2_URL + scope_url + str(currency) + '?' + encoded_key
#        response = urllib2.urlopen(full_url)
#        the_page = response.read()
#        wallet = json.loads(the_page)
#        wallet_data.append(wallet)
#        
#    for attribute in wallet_data:
#        attribute.pop('description', None)
#        attribute.pop('icon', None)
#        
    pprint(wallet_data)

def getCurrency(API2_URL, encoded_key):
    scope_url = '/currencies'
    full_url = API2_URL + scope_url + '?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    wallet_data = json.loads(the_page)
    return wallet_data
        