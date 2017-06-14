# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import textwrap

from testutils import LowlevelTestCase, expect_root, expect_first_child


class IterationWithReplacementTest(LowlevelTestCase):
    SAMPLE = textwrap.dedent("""\
        Проверяем *CommonMark*.

        Вставляем `код`.
        И [другие](https://example.org) штуки.

        <p>Test of <em>HTML</em>.</p>

        ```pycon
        Python 3.5.0 (default)
        [GCC] on linux
        Type "help" for more information.
        >>> a = 1
        >>> b = 3
        >>> a, b = b, a
        >>> print(a, b)
        3 1
        ```

        Можно ещё здесь что-нибудь написать.

        ```haskell
        Here is a candidate for reduction:

        > add :: Integer -> Integer -> Integer
        > add x y = (+) x y  -- xD
        ```
        """)
    NEW_CODE_BLOCK_TEMPLATE = (
        "<pre><code class=\"language-{}\"><b>It was:</b>\n"
        "&lt;|{}|&gt;\n</code></pre>")
    EXPECTED = textwrap.dedent("""\
        <p>Проверяем <em>CommonMark</em>.</p>
        <p>Вставляем <code>код</code>.
        И <a href="https://example.org">другие</a> штуки.</p>
        <p>Test of <em>HTML</em>.</p>
        <pre><code class="language-pycon"><b>It was:</b>
        &lt;|Python 3.5.0 (default)
        [GCC] on linux
        Type "help" for more information.
        >>> a = 1
        >>> b = 3
        >>> a, b = b, a
        >>> print(a, b)
        3 1
        |&gt;
        </code></pre>
        <p>Можно ещё здесь что-нибудь написать.</p>
        <pre><code class="language-haskell"><b>It was:</b>
        &lt;|Here is a candidate for reduction:

        > add :: Integer -> Integer -> Integer
        > add x y = (+) x y  -- xD
        |&gt;
        </code></pre>
        """)

    def _substitute_code_block_node(self, old_node):
        contents = self.mod.text_to_c(
            self.NEW_CODE_BLOCK_TEMPLATE.format(
                self.mod.text_from_c(self.mod.node_get_fence_info(old_node)),
                self.mod.text_from_c(self.mod.node_get_literal(old_node))))
        new_node = self.mod.node_new(self.mod.NODE_HTML_BLOCK)
        try:
            assert self.mod.node_set_literal(new_node, contents) == 1
            assert self.mod.node_replace(old_node, new_node) == 1
        except Exception:
            self.mod.node_free(new_node)
            raise
        self.mod.node_free(old_node)

    def _substitute_code_blocks(self, root):
        iter_ = self.mod.iter_new(root)
        try:
            while True:
                ev_type = self.mod.iter_next(iter_)
                if ev_type == self.mod.EVENT_DONE:
                    break
                elif ev_type == self.mod.EVENT_ENTER:
                    node = self.mod.iter_get_node(iter_)
                    node_type = self.mod.node_get_type(node)
                    if node_type == self.mod.NODE_CODE_BLOCK:
                        self._substitute_code_block_node(node)
        finally:
            self.mod.iter_free(iter_)

    def runTest(self):
        text_bytes = self.mod.text_to_c(self.SAMPLE)
        root = self.mod.parse_document(
            text_bytes, len(text_bytes), self.mod.OPT_DEFAULT)
        try:
            self._substitute_code_blocks(root)
            result = self.mod.text_from_c(
                self.mod.render_html(root, self.mod.OPT_DEFAULT))
        finally:
            self.mod.node_free(root)
        self.assertEqual(result, self.EXPECTED)


class IterationTest(LowlevelTestCase):
    SAMPLE = """\
        test1

        > test2.0
        > test2.1

        test3
        """

    @expect_root(SAMPLE)
    def test_get_root(self, root):
        iter_ = self.mod.iter_new(root)
        ev_type = None
        try:
            while ev_type != self.mod.EVENT_DONE:
                ev_type = self.mod.iter_next(iter_)
                self.assertEqual(root, self.mod.iter_get_root(iter_))
        finally:
            self.mod.iter_free(iter_)

    @expect_root(SAMPLE)
    def test_get_event_type(self, root):
        iter_ = self.mod.iter_new(root)
        ev_type = None
        try:
            while ev_type != self.mod.EVENT_DONE:
                ev_type = self.mod.iter_next(iter_)
                self.assertEqual(ev_type, self.mod.iter_get_event_type(iter_))
        finally:
            self.mod.iter_free(iter_)

    @expect_root(SAMPLE)
    def test_reset(self, root):
        event_for_tracing = self.mod.EVENT_ENTER

        def _get_trace(iter_):
            ev_type = None
            while ev_type != self.mod.EVENT_DONE:
                ev_type = self.mod.iter_next(iter_)
                if ev_type == event_for_tracing:
                    node = self.mod.iter_get_node(iter_)
                    yield node

        iter_ = self.mod.iter_new(root)
        try:
            full_trace = tuple(_get_trace(iter_))
        finally:
            self.mod.iter_free(iter_)

        iter_ = self.mod.iter_new(root)
        try:
            for n, start_node in enumerate(full_trace, start=1):
                self.mod.iter_reset(iter_, start_node, event_for_tracing)
                self.assertEqual(
                    tuple(_get_trace(iter_)), full_trace[n:])
        finally:
            self.mod.iter_free(iter_)


class ListTypeTest(LowlevelTestCase):

    def check(self, source, expected, preparer=lambda node: None):
        text_bytes = self.mod.text_to_c(source)
        root = self.mod.parse_document(
            text_bytes, len(text_bytes), self.mod.OPT_DEFAULT)
        node = self.mod.node_first_child(root)
        try:
            preparer(node)
            self.assertEqual(
                self.mod.node_get_list_type(node), expected)
        finally:
            self.mod.node_free(root)

    def test_bullet_list(self):
        source = textwrap.dedent("""\
            * zero
            * one
            """)
        self.check(source, self.mod.BULLET_LIST)

    def test_ordered_list(self):
        source = textwrap.dedent("""\
            1. one
            2. two
            """)
        self.check(source, self.mod.ORDERED_LIST)

    def test_no_list(self):
        self.check("Hello, List!\n", self.mod.NO_LIST)

    def test_changing_from_bullet_list_to_ordered(self):
        def _prepare_node(node):
            self.assertEqual(
                self.mod.node_get_list_type(node),
                self.mod.BULLET_LIST)
            assert self.mod.node_set_list_type(
                node, self.mod.ORDERED_LIST) == 1

        source = textwrap.dedent("""\
            * one
            * two
            """)
        self.check(source, self.mod.ORDERED_LIST, preparer=_prepare_node)


class TreeTraversalTest(LowlevelTestCase):
    SAMPLE = textwrap.dedent("""\
        > Hello, Traversal!

        * a
        * b
        * c
        """)

    @expect_root(SAMPLE)
    def test_next_exists(self, root):
        self.assertIsNotNone(
            self.mod.node_next(self.mod.node_first_child(root)))

    @expect_root(SAMPLE)
    def test_next_does_not_exist(self, root):
        self.assertIsNone(self.mod.node_next(root))

    @expect_root(SAMPLE)
    def test_previous_exists(self, root):
        self.assertIsNotNone(
            self.mod.node_previous(
                self.mod.node_next(self.mod.node_first_child(root))))

    @expect_root(SAMPLE)
    def test_previous_does_not_exist(self, root):
        self.assertIsNone(
            self.mod.node_previous(self.mod.node_first_child(root)))

    @expect_root(SAMPLE)
    def test_parent_exists(self, root):
        self.assertIsNotNone(
            self.mod.node_parent(self.mod.node_first_child(root)))

    @expect_root(SAMPLE)
    def test_parent_does_not_exist(self, root):
        self.assertIsNone(self.mod.node_parent(root))

    @expect_root(SAMPLE)
    def test_first_child_exists(self, root):
        self.assertIsNotNone(self.mod.node_first_child(root))

    @expect_root(SAMPLE)
    def test_first_child_does_not_exist(self, root):
        getter = self.mod.node_first_child
        self.assertIsNone(getter(getter(getter(getter(root)))))

    @expect_root(SAMPLE)
    def test_last_child_exists(self, root):
        self.assertIsNotNone(self.mod.node_last_child(root))

    @expect_root(SAMPLE)
    def test_last_child_does_not_exist(self, root):
        getter = self.mod.node_last_child
        self.assertIsNone(
            getter(getter(getter(getter(getter(root))))))


class FenceInfoTest(LowlevelTestCase):
    INFO = "something-interesting-here"

    def set_fence_info(self, node):
        return self.mod.node_set_fence_info(
            node, self.mod.text_to_c(self.INFO))

    def test_paragraph_node(self):
        node = self.mod.node_new(self.mod.NODE_PARAGRAPH)
        try:
            self.assertEqual(self.set_fence_info(node), 0)
            self.assertIsNone(self.mod.node_get_fence_info(node))
        finally:
            self.mod.node_free(node)

    def test_code_block_node(self):
        node = self.mod.node_new(self.mod.NODE_CODE_BLOCK)
        try:
            self.assertEqual(
                self.mod.text_from_c(self.mod.node_get_fence_info(node)),
                "")
            self.assertEqual(self.set_fence_info(node), 1)
            self.assertEqual(
                self.mod.text_from_c(self.mod.node_get_fence_info(node)),
                self.INFO)
        finally:
            self.mod.node_free(node)


class LiteralTest(LowlevelTestCase):
    CONTENTS = "here is some exciting new contents"

    def set_literal(self, node):
        return self.mod.node_set_literal(
            node, self.mod.text_to_c(self.CONTENTS))

    def test_supported_node_types(self):
        for node_type_name in (
                "NODE_HTML_BLOCK", "NODE_TEXT", "NODE_HTML_INLINE",
                "NODE_CODE", "NODE_CODE_BLOCK"):
            node = self.mod.node_new(getattr(self.mod, node_type_name))
            try:
                self.assertEqual(
                    self.mod.text_from_c(self.mod.node_get_literal(node)),
                    "")
                self.assertEqual(self.set_literal(node), 1)
                self.assertEqual(
                    self.mod.text_from_c(self.mod.node_get_literal(node)),
                    self.CONTENTS)
            finally:
                self.mod.node_free(node)

    def test_one_of_unsupported_node_types(self):
        node = self.mod.node_new(self.mod.NODE_PARAGRAPH)
        try:
            self.assertIsNone(self.mod.node_get_literal(node))
            self.assertEqual(self.set_literal(node), 0)
            self.assertIsNone(self.mod.node_get_literal(node))
        finally:
            self.mod.node_free(node)


class ListDelimiterTest(LowlevelTestCase):

    @expect_first_child("""\
        1) one
        2) two
        """)
    def test_paren_delim_list_node(self, node):
        self.assertEqual(
            self.mod.node_get_list_delim(node),
            self.mod.PAREN_DELIM)

    @expect_first_child("""\
        1. one
        2. two
        """)
    def test_period_delim_list_node(self, node):
        self.assertEqual(
            self.mod.node_get_list_delim(node),
            self.mod.PERIOD_DELIM)

    @expect_first_child("""\
        * one
        * two
        """)
    def test_no_delim_list_node(self, node):
        self.assertEqual(
            self.mod.node_get_list_delim(node),
            self.mod.NO_DELIM)

    @expect_first_child("""\
        one
        two
        """)
    def test_no_delim_non_list_node(self, node):
        self.assertEqual(
            self.mod.node_get_list_delim(node),
            self.mod.NO_DELIM)

    @expect_first_child("""\
        1) one
        2) two
        """)
    def test_changing_from_paren_to_period(self, node):
        self.assertEqual(
            self.mod.node_get_list_delim(node),
            self.mod.PAREN_DELIM)
        assert self.mod.node_set_list_delim(
            node, self.mod.PERIOD_DELIM) == 1
        self.assertEqual(
            self.mod.node_get_list_delim(node),
            self.mod.PERIOD_DELIM)


class NodeTypeStringTest(LowlevelTestCase):

    def check(self, node, expected):
        self.assertEqual(
            self.mod.text_from_c(self.mod.node_get_type_string(node)),
            expected)

    @expect_first_child("test")
    def test_paragraph(self, node):
        self.check(node, "paragraph")

    @expect_root("test")
    def test_document(self, node):
        self.check(node, "document")

    @expect_first_child("* a\n* b\n\n")
    def test_list(self, node):
        self.check(node, "list")


class HeadingLevelTest(LowlevelTestCase):

    def check(self, node, expected):
        self.assertEqual(
            self.mod.node_get_heading_level(node), expected)

    @expect_first_child("test")
    def test_non_heading(self, node):
        self.check(node, 0)

    @expect_first_child("# Heading")
    def test_h1(self, node):
        self.check(node, 1)

    @expect_first_child("## Heading")
    def test_h2(self, node):
        self.check(node, 2)

    @expect_first_child("### Heading")
    def test_h3(self, node):
        self.check(node, 3)

    @expect_first_child("#### Heading")
    def test_h4(self, node):
        self.check(node, 4)

    @expect_first_child("##### Heading")
    def test_h5(self, node):
        self.check(node, 5)

    @expect_first_child("###### Heading")
    def test_h6(self, node):
        self.check(node, 6)

    @expect_first_child("####### Heading")
    def test_too_many_chars_for_atx_heading(self, node):
        self.check(node, 0)

    @expect_first_child("Heading\n=======\n\n")
    def test_setting(self, node):
        self.check(node, 1)
        assert self.mod.node_set_heading_level(node, 5) == 1
        self.check(node, 5)


class ListStartTest(LowlevelTestCase):

    def check(self, node, expected):
        self.assertEqual(self.mod.node_get_list_start(node), expected)

    @expect_first_child("* one\n* two\n\n")
    def test_unordered_list(self, node):
        self.check(node, 0)

    @expect_first_child("1. one\n2. two\n\n")
    def test_ordered_list_started_at_1(self, node):
        self.check(node, 1)

    @expect_first_child("7. one\n8. two\n\n")
    def test_ordered_list_started_at_7(self, node):
        self.check(node, 7)

    @expect_first_child("1. one\n2. two\n\n")
    def test_setting(self, node):
        self.check(node, 1)
        assert self.mod.node_set_list_start(node, 9) == 1
        self.check(node, 9)


class ListTightTest(LowlevelTestCase):

    def check(self, node, expected):
        self.assertEqual(
            self.mod.node_get_list_tight(node), expected)

    @expect_first_child("one two")
    def test_non_list(self, node):
        self.check(node, 0)

    @expect_first_child("""\
        * one

        * two
        """)
    def test_loose(self, node):
        self.check(node, 0)

    @expect_first_child("""\
        * one
        * two
        """)
    def test_tight(self, node):
        self.check(node, 1)

    @expect_first_child("""\
        * one

        * two
        """)
    def test_setting(self, node):
        self.check(node, 0)
        assert self.mod.node_set_list_tight(node, 1) == 1
        self.check(node, 1)


class UrlTest(LowlevelTestCase):

    def check(self, node, expected):
        self.assertEqual(
            self.mod.text_from_c(self.mod.node_get_url(node)),
            expected)

    @expect_first_child("[text](//example.org/link/)")
    def test_link(self, parent_node):
        node = self.mod.node_first_child(parent_node)
        self.check(node, "//example.org/link/")

    @expect_first_child("![image](//example.org/image/)")
    def test_image(self, parent_node):
        node = self.mod.node_first_child(parent_node)
        self.check(node, "//example.org/image/")

    @expect_first_child("just paragraph")
    def test_other_kind_of_node(self, node):
        self.assertIsNone(self.mod.node_get_url(node))
        self.check(node, "")

    @expect_first_child("[text](//example.org/link/)")
    def test_setting_for_link(self, parent_node):
        node = self.mod.node_first_child(parent_node)
        self.check(node, "//example.org/link/")
        assert self.mod.node_set_url(
            node, self.mod.text_to_c("//example.org/new/")) == 1
        self.check(node, "//example.org/new/")

    @expect_first_child("![image](//example.org/image/)")
    def test_setting_for_image(self, parent_node):
        node = self.mod.node_first_child(parent_node)
        self.check(node, "//example.org/image/")
        assert self.mod.node_set_url(
            node, self.mod.text_to_c("//example.org/other/")) == 1
        self.check(node, "//example.org/other/")


class TitleTest(LowlevelTestCase):

    def check(self, node, expected):
        self.assertEqual(
            self.mod.text_from_c(self.mod.node_get_title(node)),
            expected)

    @expect_first_child("[text](//example.org/link/ \"link title\")")
    def test_link(self, parent_node):
        node = self.mod.node_first_child(parent_node)
        self.check(node, "link title")

    @expect_first_child("![text](//example.org/image/ \"image title\")")
    def test_image(self, parent_node):
        node = self.mod.node_first_child(parent_node)
        self.check(node, "image title")

    @expect_first_child("just paragraph")
    def test_other_kind_of_node(self, node):
        self.assertIsNone(self.mod.node_get_title(node))
        self.check(node, "")

    @expect_first_child("[text](//example.org/link/ \"link title\")")
    def test_setting_for_link(self, parent_node):
        node = self.mod.node_first_child(parent_node)
        self.check(node, "link title")
        assert self.mod.node_set_title(
            node, self.mod.text_to_c("completely different")) == 1
        self.check(node, "completely different")

    @expect_first_child("![text](//example.org/image/ \"image title\")")
    def test_setting_for_image(self, parent_node):
        node = self.mod.node_first_child(parent_node)
        self.check(node, "image title")
        assert self.mod.node_set_title(
            node, self.mod.text_to_c("just an image")) == 1
        self.check(node, "just an image")


class LineAndColumnTest(LowlevelTestCase):
    SAMPLE = """\
        No such file or directory.
        Command not found.
        rm -rf.

        Headache.
        Touchpad does not work.
        Don't sleep on the laptop.
        """

    def get_info(self, root, expected_node_types):
        iter_ = self.mod.iter_new(root)
        ev_type = None
        try:
            while ev_type != self.mod.EVENT_DONE:
                ev_type = self.mod.iter_next(iter_)
                if ev_type != self.mod.EVENT_ENTER:
                    continue
                node = self.mod.iter_get_node(iter_)
                node_type = self.mod.node_get_type(node)
                if node_type not in expected_node_types:
                    continue
                yield (
                    self.mod.text_from_c(
                        self.mod.node_get_type_string(node)),
                    self.mod.node_get_start_line(node),
                    self.mod.node_get_start_column(node),
                    self.mod.node_get_end_line(node),
                    self.mod.node_get_end_column(node))
        finally:
            self.mod.iter_free(iter_)

    @expect_root(SAMPLE)
    def runTest(self, root):
        expected_types = {self.mod.NODE_DOCUMENT, self.mod.NODE_PARAGRAPH}
        expected = (
            ("document", 1, 1, 7, 26),
            ("paragraph", 1, 1, 3, 7),
            ("paragraph", 5, 1, 7, 26))
        self.assertEqual(
            tuple(self.get_info(root, expected_types)), expected)


class StreamingParserTest(LowlevelTestCase):
    SAMPLE = textwrap.dedent("""\
        Let's check that streaming parser emits node tree
        that *looks* like one built by
        [`simple`](http://example.org) parser.

        To do this, we'll build **trace** for each of node
        trees, and then compare (with `assertEqual`) them
        as tuples.
        """)

    def get_trace(self, root):
        def _gen(it):
            ev_type = None
            while ev_type != self.mod.EVENT_DONE:
                ev_type = self.mod.iter_next(it)
                if ev_type == self.mod.EVENT_ENTER:
                    yield self.mod.text_from_c(
                        self.mod.node_get_type_string(
                            self.mod.iter_get_node(it)))

        iter_ = self.mod.iter_new(root)
        try:
            for item in _gen(iter_):  # py27 (yield from)
                yield item
        finally:
            self.mod.iter_free(iter_)

    @expect_root(SAMPLE)
    def test_side_by_side(self, simple_root):
        parser = self.mod.parser_new(self.mod.OPT_DEFAULT)
        try:
            for line in self.SAMPLE.splitlines(True):  # py27 (kwarg)
                buf = self.mod.text_to_c(line)
                self.mod.parser_feed(parser, buf, len(buf))
            streaming_root = self.mod.parser_finish(parser)
        finally:
            self.mod.parser_free(parser)
        try:
            simple_root_trace = tuple(self.get_trace(simple_root))
            self.assertIn("link", simple_root_trace)
            self.assertIn("code", simple_root_trace)
            self.assertIn("paragraph", simple_root_trace)
            self.assertEqual(
                simple_root_trace,
                tuple(self.get_trace(streaming_root)))
        finally:
            self.mod.node_free(streaming_root)

    def test_nothing_fed(self):
        parser = self.mod.parser_new(self.mod.OPT_DEFAULT)
        try:
            root = self.mod.parser_finish(parser)
        finally:
            self.mod.parser_free(parser)
        self.assertEqual(tuple(self.get_trace(root)), ("document", ))


class TreeManipulationTest(LowlevelTestCase):

    def check(self, root, expected):
        result = self.mod.text_from_c(
            self.mod.render_html(root, self.mod.OPT_DEFAULT))
        self.assertEqual(result, expected)

    @expect_root("Some text here.")
    def test_unlink(self, root):
        node = self.mod.node_first_child(root)
        self.mod.node_unlink(node)
        try:
            self.check(root, "")
        finally:
            self.mod.node_free(node)

    @expect_root("Insert before this.")
    def test_insert_before(self, root):
        existing_node = self.mod.node_first_child(root)

        new_node = self.mod.node_new(self.mod.NODE_HTML_BLOCK)
        try:
            assert self.mod.node_set_literal(
                new_node, self.mod.text_to_c("<p>test</p>")) == 1
            assert self.mod.node_insert_before(existing_node, new_node) == 1
        except Exception:
            self.mod.node_free(new_node)
            raise

        self.check(root, "<p>test</p>\n<p>Insert before this.</p>\n")

    @expect_root("Insert after this.")
    def test_insert_after(self, root):
        existing_node = self.mod.node_first_child(root)

        new_node = self.mod.node_new(self.mod.NODE_HTML_BLOCK)
        try:
            assert self.mod.node_set_literal(
                new_node, self.mod.text_to_c("<p>test</p>")) == 1
            assert self.mod.node_insert_after(existing_node, new_node) == 1
        except Exception:
            self.mod.node_free(new_node)
            raise

        self.check(root, "<p>Insert after this.</p>\n<p>test</p>\n")

    @expect_root("Replace this.")
    def test_replace(self, root):
        existing_node = self.mod.node_first_child(root)

        new_node = self.mod.node_new(self.mod.NODE_HTML_BLOCK)
        try:
            assert self.mod.node_set_literal(
                new_node, self.mod.text_to_c("<p>test</p>")) == 1
            assert self.mod.node_replace(existing_node, new_node) == 1
        except Exception:
            self.mod.node_free(new_node)
            raise

        try:
            self.check(root, "<p>test</p>\n")
        finally:
            self.mod.node_free(existing_node)

    @expect_root("Add sibling before.")
    def test_prepend_child(self, root):
        new_node = self.mod.node_new(self.mod.NODE_HTML_BLOCK)
        try:
            assert self.mod.node_set_literal(
                new_node, self.mod.text_to_c("<p>test</p>")) == 1
            assert self.mod.node_prepend_child(root, new_node) == 1
        except Exception:
            self.mod.node_free(new_node)
            raise

        self.check(root, "<p>test</p>\n<p>Add sibling before.</p>\n")

    @expect_root("Add sibling after.")
    def test_append_child(self, root):
        new_node = self.mod.node_new(self.mod.NODE_HTML_BLOCK)
        try:
            assert self.mod.node_set_literal(
                new_node, self.mod.text_to_c("<p>test</p>")) == 1
            assert self.mod.node_append_child(root, new_node) == 1
        except Exception:
            self.mod.node_free(new_node)
            raise

        self.check(root, "<p>Add sibling after.</p>\n<p>test</p>\n")

    @expect_root("One.")
    def test_consolidate_text_nodes(self, root):
        def _count_text_nodes(root):
            count = 0
            iter_ = self.mod.iter_new(root)
            try:
                ev_type = None
                while ev_type != self.mod.EVENT_DONE:
                    ev_type = self.mod.iter_next(iter_)
                    if ev_type == self.mod.EVENT_ENTER:
                        node = self.mod.iter_get_node(iter_)
                        if self.mod.node_get_type(node) != self.mod.NODE_TEXT:
                            continue
                        count += 1
            finally:
                self.mod.iter_free(iter_)
            return count

        self.assertEqual(_count_text_nodes(root), 1)

        paragraph = self.mod.node_first_child(root)

        new_node = self.mod.node_new(self.mod.NODE_TEXT)
        try:
            self.mod.node_set_literal(
                new_node, self.mod.text_to_c(" Two.")) == 1
            self.mod.node_append_child(paragraph, new_node) == 1
        except Exception:
            self.mod.node_free(new_node)
            raise
        self.assertEqual(_count_text_nodes(root), 2)

        self.mod.consolidate_text_nodes(root)
        self.assertEqual(_count_text_nodes(root), 1)
        self.check(root, "<p>One. Two.</p>\n")


class HelpersTest(LowlevelTestCase):

    def test_text_from_c_can_handle_none(self):
        self.assertEqual(self.mod.text_from_c(None), "")
