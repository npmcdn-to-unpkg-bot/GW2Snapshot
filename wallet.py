import urllib
import urllib2
import json
from pprint import pprint

def getWallet(API2_URL, encoded_key):
    scope_url = '/account/wallet'
    wallet_data = []
    full_url = API2_URL + scope_url + '?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    wallet_data = json.loads(the_page)
    return wallet_data

        