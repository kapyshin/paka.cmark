from __future__ import unicode_literals

import unittest


class VersionTest(unittest.TestCase):

    def setUp(self):
        from paka.cmark import get_version

        self.func = get_version

    def test_version_is_correct(self):
        self.assertEqual(self.func(), u"0.30.2")
