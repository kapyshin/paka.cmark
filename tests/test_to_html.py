# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest


class ToHTMLTest(unittest.TestCase):
    SAMPLE = (
        "Проверяем *CommonMark*.\n\nВставляем `код`.\nИ другие штуки.\n\n"
        "<p>Test of <em>HTML</em>.</p>")

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
                "<p>Вставляем <code>код</code>. И другие штуки.</p>\n"
                "<p>Test of <em>HTML</em>.</p>\n"))

    def test_breaks(self):
        self.check(
            self.SAMPLE,
            (
                "<p>Проверяем <em>CommonMark</em>.</p>\n"
                "<p>Вставляем <code>код</code>.\nИ другие штуки.</p>\n"
                "<p>Test of <em>HTML</em>.</p>\n"),
            breaks=True)

    def test_safe(self):
        self.check(
            self.SAMPLE,
            (
                "<p>Проверяем <em>CommonMark</em>.</p>\n"
                "<p>Вставляем <code>код</code>. И другие штуки.</p>\n"
                "<!-- raw HTML omitted -->\n"),
            safe=True)

    def test_breaks_and_safe(self):
        self.check(
            self.SAMPLE,
            (
                "<p>Проверяем <em>CommonMark</em>.</p>\n"
                "<p>Вставляем <code>код</code>.\nИ другие штуки.</p>\n"
                "<!-- raw HTML omitted -->\n"),
            breaks=True, safe=True)
