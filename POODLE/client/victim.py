import requests
import os
from ssl3 import encrypt, decrypt

def get_request(url: str, data: str) -> bytes:
    response = requests.get(url="https://server_container/keys", params={"cookie": os.environ["COOKIE"]})
    keys = tuple(response.json().get("keys"))
    return encrypt(text, *keys)

def send_request(request: bytes):
    return requests.get(request)

response = requests.get(url="https://server_container/login")
os.environ["COOKIE"] = response.text

