import requests
from flask import Flask, jsonify, request, Response
import os
from ssl3 import encrypt, decrypt, bytes_to_str, str_to_bytes

app = Flask(__name__)

_SERVER_URL = "http://server_container:3000/"

cookie = requests.post(url= _SERVER_URL + "login",
                        headers={"Content-Type":"application/json"}).text

@app.route('/', methods=['GET'])
def get_request():
    path = request.args.get("path")
    data = request.args.get("data")
    raw = f"POST /{path} HTTP/1.1\r\nCookies: session-cookie={cookie}\r\nBody: {data}"
    response = requests.get(url= _SERVER_URL + "keys",
                            cookies={"cookie": cookie},
                            headers={"Content-Type":"application/json"})
    keys = [str_to_bytes(i) for i in response.json().get("keys", [])]
    return bytes_to_str(encrypt(raw, *keys))


@app.route('/', methods=['POST'])
def send_request():
    data = request.data
    response = requests.post(url= _SERVER_URL,
                            data=data,
                            cookies={"cookie": cookie},
                            headers={"Content-Type":"application/json"})
    return Response(
        response.content,
        status=response.status_code,
        headers=dict(response.headers)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)