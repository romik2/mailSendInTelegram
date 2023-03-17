import http.server
import socketserver
from http import HTTPStatus
import flask_conn
from models import messages

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        i = self.path.index ( "?" ) + 1
        params = dict ( [ tuple ( p.split("=") ) for p in self.path[i:].split ( "&" ) ] )
        with flask_conn.app.app_context():
            messagesRes = messages.Messages.query.filter_by(key=params['key']).first()
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(messagesRes.text_message)


httpd = socketserver.TCPServer(('', 8001), Handler)
httpd.serve_forever()
