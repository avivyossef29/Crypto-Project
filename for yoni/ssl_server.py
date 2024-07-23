import ssl
import socket

def create_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the port
    server_address = ('localhost', 10001)
    print(f'Starting up on {server_address[0]} port {server_address[1]}')
    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(1)

    # Load SSL context with TLS 1.0
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)  # For TLS 1.0
    # context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)  # Uncomment for SSL 3.0 if needed
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')

    # Set cipher list to include AES-CBC
    context.set_ciphers('AES128-SHA')

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        connection, client_address = sock.accept()
        
        ssl_conn = None  # Initialize ssl_conn to None
        try:
            print(f'Connection from {client_address}')
            
            # Wrap the connection with SSL
            ssl_conn = context.wrap_socket(connection, server_side=True)
            
            while True:
                data = ssl_conn.recv(1024)
                if data:
                    print(f'Received: {data.decode()}')
                    ssl_conn.sendall(b'HTTP/1.1 200 OK\r\n'
                                     b'Content-Type: text/plain\r\n\r\n'
                                     b'Hello, world!')
                else:
                    break
                
        except ssl.SSLError as e:
            print(f'SSL error: {e}')
        
        finally:
            if ssl_conn:
                try:
                    ssl_conn.shutdown(socket.SHUT_RDWR)
                    ssl_conn.close()
                except:
                    pass
            print('Connection closed')

if __name__ == "__main__":
    create_server()
