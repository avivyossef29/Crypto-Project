from flask import Flask, jsonify, request, make_response
from uuid import uuid4
import ssl

app = Flask(__name__)

users = {
    'victim': {'password': '12345', 'cookie': '', 'expired': True}
}

@app.after_request
def apply_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def verify_cookie(func):
    def wrapper():
        user = users.get(request.args.get('username'))
        cookie = request.cookies.get('secret-cookie')
        if not user:
            return func(text='no user')
        if not cookie:
            return func(text='no cookie')
        if cookie == user['cookie'] and not user['expired']:
            return func()
        else:
            return func(text='wrong cookie')
    return wrapper

@app.route('/', methods=['GET'])
def api_root():
    res = make_response(jsonify(request.get_json()))
    return res

@app.route('/', methods=['POST'])
@verify_cookie
def api_post_test(text='hello'):
    res = make_response(text)
    return res


@app.route('/login', methods=['POST'])
def login():
    res = make_response()
    username = request.args.get('username')
    password = request.args.get('password')
    if not username or not password:
        res.set_data("missing username or password")
    user = users.get(username)
    if not user:
        res.set_data("wrong username or password")
    elif user['password'] != password:
        res.set_data("wrong username or password")
    else:
        cookie = str(uuid4())
        user['cookie'] = cookie
        user['expired'] = False
        res.set_data(cookie)
    return res

if __name__ == '__main__':
    
    # Create an SSL 3.0 context
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)

    # Load server's certificate and private key
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    # Limit cipher suites to CBC
    context.set_ciphers('AES128-SHA')

    app.run(host='0.0.0.0', port=443, ssl_context=context)