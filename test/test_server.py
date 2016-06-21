
import unittest

from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

import modly.server as server

class TestServer(unittest.TestCase):

    def setUp(self):
        self.c = Client(
            server.get_instance('cacahootie', 'modly-test'), BaseResponse
        )

    def test_root(self):
        resp = self.c.get('/')
        self.assertEqual(resp.status_code, 404)

    def test_real_path(self):
        resp = self.c.get('/hello/helloworld/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, 'hello world')

    def test_echo(self):
        resp = self.c.get('/echo/?fred=rogers')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, '{"fred": "rogers"}')
