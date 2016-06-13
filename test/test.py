import unittest

import modly.getters as getters

class TestImport(unittest.TestCase):

    def test_import_string(self):
        modstr = "a = 5"
        newmod = getters.get_module(modstr)
        self.assertEqual(newmod.a, 5)

    def test_github_string(self):
        teststr = getters.get_github_string(
            'cacahootie', 'modly', 'test/tmod.py'
        )
        self.assertTrue("a = 11" in teststr)

    def test_github_module(self):
        testmod = getters.get_github_module(
            'cacahootie', 'modly', 'test/tmod.py', 'tmod'
        )
        self.assertEqual(testmod.a, 11)
        self.assertEqual(testmod.b, 12)
