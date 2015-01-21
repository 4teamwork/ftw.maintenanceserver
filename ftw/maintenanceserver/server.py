from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import os
import posixpath
import re
import socket
import urllib


def remove_virtual_host_monster_config(path):
    if 'VirtualHostBase' not in path.split('/'):
        return path

    path = re.sub(r'^\/VirtualHostBase\/.*\/VirtualHostRoot', r'', path)
    while path.startswith('/_vh_'):
        path = re.sub(r'/(_vh_[^/]+)/', '/', path)
    return path


class HTTPRequestHandler(SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()

        # Do not finish() when we have a broken pipe.
        try:
            self.handle()
        except socket.error:
            pass  # broken pipe
        except:
            self.finish()
            raise
        else:
            self.finish()

    do_POST = SimpleHTTPRequestHandler.do_GET

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Allow', 'GET,HEAD,POST,OPTIONS')
        self.end_headers()

    def translate_path(self, path):
        path = remove_virtual_host_monster_config(path)
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
