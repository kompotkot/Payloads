"""
python2:
> python -m SimpleHTTPServer 7331
python3:
> python3 -m http.server 7331
"""

import http.server
import socketserver

PORT = 7070
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
