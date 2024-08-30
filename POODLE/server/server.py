from flask import Flask, jsonify
import ssl

app = Flask(__name__)

@app.route('/', methods=['GET'])
def api_root():
    return jsonify(message="Hello, SSLv3 with CBC encryption!")

if __name__ == '__main__':
    
    # Create an SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)

    # # Enable SSL 3.0
    # context.options &= ~ssl.OP_NO_SSLv3

    # Load server's certificate and private key
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    # Limit cipher suites to CBC
    context.set_ciphers('AES128-SHA')

    app.run(host='0.0.0.0', port=443, ssl_context=context)