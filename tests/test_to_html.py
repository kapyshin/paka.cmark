# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest


class ToHTMLTest(unittest.TestCase):
    SAMPLE = "Проверяем *CommonMark*.\n\nВставляем `код`.\nИ другие штуки."

    def setUp(self):
        from paka.cmark import to_html

        self.func = to_html

    def check(self, source, expected, **kwargs):
        self.assertEqual(self.func(source, **kwargs), expected)

    def test_empty(self):
        self.check("", "")

    def test_ascii(self):
        self.check("Hello, Noob!", "<p>Hello, Noob!</p>\n")

    def test_non_ascii(self):
        self.check(
            self.SAMPLE,
            (
                "<p>Проверяем <em>CommonMark</em>.</p>\n"
                "<p>Вставляем <code>код</code>. И другие штуки.</p>\n"))

    def test_breaks(self):
        self.check(
            self.SAMPLE,
            (
                "<p>Проверяем <em>CommonMark</em>.</p>\n"
                "<p>Вставляем <code>код</code>.\nИ другие штуки.</p>\n"),
            breaks=True)
