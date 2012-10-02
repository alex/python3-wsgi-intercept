#! /usr/bin/env python2.4
from wsgi_intercept import httplib2_intercept
from socket import gaierror
import wsgi_intercept
from test import wsgi_app
import httplib2

import py.test

_saved_debuglevel = None


def install(port=80):
    _saved_debuglevel, wsgi_intercept.debuglevel = wsgi_intercept.debuglevel, 1
    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('some_hopefully_nonexistant_domain', port, test_wsgi_app.create_fn)

def uninstall():
    wsgi_intercept.debuglevel = _saved_debuglevel
    httplib2_intercept.uninstall()

def test_success():
    install()
    http = httplib2.Http()
    resp, content = http.request('http://some_hopefully_nonexistant_domain:80/', 'GET')
    eq_(content, "WSGI intercept successful!\n")
    assert test_wsgi_app.success()
    uninstall()

def test_bogus_domain():
    install()
    wsgi_intercept.debuglevel = 1;
    py.test.raises(gaierror, 'httplib2_intercept.HTTP_WSGIInterceptorWithTimeout("_nonexistant_domain_").connect()')
    uninstall()

def test_https_success():
    install(443)
    http = httplib2.Http()
    resp, content = http.request('https://some_hopefully_nonexistant_domain/', 'GET')
    assert test_wsgi_app.success()
    uninstall()