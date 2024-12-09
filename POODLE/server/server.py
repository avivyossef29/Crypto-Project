from flask import Flask, jsonify, request
from ssl3 import encrypt, decrypt, bytes_to_str, str_to_bytes
from uuid import uuid4
import os

app = Flask(__name__)

_SECRET_COOKIE = uuid4().hex
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

@app.before_request
def verify_cookie():
    cookie = request.cookies.get("cookie", "")
    if cookie != _SECRET_COOKIE and request.path != "/login":
        return "Wrong or missing cookie", 403

@app.after_request
def apply_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Resource not found"), 404

@app.route('/', methods=['POST'])
def api_root():
    text = request.data
    try:
        decrypt(str_to_bytes(text), cbc_key, cbc_iv, mac_key, mac_iv)
        return "", 200
    except Exception as e:
        refresh_keys()
        return str(e), 423

@app.route('/login', methods=['POST'])
def login():
    global logged_in
    if logged_in:
        return "You are already logged in", 403
    logged_in = True
    return _SECRET_COOKIE

@app.route('/keys', methods=['GET'])
def get_keys():
    return jsonify({"keys": [bytes_to_str(i) for i in [cbc_key, cbc_iv, mac_key, mac_iv]]})

@app.route('/get-private-data', methods=['GET'])
def ctf_final_check():
    return '\033[92m' + "\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n\nCongradulations!!! You won the CTF challenge!!!\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n" + '\033[0m', 200
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)