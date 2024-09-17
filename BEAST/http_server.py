import http.server
import socketserver

# Define the request handler
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            response_body = b'Hello, world! This is the root page.'
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', str(len(response_body)))
            self.send_header('Connection', 'keep-alive')
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

# Define the server address and port
PORT = 5000
Handler = SimpleHTTPRequestHandler

# Create the HTTP server
with socketserver.TCPServer(('127.0.0.3', PORT), Handler) as httpd:
    print(f"Serving on http://127.0.0.3:{PORT}")
    httpd.serve_forever()
