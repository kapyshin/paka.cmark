# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest


class ToHTMLTest(unittest.TestCase):

    def setUp(self):
        from paka.cmark import to_html

        self.func = to_html

    def check(self, source, expected):
        self.assertEqual(self.func(source), expected)

    def test_empty(self):
        self.check("", "")

    def test_ascii(self):
        self.check("Hello, Noob!", "<p>Hello, Noob!</p>\n")

    def test_non_ascii(self):
        self.check(
            "Проверяем *CommonMark*.\n\nВставляем `код`.\nИ другие штуки.",
            (
                "<p>Проверяем <em>CommonMark</em>.</p>\n"
                "<p>Вставляем <code>код</code>. И другие штуки.</p>\n"))
