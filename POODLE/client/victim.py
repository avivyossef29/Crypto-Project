import requests
import os
from ssl3 import encrypt, decrypt, bytes_to_str, str_to_bytes

def get_request(path: str, data: str) -> bytes:
    request = f"POST /{path} HTTP/1.1\r\nCookie: cookie={_SECRET_COOKIE}\r\nBody: {data}"
    response = requests.get(url="http://server_container:3000/keys",
                            cookies={"cookie": _SECRET_COOKIE},
                            headers={"Content-Type":"application/json"})
    keys = [str_to_bytes(i) for i in response.json().get("keys", [])]
    return encrypt(request, *keys)

def send_request(request: bytes):
    response = requests.post(url="http://server_container:3000/",
                            data=bytes_to_str(request),
                            cookies={"cookie": _SECRET_COOKIE},
                            headers={"Content-Type":"application/json"})
    return response

def check_solution(cookie: str) -> str:
    response = requests.get(url="http://server_container:3000/get-private-data",
                            cookies={"cookie": cookie},
                            headers={"Content-Type":"application/json"})
    return response.text

response = requests.post(url="http://server_container:3000/login",
                        headers={"Content-Type":"application/json"})
_SECRET_COOKIE = response.text
