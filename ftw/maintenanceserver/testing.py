from ftw.maintenanceserver.server import HTTPServer
from plone.testing import Layer
from threading import Thread
import os


DOCUMENT_ROOT = os.path.join(os.path.dirname(__file__), 'tests', 'htdocs')
PORT = int(os.environ.get('ZSERVER_PORT', 55001))


class ServerLayer(Layer):

    def setUp(self):
        self.httpd = HTTPServer(DOCUMENT_ROOT, PORT)
        self.thread = Thread(target=self.httpd.serve_forever)
        self.thread.start()
        self['URL'] = 'http://localhost:%i/' % PORT

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        while self.thread.isAlive():
            pass
        self.thread.join()


SERVER_LAYER = ServerLayer()
