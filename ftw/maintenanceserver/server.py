from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import os
import posixpath
import urllib


class HTTPRequestHandler(SimpleHTTPRequestHandler):

    do_POST = SimpleHTTPRequestHandler.do_GET

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Allow', 'GET,HEAD,POST,OPTIONS')
        self.end_headers()

    def translate_path(self, path):
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)

        document_root = os.path.abspath(self.server.document_root)
        index = os.path.join(document_root, 'index.html')
        filepath = os.path.abspath(os.path.join(document_root, *words))

        if not os.path.isfile(filepath):
            return index

        elif not filepath.startswith(document_root):
            return index

        else:
            return filepath


class HTTPServer(SocketServer.TCPServer):

    allow_reuse_address = True

    def __init__(self, document_root, port):
        self.document_root = document_root
        SocketServer.TCPServer.__init__(
            self, ('localhost', port), HTTPRequestHandler)


def command(document_root, port):
    HTTPServer(document_root, port).serve_forever()
