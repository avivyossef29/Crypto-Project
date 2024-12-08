from flask import Flask, jsonify, request, make_response
import requests
import os
from ssl3 import encrypt, decrypt, bytes_to_str, str_to_bytes

app = Flask(__name__)

_SERVER_URL = "http://server_container:3000/"

@app.route('/', methods=['GET'])
def get_request():
    """Gets a path and data and returns the encrypted request
    that will be sent to that path with the data. The request 
    will be ecrypted with the keys recieved from the server

    @param path (str): The path in the url that the request will be sent to
    @param data (str): The data to be added to the body of the request

    @returns (bytes): Padded and encrypted request as bytes
    """
    json = request.json
    path = data.get("path")
    data = data.get("data")
    request = f"POST /{path} HTTP/1.1\r\nCookies: session-cookie={os.environ["SECRET_COOKIE"]}\r\nBody: {data}"
    response = requests.get(url= _SERVER_URL + "keys",
                            cookies={"cookie": os.environ["SECRET_COOKIE"]},
                            headers={"Content-Type":"application/json"})
    keys = [str_to_bytes(i) for i in response.json().get("keys", [])]
    return bytes_to_str(encrypt(request, *keys))



@app.route('/', methods=['POST'])
def send_request():
    """Sends the request to the server together with the cookie

    @param request (bytes): The request as bytes to be sent to the server

    @returns (response): The response from the server
    """
    data = request.data
    response = requests.post(url= _SERVER_URL,
                            data=data,
                            cookies={"cookie": os.environ["SECRET_COOKIE"]},
                            headers={"Content-Type":"application/json"})
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)