import unittest

import modly

class TestImport(unittest.TestCase):

    def test_import_string(self):
        modstr = "a = 5"
        newmod = modly.get_module(modstr)
        self.assertEqual(newmod.a, 5)
