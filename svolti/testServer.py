import BaseHTTPServer
import CGIHTTPServer

address = ('', 8000)
handler = CGIHTTPServer.CGIHTTPRequestHandler
handler.cgi_directories=["/html", "elsewhere"]
server = BaseHTTPServer.HTTPServer(address, handler)
server.serve_forever()

