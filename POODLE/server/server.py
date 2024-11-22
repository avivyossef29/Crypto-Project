from flask import Flask, jsonify, request, make_response
from ssl3 import encode, decrypt
from uuid import uuid4
import os

app = Flask(__name__)

cookie = str(uuid4())
logged_in = False

cbc_key = os.urandom(16)
cbc_iv = os.urandom(16)
mac_key = os.urandom(16)
mac_iv = os.urandom(16)

def refresh_keys():
    global cbc_key
    global cbc_iv
    global mac_key
    global mac_iv
    cbc_key = os.urandom(16)
    cbc_iv = os.urandom(16)
    mac_key = os.urandom(16)
    mac_iv = os.urandom(16)

def verify_cookie(func):

def decrypt_request(func):

@app.after_request
def apply_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Resource not found"), 404

@app.route('/', methods=['GET'])
@decrypt_request
def api_root():
    res = make_response(jsonify(request.get_json()))
    return res


@app.route('/login', methods=['POST'])
def login():
    global logeed_in
    if logeed_in:
        return null
    logeed_in = True
    return cookie
    

@app.route('/keys', methods=['GET'])
@verify_cookie
def get_keys():
    return jsonify({"keys": (cbc_key, cbc_iv, mac_key, mac_iv)})    

@app.route('/check-cookie', methods=['GET'])
def check_cookie():

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)