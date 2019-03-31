# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest


class ToHTMLTest(unittest.TestCase):
    SAMPLE = (
        "Проверяем *CommonMark*.\n\nВставляем `код`.\nИ "
        "[другие](https://example.org) [штуки](javascript:pwnd).\n\n"
        "<p>Test of <em>HTML</em>.</p>\n\n"
        "Проверка---\"test\" -- test.")

    def setUp(self):
        from paka.cmark import LineBreaks, to_html

        self.func = to_html
        self.line_breaks = LineBreaks

    def check(self, source, expected, **kwargs):
        kwargs.setdefault("safe", False)
        self.assertEqual(self.func(source, **kwargs), expected)

    def test_empty(self):
        self.check("", "")

    def test_ascii(self):
        self.check("Hello, Noob!", "<p>Hello, Noob!</p>\n")

    def test_no_breaks(self):
        expected = (
            "<p>Проверяем <em>CommonMark</em>.</p>\n"
            "<p>Вставляем <code>код</code>. И "
            "<a href=\"https://example.org\">другие</a> "
            "<a href=\"javascript:pwnd\">штуки</a>.</p>\n"
            "<p>Test of <em>HTML</em>.</p>\n"
            "<p>Проверка---&quot;test&quot; -- test.</p>\n")
        self.check(self.SAMPLE, expected)
        self.check(self.SAMPLE, expected, breaks=False)

    def test_soft_breaks(self):
        expected = (
            "<p>Проверяем <em>CommonMark</em>.</p>\n"
            "<p>Вставляем <code>код</code>.\nИ "
            "<a href=\"https://example.org\">другие</a> "
            "<a href=\"javascript:pwnd\">штуки</a>.</p>\n"
            "<p>Test of <em>HTML</em>.</p>\n"
            "<p>Проверка---&quot;test&quot; -- test.</p>\n")
        self.check(self.SAMPLE, expected, breaks=True)
        self.check(self.SAMPLE, expected, breaks=self.line_breaks.soft)
        self.check(self.SAMPLE, expected, breaks="soft")

    def test_hard_breaks(self):
        expected = (
            "<p>Проверяем <em>CommonMark</em>.</p>\n"
            "<p>Вставляем <code>код</code>.<br />\nИ "
            "<a href=\"https://example.org\">другие</a> "
            "<a href=\"javascript:pwnd\">штуки</a>.</p>\n"
            "<p>Test of <em>HTML</em>.</p>\n"
            "<p>Проверка---&quot;test&quot; -- test.</p>\n")
        self.check(self.SAMPLE, expected, breaks=self.line_breaks.hard)
        self.check(self.SAMPLE, expected, breaks="hard")

    def test_no_breaks_and_safe(self):
        expected = (
            "<p>Проверяем <em>CommonMark</em>.</p>\n"
            "<p>Вставляем <code>код</code>. И "
            "<a href=\"https://example.org\">другие</a> "
            "<a href=\"\">штуки</a>.</p>\n"
            "<!-- raw HTML omitted -->\n"
            "<p>Проверка---&quot;test&quot; -- test.</p>\n")
        self.check(self.SAMPLE, expected, safe=True)
        self.check(self.SAMPLE, expected, breaks=False, safe=True)

    def test_soft_breaks_and_safe(self):
        expected = (
            "<p>Проверяем <em>CommonMark</em>.</p>\n"
            "<p>Вставляем <code>код</code>.\nИ "
            "<a href=\"https://example.org\">другие</a> "
            "<a href=\"\">штуки</a>.</p>\n"
            "<!-- raw HTML omitted -->\n"
            "<p>Проверка---&quot;test&quot; -- test.</p>\n")
        self.check(self.SAMPLE, expected, breaks=True, safe=True)
        self.check(
            self.SAMPLE, expected, breaks=self.line_breaks.soft, safe=True)
        self.check(self.SAMPLE, expected, breaks="soft", safe=True)

    def test_hard_breaks_and_safe(self):
        expected = (
            "<p>Проверяем <em>CommonMark</em>.</p>\n"
            "<p>Вставляем <code>код</code>.<br />\nИ "
            "<a href=\"https://example.org\">другие</a> "
            "<a href=\"\">штуки</a>.</p>\n"
            "<!-- raw HTML omitted -->\n"
            "<p>Проверка---&quot;test&quot; -- test.</p>\n")
        self.check(
            self.SAMPLE, expected, breaks=self.line_breaks.hard, safe=True)
        self.check(self.SAMPLE, expected, breaks="hard", safe=True)

    def test_no_breaks_and_sourcepos(self):
        expected = (
            "<p data-sourcepos=\"1:1-1:32\">Проверяем <em>CommonMark"
            "</em>.</p>\n<p data-sourcepos=\"3:1-4:69\">Вставляем "
            "<code>код</code>. И <a href=\"https://example.org\">другие</a> "
            "<a href=\"javascript:pwnd\">штуки</a>.</p>\n"
            "<p>Test of <em>HTML</em>.</p>\n"
            "<p data-sourcepos=\"8:1-8:34\">Проверка---&quot;test&quot; "
            "-- test.</p>\n")
        self.check(self.SAMPLE, expected, sourcepos=True)
        self.check(self.SAMPLE, expected, breaks=False, sourcepos=True)

    def test_no_breaks_and_smart(self):
        expected = (
            "<p>Проверяем <em>CommonMark</em>.</p>\n"
            "<p>Вставляем <code>код</code>. И "
            "<a href=\"https://example.org\">другие</a> "
            "<a href=\"javascript:pwnd\">штуки</a>.</p>\n"
            "<p>Test of <em>HTML</em>.</p>\n"
            "<p>Проверка—“test” – test.</p>\n")
        self.check(self.SAMPLE, expected, smart=True)
        self.check(self.SAMPLE, expected, breaks=False, smart=True)
