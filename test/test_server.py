
import unittest

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

import modly.server as server


class _basetest(object):

    def test_root(self):
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 404)

    def test_real_path(self):
        resp = self.c.get('/hello/helloworld/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, 'hello world')

    def test_real_path_branch(self):
        resp = self.c.get('/hello/testbranch/helloworld/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, 'hello wurld')

    def test_echo(self):
        resp = self.c.get('/echo/echo?fred=rogers')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, '{\n  "fred": "rogers"\n}\n')


class TestServer(unittest.TestCase, _basetest):

    def setUp(self):
        self.c = Client(
            server.get_instance('cacahootie', 'modly-test'), BaseResponse
        )


class TestNocache(unittest.TestCase, _basetest):

    def setUp(self):
        self.c = Client(
            server.get_instance('cacahootie', 'modly-test', True), BaseResponse
        )
