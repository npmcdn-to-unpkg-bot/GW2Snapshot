import urllib
import urllib2
import json
import sys
import credentials
import filewriter

from pprint import pprint
from listManipulation import *
from wallet import getWallet, walletIDToName
from inventory import getAllInventory, itemIDToName
from bank import get_bank
from sharedInventory import getSharedInventory 
from material import getMaterials

from app import app
from flask import Blueprint, render_template, request, make_response, flash

API2_URL = 'https://api.guildwars2.com/v2'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/snapshot', methods=['POST'])
def get_snapshot():
    key = {'access_token' : request.form['apiKey']}
    encoded_key = urllib.urlencode(key)
    walletJSON = getWallet(API2_URL, encoded_key)
    if walletJSON == "Access denied!":
        return render_template('index.html',error='Access denied!')
    inventoryJSON = getAllInventory(API2_URL, encoded_key)
    bankJSON = get_bank(API2_URL, encoded_key)
    sharedJSON = getSharedInventory(API2_URL, encoded_key)
    materialsJSON = getMaterials(API2_URL, encoded_key)
    materialsJSON2 = remove_zero_count(materialsJSON)
    resp = make_response(render_template('snapshot.html', wallet=walletJSON))
    resp.set_cookie('key', encoded_key)
    resp.set_cookie('wallet_data', json.dumps(walletJSON))
    resp.set_cookie('bank_data', json.dumps(bankJSON))
    resp.set_cookie('shared_data', json.dumps(sharedJSON))
    return resp

@app.route('/results', methods=['POST'])
def retake_snapshot():
    encoded_key = request.cookies.get('key')
    old_wallet_data = request.cookies.get('wallet_data')
    old_bank_data = request.cookies.get('bank_data')
    old_shared_data = request.cookies.get('shared_data')
    
    old_wallet_JSON = json.loads(old_wallet_data)
    old_bank_JSON = json.loads(old_bank_data)
    old_shared_JSON = json.loads(old_shared_data)
    
    new_wallet_JSON = getWallet(API2_URL, encoded_key)
    new_bank_JSON = get_bank(API2_URL, encoded_key)
    new_shared_JSON = getSharedInventory(API2_URL, encoded_key)
    
    wallet_delta_list = []
    bank_delta_list = []
    shared_delta_list = []
    
    wallet_delta_list = compare_wallet(old_wallet_JSON, new_wallet_JSON)
    wallet_delta_list = remove_zero_value(wallet_delta_list)
    
    bank_delta_list = compare_inventory(old_bank_JSON, new_bank_JSON)
    bank_delta_list = remove_zero_count(bank_delta_list)

    shared_delta_list = compare_inventory(old_shared_JSON, new_shared_JSON)
    shared_delta_list = remove_zero_count(shared_delta_list)

    for currency in wallet_delta_list:
        currency['id'] = walletIDToName(API2_URL, currency['id'])
    for item in bank_delta_list:
        item['id'] = itemIDToName(API2_URL, item['id'])
    for item in shared_delta_list:
        item['id'] = itemIDToName(API2_URL, item['id'])    
    resp = make_response(render_template('results.html',wallet_delta_list=wallet_delta_list, bank_delta_list=bank_delta_list, shared_delta_list=shared_delta_list))
    return resp
