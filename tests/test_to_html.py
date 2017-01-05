# -*- coding: utf-8 -*-

import unittest


class ToHTMLTest(unittest.TestCase):

    def setUp(self):
        from paka.cmark import to_html

        self.func = to_html

    def check(self, source, expected):
        self.assertEqual(self.func(source), expected)

    def test_empty(self):
        self.check(u"", u"")

    def test_ascii(self):
        self.check(u"Hello, Noob!", u"<p>Hello, Noob!</p>\n")

    def test_non_ascii(self):
        self.check(
            u"Проверяем *CommonMark*.\n\nВставляем `код`.\nИ другие штуки.",
            (
                u"<p>Проверяем <em>CommonMark</em>.</p>\n"
                u"<p>Вставляем <code>код</code>. И другие штуки.</p>\n"))
