from http.server import SimpleHTTPRequestHandler, HTTPServer

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        elif self.path == '/sslApplet.class':
            self.path = 'sslApplet.class'
        return super().do_GET()

def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('127.0.0.3', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()