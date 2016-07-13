import urllib
import urllib2
import json

from pprint import pprint

def getMaterials(API2_URL, encoded_key):
    full_url = API2_URL + '/account/materials?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    material_data = json.loads(the_page)
    m5 = []
    m6 = []
    m29 = []
    m30 = []
    m37 = []
    m38 = []
    m46 = []
    for attribute in material_data:
    #     attribute.pop('category', None)
        if attribute['category'] == 5:
            if attribute['count'] != 0:
                m5.append({'id': attribute['id'], 'count' : attribute['count']})
        elif attribute['category'] == 6:
            if attribute['count'] != 0:
                m6.append({'id': attribute['id'], 'count' : attribute['count']})
        elif attribute['category'] == 29:
            if attribute['count'] != 0:
                m29.append({'id': attribute['id'], 'count' : attribute['count']})
        elif attribute['category'] == 30:
            if attribute['count'] != 0:
                m30.append({'id': attribute['id'], 'count' : attribute['count']})
        elif attribute['category'] == 37:
            if attribute['count'] != 0:
                m37.append({'id': attribute['id'], 'count' : attribute['count']})
        elif attribute['category'] == 38:
            if attribute['count'] != 0:
                m38.append({'id': attribute['id'], 'count' : attribute['count']})
        elif attribute['category'] == 46:
            if attribute['count'] != 0:
                m46.append({'id': attribute['id'], 'count' : attribute['count']})
        else:
            print 'Unknown material category'
    return [m5, m6, m29, m30, m37, m38, m46]

def getMaterials2(API2_URL, encoded_key):
    full_url = API2_URL + '/account/materials?' + encoded_key
    response = urllib2.urlopen(full_url)
    the_page = response.read()
    material_data = json.loads(the_page)
    for attribute in material_data:
         attribute.pop('category', None)
    return material_data
