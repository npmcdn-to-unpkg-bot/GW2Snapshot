import urllib
import urllib2
import json
import sys
import filewriter
import time
import copy

from pprint import pprint
from listManipulation import *
from wallet import getWallet, walletIDToName
from inventory import *
from bank import get_bank
from sharedInventory import getSharedInventory 
from material import getMaterials, getMaterials2
from app import models
from app import app
from flask import Blueprint, render_template, request, make_response, flash, session
from tradingPost import getSellPrice
API2_URL = 'https://api.guildwars2.com/v2'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/snapshot', methods=['POST'])
def get_snapshot():
    api_key = request.form['apiKey']
    key = {'access_token' : api_key}
    print request.form['apiKey']
    encoded_key = urllib.urlencode(key)
    walletJSON = getWallet(API2_URL, encoded_key)
    if walletJSON == "Access denied!":
        return render_template('index.html',error='Access denied!')

    inventoryJSON = getAllInventory(API2_URL, encoded_key)
    inventory_data = json.dumps(inventoryJSON)
    assert len(inventory_data) < 20000
    sharedJSON = getSharedInventory(API2_URL, encoded_key)
    bankJSON = get_bank(API2_URL, encoded_key)
    materialsJSON = getMaterials2(API2_URL, encoded_key)
    materials_data = json.dumps(materialsJSON)
    assert len(materials_data) < 20000
    exists = models.db.session.query(models.Snapshot.api_key).filter_by(api_key=request.form['apiKey']).scalar() is not None
    if exists:
        snapshot = models.Snapshot.query.filter_by(api_key=request.form['apiKey']).first_or_404()
        snapshot.inventory = inventory_data
        snapshot.materials = materials_data
        models.db.session.commit()
    else:
        snapshot = models.Snapshot(request.form['apiKey'], inventory_data, materials_data)
        models.db.session.add(snapshot)
        models.db.session.commit()

    resp = make_response(render_template('snapshot.html'))
    resp.set_cookie('key', request.form['apiKey'])
    session['bank'] = bankJSON
    session['shared'] = sharedJSON
    session['wallet'] = walletJSON
    session['time'] = time.time()

    return resp

@app.route('/asdf', methods=['POST'])
def take_first_snapshot():
    api_key = request.form['key']
    key = {'access_token': api_key}
    encoded_key = urllib.urlencode(key)
    walletJSON = getWallet(API2_URL, encoded_key)
    if walletJSON == "Access denied!":
        return render_template('index.html', error='Access denied!')
    print '1'
    inventoryJSON = getAllInventory(API2_URL, encoded_key)
    inventory_data = json.dumps(inventoryJSON)
    assert len(inventory_data) < 20000
    sharedJSON = getSharedInventory(API2_URL, encoded_key)
    bankJSON = get_bank(API2_URL, encoded_key)
    materialsJSON = getMaterials2(API2_URL, encoded_key)
    materials_data = json.dumps(materialsJSON)
    assert len(materials_data) < 20000
    exists = models.db.session.query(models.Snapshot.api_key).filter_by(
        api_key=api_key).scalar() is not None
    print '2'
    if exists:
        snapshot = models.Snapshot.query.filter_by(api_key=api_key).first_or_404()
        snapshot.inventory = inventory_data
        snapshot.materials = materials_data
        models.db.session.commit()
    else:
        snapshot = models.Snapshot(api_key, inventory_data, materials_data)
        models.db.session.add(snapshot)
        models.db.session.commit()

    session['bank'] = bankJSON
    session['shared'] = sharedJSON
    session['wallet'] = walletJSON
    session['time'] = time.time()
    return api_key

@app.route('/results', methods=['POST'])
def retake_snapshot():
    api_key = request.cookies.get('key')
    key = {'access_token' : api_key}
    encoded_key = urllib.urlencode(key)
    start_time = session['time']
    minutes_elapsed = (time.time()-start_time)/60
    old_wallet_JSON = session['wallet']
    old_bank_JSON = session['bank']
    old_shared_JSON = session['shared']
    snapshot = models.Snapshot.query.filter_by(api_key=api_key).first_or_404()
    old_inventory_data = snapshot.inventory
    old_materials_data = snapshot.materials

    old_inventory_JSON = json.loads(old_inventory_data)
    old_materials_JSON = json.loads(old_materials_data)
    
    new_wallet_JSON = getWallet(API2_URL, encoded_key)
    new_inventory_JSON = getAllInventory(API2_URL, encoded_key)
    new_shared_JSON = getSharedInventory(API2_URL, encoded_key)
    new_bank_JSON = get_bank(API2_URL, encoded_key)
    new_materials_JSON = getMaterials2(API2_URL, encoded_key)
    
    wallet_delta_list = []
    inventory_delta_list = []
    shared_delta_list = []
    bank_delta_list = []
    materials_delta_list = []
    
    wallet_delta_list = compare_wallet(old_wallet_JSON, new_wallet_JSON)
    inventory_delta_list = compare_inventory(old_inventory_JSON, new_inventory_JSON)
    shared_delta_list = compare_inventory(old_shared_JSON, new_shared_JSON)
    bank_delta_list = compare_inventory(old_bank_JSON, new_bank_JSON)
    materials_delta_list = compare_inventory(old_materials_JSON, new_materials_JSON)
    
    wallet_delta_list = remove_zero_value(wallet_delta_list)
    inventory_delta_list = remove_zero_count(inventory_delta_list)
    shared_delta_list = remove_zero_count(shared_delta_list)
    bank_delta_list = remove_zero_count(bank_delta_list)
    materials_delta_list = remove_zero_count(materials_delta_list)
    condensed_list = inventory_delta_list+shared_delta_list+bank_delta_list+materials_delta_list

    for item in condensed_list:
        exists = models.db.session.query(models.Item.name).filter_by(id=item['id']).scalar() is not None
        if exists:
            name = (models.Item.query.filter_by(id=item['id']).first_or_404()).name
            item['name'] = name
            print name + ' found'
        else:
            name = itemIDToName(API2_URL, item['id'])
            dbItem = models.Item(item['id'], name)
            models.db.session.add(dbItem)
            models.db.session.commit()
            item['name'] = name
            print name + ' added'

    condensed_list2 = copy.deepcopy(condensed_list)
    condensed_list2 = compress_list(condensed_list2)
    condensed_list2 = remove_zero_count(condensed_list2)
    totalValue = 0
    for item in condensed_list2:
        value = getSellPrice(API2_URL, item['id'])
        item['value'] = item['count']*value
        totalValue += item['value']
    for currency in wallet_delta_list:
        currency['id'] = walletIDToName(API2_URL, currency['id'])

    zero_value_items = [zero_value_item for zero_value_item in condensed_list2 if zero_value_item['value'] == 0]
    headers = {'Content-Type': 'text/html'}
    resp = make_response(render_template('results.html',zero_value_items=zero_value_items, materials_delta_list=materials_delta_list, minutes_elapsed=minutes_elapsed, wallet_delta_list=wallet_delta_list, bank_delta_list=bank_delta_list, shared_delta_list=shared_delta_list, inventory=inventory_delta_list, totals=condensed_list2, totalValue=totalValue),200,headers)
    session.pop('wallet', None)
    session.pop('shared', None)
    session.pop('bank', None)
    session.pop('time', None)
    return resp




