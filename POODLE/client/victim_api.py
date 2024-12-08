import requests
import os
from ssl3 import encrypt, decrypt, bytes_to_str, str_to_bytes

_VICTIM_URL = "http://server_container:4000/"
_SERVER_URL = "http://server_container:3000/"

def get_request(path: str, data: str) -> bytes:
    """Gets a path and data and returns the encrypted request
    that will be sent to that path with the data. The request 
    will be ecrypted with the keys recieved from the server

    @param path (str): The path in the url that the request will be sent to
    @param data (str): The data to be added to the body of the request

    @returns (bytes): Padded and encrypted request as bytes
    """
    response = requests.get(url= _VICTIM_URL,
                            params={"path": path, "data": data},
                            headers={"Content-Type":"application/json"})
    return str_to_bytes(response.text)


def send_request(request: bytes):
    """Sends the request to the server together with the cookie

    @param request (bytes): The request as bytes to be sent to the server

    @returns (response): The response from the server
    """
    response = requests.post(url= _VICTIM_URL,
                            data=bytes_to_str(request),
                            headers={"Content-Type":"application/json"})
    return response


def check_solution(cookie: str) -> str:
    """Sends a request to the server with a provided cookie that checks
    if you solved the challenge

    @param cookie (str): The cookie that would grant access to the private
    data of the victim

    @returns (str): A victory message
    """
    response = requests.get(url= _SERVER_URL + "get-private-data",
                            cookies={"cookie": cookie},
                            headers={"Content-Type":"application/json"})
    return response.text
