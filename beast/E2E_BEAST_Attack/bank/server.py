from http import cookies
import http.server
import ssl

# Define the handler to serve HTTP requests
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            response_body = b'Welcome to TAU Bank! This is the root page.'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', str(len(response_body)))
            self.send_header('Connection', 'keep-alive')
            if 'Cookie' not in self.headers:
                self.send_new_cookie()
            self.end_headers()
            self.wfile.write(response_body)
        else:
            response_body = b'404 Not Found'
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', str(len(response_body)))
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            self.wfile.write(response_body)

    def do_POST(self):
        # Read the length of the data
        content_length = int(self.headers['Content-Length'])
        # Read the POST data
        post_data = self.rfile.read(content_length)
        
        # Here you can process the post_data as needed.
        # For this example, we'll just echo the received data.
        response_body = b'Received POST data: ' + post_data

        # Send a response back to the client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(response_body)))
        self.send_header('Connection', 'keep-alive')
        self.end_headers()
        self.wfile.write(response_body)


    def send_new_cookie(self):
        new_cookie = cookies.SimpleCookie()
        new_cookie['session_id'] = 'Secret_Val'
        new_cookie['session_id']['path'] = '/'
        expires_time = 'Wed, 21 Oct 2026 07:28:00 GMT'
        new_cookie['session_id']['expires'] = expires_time
        new_cookie['session_id']['domain'] = '127.0.0.3'
        self.send_header('Set-Cookie', new_cookie.output(header='', sep=''))
        
# Create an HTTP server
httpd = http.server.HTTPServer(('127.0.0.3', 443), SimpleHTTPRequestHandler)

# Wrap the server with SSL
httpd.socket = ssl.wrap_socket(httpd.socket,
                               keyfile="server.key",
                               certfile="server.crt",
                               server_side=True,
                               ssl_version=ssl.PROTOCOL_TLSv1, 
                               ciphers='AES128-SHA')  # Specify the cipher

print("Serving on https://127.0.0.3:443")
httpd.serve_forever()
