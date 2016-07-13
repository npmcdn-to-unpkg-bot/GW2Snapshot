import urllib
import urllib2
import json

from pprint import pprint

def getSellPrice(API2_URL, id):
    full_url = API2_URL + '/commerce/prices/' + str(id)
    try:
        response = urllib2.urlopen(full_url)
        the_page = response.read()
        listing_data = json.loads(the_page)
        sells = listing_data['sells']
        price = sells['unit_price']
    except:
        return 0
    return price

