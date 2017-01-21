from __future__ import unicode_literals

import unittest


class VersionTest(unittest.TestCase):

    def setUp(self):
        from paka.cmark import get_version

        self.func = get_version

    def test_version_return_type_is_correct(self):
        result = self.func()
        self.assertIsInstance(result, str)

    def test_version_is_correct(self):
        self.assertEqual(self.func(), str("0.27.1"))
