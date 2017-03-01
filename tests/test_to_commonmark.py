# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest


class ToCommonMarkTest(unittest.TestCase):
    def setUp(self):
        from paka.cmark import to_commonmark

        self.func = to_commonmark

    def check(self, source, expected, **kwargs):
        self.assertEqual(self.func(source, **kwargs), expected)

    def test_empty(self):
        self.check("", "\n")

    def test_newline(self):
        self.check("\n", "\n")

    def test_escape(self):
        self.check("Hello, Noob!\n", "Hello, Noob\\!\n")

    def test_list(self):
        self.check(" * a\n * b\n", "  - a\n  - b\n")

    def test_width(self):
        self.check("abc def ghi jkl", 'abc\ndef\nghi\njkl\n', width=5)
        self.check("abc def ghi jkl", 'abc def ghi jkl\n', width=0)
