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
from material import getMaterials, getMaterials2

from app import app
from flask import Blueprint, render_template, request, make_response, flash, session
from ChunkedCookie import ChunkedSecureCookieSessionInterface
inventory2JSON = []
API2_URL = 'https://api.guildwars2.com/v2'
chunked = ChunkedSecureCookieSessionInterface()
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
    inventoryJSON = getAllInventory(API2_URL, encoded_key)
    bankJSON = get_bank(API2_URL, encoded_key)
    sharedJSON = getSharedInventory(API2_URL, encoded_key)
    materialsJSON = getMaterials(API2_URL, encoded_key)
  
    resp = make_response(render_template('snapshot.html'))
    resp.set_cookie('key', request.form['apiKey'])
    resp.set_cookie('materials5', json.dumps(materialsJSON[0]))
    resp.set_cookie('materials6', json.dumps(materialsJSON[1]))
    resp.set_cookie('materials29', json.dumps(materialsJSON[2]))
    resp.set_cookie('materials30', json.dumps(materialsJSON[3]))
    resp.set_cookie('materials37', json.dumps(materialsJSON[4]))
    resp.set_cookie('materials38', json.dumps(materialsJSON[5]))
    resp.set_cookie('materials46', json.dumps(materialsJSON[6]))
                        
    session['inventory'] = inventoryJSON
    session['bank'] = bankJSON
    session['shared'] = sharedJSON
    session['wallet'] = walletJSON
    session['characters'] = character_names
    session['time'] = time.time()
    
    chunked.save_session(app, session, resp)
    return resp

@app.route('/results', methods=['POST'])
def retake_snapshot():
    chunked.open_session(app, request)
    key = {'access_token' : request.cookies.get('key')}
    encoded_key = urllib.urlencode(key)
    start_time = session['time']
    minutes_elapsed = (time.time()-start_time)/60
    print '1'
    old_wallet_JSON = session['wallet']
    old_bank_JSON = session['bank']
    old_shared_JSON = session['shared']
    old_inventory_JSON = session['inventory']
    print '2'
    old_materials5_JSON = json.loads(request.cookies.get('materials5'))
    old_materials6_JSON = json.loads(request.cookies.get('materials6'))
    old_materials29_JSON = json.loads(request.cookies.get('materials29'))
    old_materials30_JSON = json.loads(request.cookies.get('materials30'))
    old_materials37_JSON = json.loads(request.cookies.get('materials37'))
    old_materials38_JSON = json.loads(request.cookies.get('materials38'))
    old_materials46_JSON = json.loads(request.cookies.get('materials46'))
    print '3'
    new_wallet_JSON = getWallet(API2_URL, encoded_key)
    new_bank_JSON = get_bank(API2_URL, encoded_key)
    new_shared_JSON = getSharedInventory(API2_URL, encoded_key)
    new_materials_JSON = getMaterials(API2_URL, encoded_key)
    new_inventory_JSON = getAllInventory(API2_URL, encoded_key)
    print '4'
    
    wallet_delta_list = []
    inventory_delta_list = []
    shared_delta_list = []
    bank_delta_list = []
    
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
    print '5'
    wallet_delta_list = compare_wallet(old_wallet_JSON, new_wallet_JSON)
    inventory_delta_list = compare_inventory(old_inventory_JSON, new_inventory_JSON)
    shared_delta_list = compare_inventory(old_shared_JSON, new_shared_JSON)
    bank_delta_list = compare_inventory(old_bank_JSON, new_bank_JSON)
    print '6'
    wallet_delta_list = remove_zero_value(wallet_delta_list)
    inventory_delta_list = remove_zero_count(inventory_delta_list)
    shared_delta_list = remove_zero_count(shared_delta_list)
    bank_delta_list = remove_zero_count(bank_delta_list)
    print '7'
    for materials in materials_delta_list2:
        for item in materials:
            item['id'] = itemIDToName(API2_URL, item['id'])       
    for currency in wallet_delta_list:
        currency['id'] = walletIDToName(API2_URL, currency['id'])
    for item in bank_delta_list:
        item['id'] = itemIDToName(API2_URL, item['id'])
    for item in shared_delta_list:
        item['id'] = itemIDToName(API2_URL, item['id'])
    for item in inventory_delta_list:
        item['id'] = itemIDToName(API2_URL, item['id'])
        
    resp = make_response(render_template('results.html',materials_delta_list=materials_delta_list2, minutes_elapsed=minutes_elapsed, wallet_delta_list=wallet_delta_list, bank_delta_list=bank_delta_list, shared_delta_list=shared_delta_list, inventory=inventory_delta_list))
    resp.set_cookie('materials5', expires=0)
    resp.set_cookie('materials6', expires=0)
    resp.set_cookie('materials29', expires=0)
    resp.set_cookie('materials30', expires=0)
    resp.set_cookie('materials37', expires=0)
    resp.set_cookie('materials38', expires=0)
    resp.set_cookie('materials46', expires=0)
    session.pop('inventory', None)
    session.pop('bank', None)
    session.pop('shared', None)
    session.pop('wallet', None)
    session.pop('characters', None)
    session.pop('time', None)
    return resp


