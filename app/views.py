import urllib
import urllib2
import json

import credentials
import filewriter

from pprint import pprint
from listManipulation import *
from wallet import getWallet
from inventory import getInventory
from bank import get_bank

from app import app
from flask import Blueprint, render_template, request, make_response

API2_URL = 'https://api.guildwars2.com/v2'
key = ''

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/snapshot', methods=['POST'])
def get_snapshot():
    key = {'access_token' : request.form['apiKey']}
    encoded_key = urllib.urlencode(key)
    wallet_data = getWallet(API2_URL, encoded_key)
    print type(wallet_data)
    resp = make_response(render_template('snapshot.html', wallet=json.loads(wallet_data)))
    pprint(wallet_data)
    resp.set_cookie('key', encoded_key)
    resp.set_cookie('wallet_data', wallet_data)
    return resp

@app.route('/results', methods=['POST'])
def retake_snapshot():
    encoded_key = request.cookies.get('key')
    old_wallet_data = request.cookies.get('wallet_data')
    new_wallet_data = getWallet(API2_URL, encoded_key)
    delta_list = []
    pprint(old_wallet_data)
    pprint(new_wallet_data)
    old_wallet_data = json.loads(old_wallet_data)
    new_wallet_data = json.loads(new_wallet_data)
    delta_list = compare_wallet(old_wallet_data, new_wallet_data)
    delta_list = remove_zero_value(delta_list)
    pprint(delta_list)
    resp = make_response(render_template('results.html',dlist=delta_list, new_list=new_wallet_data))
    return resp
