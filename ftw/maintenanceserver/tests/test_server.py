from ftw.maintenanceserver.testing import SERVER_LAYER
from ftw.testbrowser import browser
from ftw.testbrowser import browsing
from StringIO import StringIO
from unittest2 import TestCase
import os.path
import sys


def catch_stderr(func):
    def stderr_catcher(*args, **kwargs):
        ori_stderr = sys.stderr
        sys.stderr = StringIO()
        try:
            return func(*args, **kwargs)
        except:
            print sys.stderr.getvalue()
            raise
        finally:
            sys.stderr = ori_stderr
    return stderr_catcher


class TestServer(TestCase):
    layer = SERVER_LAYER

    def open(self, path, method='GET'):
        url = os.path.join(self.layer['URL'], path)
        browser.open(url, method=method)

    def setUp(self):
        # We actually *expect* the maintenance server to produce
        # "HTTP Errors", such as "503 Service Unavailable"
        browser.raise_http_errors = False

    @browsing
    @catch_stderr
    def test_server_serves_index_html(self, browser):
        self.open('')
        self.assertEquals('Maintenance', browser.css('h1').first.text)

    @browsing
    @catch_stderr
    def test_directory_requests_falls_back_to_index(self, browser):
        self.open('images')
        self.assertEquals('Maintenance', browser.css('h1').first.text)

    @browsing
    @catch_stderr
    def test_resources_are_served(self, browser):
        self.open('images/logo.png')
        self.assertEquals('TheLogo', browser.contents.strip())

    @browsing
    @catch_stderr
    def test_restricted_to_document_root(self, browser):
        self.open('../__init__.py')
        self.assertEquals('Maintenance', browser.css('h1').first.text)

    @browsing
    @catch_stderr
    def test_POST_request_falls_back_to_GET(self, browser):
        self.open('', method='POST')
        self.assertEquals('Maintenance', browser.css('h1').first.text)

    @browsing
    @catch_stderr
    def test_HEAD_request(self, browser):
        # Respond to HEAD with 503 so that it is not cached.
        self.open('', method='HEAD')
        self.assertEquals(503, browser.status_code)
        self.assertEquals('text/html',
                          browser.headers.get('Content-Type'))

    @browsing
    @catch_stderr
    def test_OPTIONS_request(self, browser):
        # Options must be answered with 200 OK, otherwise HaProxy would
        # take the backend offline.
        # But since we want Varnish not to cache it, no matter how it is
        # configured, we set a cache-control header.
        self.open('', method='OPTIONS')
        self.assertEquals(200, browser.status_code)
        self.assertEquals('GET,HEAD,POST,OPTIONS',
                          browser.headers.get('Allow'))
        self.assertEquals('no-cache',
                          browser.headers.get('Cache-Control'))

    @browsing
    @catch_stderr
    def test_GET_responded_with_503(self, browser):
        # Respond to GET with 503 so that it is not cached.
        self.open('', method='GET')
        self.assertEquals(503, browser.status_code)
        self.assertEquals('Service Unavailable', browser.status_reason)

    @browsing
    @catch_stderr
    def test_POST_responded_with_503(self, browser):
        # Respond to POST with 503 so that it is not cached.
        self.open('', method='POST')
        self.assertEquals(503, browser.status_code)
        self.assertEquals('Service Unavailable', browser.status_reason)

    @browsing
    @catch_stderr
    def test_virtualHostMonster_configuration_is_removed(self, browser):
        self.open('VirtualHostBase/http/localhost:8080/mountpoint/'
                  'Plone/VirtualHostRoot/images/logo.png')
        self.assertEquals('TheLogo', browser.contents.strip())

    @browsing
    @catch_stderr
    def test_virtualHostMonster_inside_out_urls(self, browser):
        self.open('VirtualHostBase/http/localhost:8080/mountpoint/'
                  'Plone/VirtualHostRoot/_vh_the/_vh_site/images/logo.png')
        self.assertEquals('TheLogo', browser.contents.strip())

    @browsing
    @catch_stderr
    def test_resources_get_200(self, browser):
        self.open('images/logo.png')
        self.assertEquals(200, browser.status_code)
