import requests
import os
from ssl3 import encrypt, decrypt, bytes_to_str, str_to_bytes

_ROOT_URL = "http://server_container:3000/"

def get_request(path: str, data: str) -> bytes:
    """Gets a path and data and returns the encrypted request
    that will be sent to that path with the data. The request 
    will be ecrypted with the keys recieved from the server

    @param path (str): The path in the url that the request will be sent to
    @param data (str): The data to be added to the body of the request

    @returns (bytes): Padded and encrypted request as bytes
    """
    request = f"POST /{path} HTTP/1.1\r\nCookies: session-cookie={_SECRET_COOKIE}\r\nBody: {data}"
    response = requests.get(url= _ROOT_URL + "keys",
                            cookies={"cookie": _SECRET_COOKIE},
                            headers={"Content-Type":"application/json"})
    keys = [str_to_bytes(i) for i in response.json().get("keys", [])]
    return encrypt(request, *keys)

def send_request(request: bytes):
    """Sends the request to the server together with the cookie

    @param request (bytes): The request as bytes to be sent to the server

    @returns (response): The response from the server
    """
    response = requests.post(url= _ROOT_URL,
                            data=bytes_to_str(request),
                            cookies={"cookie": _SECRET_COOKIE},
                            headers={"Content-Type":"application/json"})
    return response

def check_solution(cookie: str) -> str:
    """Sends a request to the server with a provided cookie that checks
    if you solved the challenge

    @param cookie (str): The cookie that would grant access to the private
    data of the victim

    @returns (str): A victory message
    """
    response = requests.get(url= _ROOT_URL + "get-private-data",
                            cookies={"cookie": cookie},
                            headers={"Content-Type":"application/json"})
    return response.text

# This is a login section where the victim gets the cookie from the server
response = requests.post(url= _ROOT_URL + "login",
                        headers={"Content-Type":"application/json"})
_SECRET_COOKIE = response.text
