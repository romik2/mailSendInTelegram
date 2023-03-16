import http.server
import socketserver
from http import HTTPStatus
import markdown
import flask_conn
from models import messages

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        i = self.path.index ( "?" ) + 1
        params = dict ( [ tuple ( p.split("=") ) for p in self.path[i:].split ( "&" ) ] )
        with flask_conn.app.app_context():
            messagesRes = messages.Messages.query.filter_by(key=params['key']).first()
        html_string = markdown.markdown(messagesRes.text_message)
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes('<meta charset="utf-8">' + html_string, 'utf-8'))


httpd = socketserver.TCPServer(('', 8001), Handler)
httpd.serve_forever()