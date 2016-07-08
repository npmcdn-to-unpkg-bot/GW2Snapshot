import urllib
import urllib2
import json
import sys
import credentials
import filewriter
import time

from pprint import pprint
from listManipulation import *
from wallet import getWallet, walletIDToName
from inventory import *
from bank import get_bank
from sharedInventory import getSharedInventory 
from material import getMaterials

from app import app
from flask import Blueprint, render_template, request, make_response, flash, session

API2_URL = 'https://api.guildwars2.com/v2'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/snapshot', methods=['POST'])
def get_snapshot():
    key = {'access_token' : request.form['apiKey']}
    print request.form['apiKey']
    encoded_key = urllib.urlencode(key)
    walletJSON = getWallet(API2_URL, encoded_key)
    if walletJSON == "Access denied!":
        return render_template('index.html',error='Access denied!')
    character_names = getCharacterNames(API2_URL, encoded_key)
    print '1'
    inventoryJSONList = getAllInventory2(API2_URL, encoded_key, character_names)
    print '2'
    bankJSON = get_bank(API2_URL, encoded_key)
    print '3'
    sharedJSON = getSharedInventory(API2_URL, encoded_key)
    print '4'
    materialsJSON = getMaterials(API2_URL, encoded_key)
    print '5'
    session['materials5'] = materialsJSON[0]
    session['materials6'] = materialsJSON[1]
    session['materials29'] = materialsJSON[2]
    session['materials30'] = materialsJSON[3]
    session['materials37'] = materialsJSON[4]
    session['materials38'] = materialsJSON[5]
    session['materials46'] = materialsJSON[6]
    session['bank'] = bankJSON
    session['shared'] = sharedJSON
    session['wallet'] = walletJSON
    resp = make_response(render_template('snapshot.html', wallet=walletJSON))
    print '6'
    for character, inventoryJSON in zip(character_names, inventoryJSONList):
        resp.set_cookie('%s' % character.replace(" ", "_"), inventoryJSON)
    print '7'
    session['characters'] = character_names
    resp.set_cookie('key', request.form['apiKey'])
    resp.set_cookie('wallet_data', json.dumps(walletJSON))
    resp.set_cookie('bank_data', json.dumps(bankJSON))
    resp.set_cookie('shared_data', json.dumps(sharedJSON))
    resp.set_cookie('start_time', str(time.time()))
    return resp

@app.route('/results', methods=['POST'])
def retake_snapshot():
    key = {'access_token' : request.cookies.get('key')}
    encoded_key = urllib.urlencode(key)
    start_time = request.cookies.get('start_time')
    minutes_elapsed = (time.time()-float(start_time))/60
    print session['characters']
    for character in session['characters']:
        print request.cookies.get('%s' % character.replace(" ", "_"))
    old_wallet_data = request.cookies.get('wallet_data')
    old_bank_data = request.cookies.get('bank_data')
    old_shared_data = request.cookies.get('shared_data')
    
    old_wallet_JSON = json.loads(old_wallet_data)
    old_bank_JSON = json.loads(old_bank_data)
    old_shared_JSON = json.loads(old_shared_data)
    
    old_materials5_JSON = session['materials5']
    old_materials6_JSON = session['materials6']
    old_materials29_JSON = session['materials29']
    old_materials30_JSON = session['materials30']
    old_materials37_JSON = session['materials37']
    old_materials38_JSON = session['materials38']
    old_materials46_JSON = session['materials46']
    
    new_wallet_JSON = getWallet(API2_URL, encoded_key)
    new_bank_JSON = get_bank(API2_URL, encoded_key)
    new_shared_JSON = getSharedInventory(API2_URL, encoded_key)
    new_materials_JSON = getMaterials(API2_URL, encoded_key)
    
    wallet_delta_list = []
    bank_delta_list = []
    shared_delta_list = []
    materials5_delta_list = []
    materials6_delta_list = []
    materials29_delta_list = []
    materials30_delta_list = []
    materials37_delta_list = []
    materials38_delta_list = []
    materials46_delta_list = []
    materials_delta_list = []
    materials_delta_list.append(compare_inventory(old_materials5_JSON, new_materials_JSON[0]))
    materials_delta_list.append(compare_inventory(old_materials6_JSON, new_materials_JSON[1]))
    materials_delta_list.append(compare_inventory(old_materials29_JSON, new_materials_JSON[2]))
    materials_delta_list.append(compare_inventory(old_materials30_JSON, new_materials_JSON[3]))
    materials_delta_list.append(compare_inventory(old_materials37_JSON, new_materials_JSON[4]))
    materials_delta_list.append(compare_inventory(old_materials38_JSON, new_materials_JSON[5]))
    materials_delta_list.append(compare_inventory(old_materials46_JSON, new_materials_JSON[6]))
    materials_delta_list2 = []
    for materials in materials_delta_list:
        materials_delta_list2.append(remove_zero_count(materials))
    
    wallet_delta_list = compare_wallet(old_wallet_JSON, new_wallet_JSON)
    wallet_delta_list = remove_zero_value(wallet_delta_list)
    
    bank_delta_list = compare_inventory(old_bank_JSON, new_bank_JSON)
    bank_delta_list = remove_zero_count(bank_delta_list)

    shared_delta_list = compare_inventory(old_shared_JSON, new_shared_JSON)
    shared_delta_list = remove_zero_count(shared_delta_list)
    for materials in materials_delta_list2:
        for item in materials:
            item['id'] = itemIDToName(API2_URL, item['id'])       
    for currency in wallet_delta_list:
        currency['id'] = walletIDToName(API2_URL, currency['id'])
    for item in bank_delta_list:
        item['id'] = itemIDToName(API2_URL, item['id'])
    for item in shared_delta_list:
        item['id'] = itemIDToName(API2_URL, item['id'])    
    resp = make_response(render_template('results.html',materials_delta_list=materials_delta_list2, minutes_elapsed=minutes_elapsed, wallet_delta_list=wallet_delta_list, bank_delta_list=bank_delta_list, shared_delta_list=shared_delta_list))
    session.pop('materials5', None)
    session.pop('materials6', None)
    session.pop('materials29', None)
    session.pop('materials30', None)
    session.pop('materials37', None)
    session.pop('materials38', None)
    session.pop('materials46', None)
    return resp


