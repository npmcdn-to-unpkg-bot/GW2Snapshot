import urllib
import urllib2
import json
from pprint import pprint

def getWallet(API2_URL, encoded_key):
    scope_url = '/account/wallet'
    wallet_data = []
    full_url = API2_URL + scope_url + '?' + encoded_key
    try:
        response = urllib2.urlopen(full_url)
        the_page = response.read()
        wallet_data = json.loads(the_page)
        return wallet_data
    except urllib2.HTTPError, err:
        if err.code == 403:
            print "Access denied!"
            return "Access denied!"
        else:
            print "Something happened! Error code", err.code
            return "Some other error happened"
    except urllib2.URLError, err:
        print "Some other error happened:", err.reason
        return "Some other error happened: "
    

def walletIDToName(API2_URL, walletID):
    scope_url = '/currencies/'
    full_url = API2_URL + scope_url + str(walletID)
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    currencyJSON = json.loads(the_page)
    return currencyJSON['name']
    
        
