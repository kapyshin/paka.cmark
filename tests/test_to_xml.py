# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import textwrap
import unittest


class ToXMLTest(unittest.TestCase):
    SAMPLE = (
        "Проверяем *CommonMark*.\n\nВставляем `код`.\nИ другие "
        "[штуки](javascript:pwned).\n\n<p>Test of <em>XML</em>.</p>\n\n"
        "Проверка---\"test\" -- test.")

    def setUp(self):
        from paka.cmark import to_xml

        self.func = to_xml

    def check(self, source, expected, **kwargs):
        self.assertEqual(self.func(source, **kwargs), expected)

    def test_empty(self):
        expected = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE document SYSTEM "CommonMark.dtd">
            <document xmlns="http://commonmark.org/xml/1.0" />
            """)
        self.check("", expected)

    def test_ascii(self):
        expected = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE document SYSTEM "CommonMark.dtd">
            <document xmlns="http://commonmark.org/xml/1.0">
              <paragraph>
                <text>Hello, XML!</text>
              </paragraph>
            </document>
            """)
        self.check("Hello, XML!", expected)

    def test_sample(self):
        expected = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE document SYSTEM "CommonMark.dtd">
            <document xmlns="http://commonmark.org/xml/1.0">
              <paragraph>
                <text>Проверяем </text>
                <emph>
                  <text>CommonMark</text>
                </emph>
                <text>.</text>
              </paragraph>
              <paragraph>
                <text>Вставляем </text>
                <code>код</code>
                <text>.</text>
                <softbreak />
                <text>И другие </text>
                <link destination="javascript:pwned" title="">
                  <text>штуки</text>
                </link>
                <text>.</text>
              </paragraph>
              <html_block>&lt;p&gt;Test of &lt;em&gt;XML&lt;/em&gt;.&lt;/p&gt;
            </html_block>
              <paragraph>
                <text>Проверка---&quot;test&quot; -- test.</text>
              </paragraph>
            </document>
            """)
        self.check(self.SAMPLE, expected)
        self.check(self.SAMPLE, expected, sourcepos=False)

    def test_sourcepos(self):
        expected = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE document SYSTEM "CommonMark.dtd">
            <document sourcepos="1:1-8:34" xmlns="http://commonmark.org/xml/1.0">
              <paragraph sourcepos="1:1-1:32">
                <text sourcepos="1:1-1:19">Проверяем </text>
                <emph sourcepos="1:20-1:31">
                  <text sourcepos="1:21-1:30">CommonMark</text>
                </emph>
                <text sourcepos="1:32-1:32">.</text>
              </paragraph>
              <paragraph sourcepos="3:1-4:47">
                <text sourcepos="3:1-3:19">Вставляем </text>
                <code sourcepos="3:21-3:26">код</code>
                <text sourcepos="3:28-3:28">.</text>
                <softbreak />
                <text sourcepos="4:1-4:16">И другие </text>
                <link sourcepos="4:17-4:46" destination="javascript:pwned" title="">
                  <text sourcepos="4:18-4:27">штуки</text>
                </link>
                <text sourcepos="4:47-4:47">.</text>
              </paragraph>
              <html_block sourcepos="6:1-6:28">&lt;p&gt;Test of &lt;em&gt;XML&lt;/em&gt;.&lt;/p&gt;
            </html_block>
              <paragraph sourcepos="8:1-8:34">
                <text sourcepos="8:1-8:34">Проверка---&quot;test&quot; -- test.</text>
              </paragraph>
            </document>
            """)
        self.check(self.SAMPLE, expected, sourcepos=True)

    def test_smart(self):
        expected = textwrap.dedent("""\
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE document SYSTEM "CommonMark.dtd">
            <document xmlns="http://commonmark.org/xml/1.0">
              <paragraph>
                <text>Проверяем </text>
                <emph>
                  <text>CommonMark</text>
                </emph>
                <text>.</text>
              </paragraph>
              <paragraph>
                <text>Вставляем </text>
                <code>код</code>
                <text>.</text>
                <softbreak />
                <text>И другие </text>
                <link destination="javascript:pwned" title="">
                  <text>штуки</text>
                </link>
                <text>.</text>
              </paragraph>
              <html_block>&lt;p&gt;Test of &lt;em&gt;XML&lt;/em&gt;.&lt;/p&gt;
            </html_block>
              <paragraph>
                <text>Проверка—“test” – test.</text>
              </paragraph>
            </document>
            """)
        self.check(self.SAMPLE, expected, smart=True)
