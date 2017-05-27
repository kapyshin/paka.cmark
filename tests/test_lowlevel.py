# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import functools
import textwrap
import unittest


class IterationWithReplacementTest(unittest.TestCase):
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

    def setUp(self):
        from paka.cmark import lowlevel

        self.mod = lowlevel

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


class ListTypeTest(unittest.TestCase):

    def setUp(self):
        from paka.cmark import lowlevel

        self.mod = lowlevel

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


def expect_root(source):
    """Decorate test method so it'll get root of parsed source as argument."""
    def _wrapper(func):
        @functools.wraps(func)
        def _inner(self):
            text_bytes = self.mod.text_to_c(source)
            root = self.mod.parse_document(
                text_bytes, len(text_bytes), self.mod.OPT_DEFAULT)
            try:
                return func(self, root)
            finally:
                self.mod.node_free(root)
        return _inner
    return _wrapper


class TreeTraversalTest(unittest.TestCase):
    SAMPLE = textwrap.dedent("""\
        > Hello, Traversal!

        * a
        * b
        * c
        """)

    def setUp(self):
        from paka.cmark import lowlevel

        self.mod = lowlevel

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


class FenceInfoTest(unittest.TestCase):
    INFO = "something-interesting-here"

    def setUp(self):
        from paka.cmark import lowlevel

        self.mod = lowlevel

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


class LiteralTest(unittest.TestCase):
    CONTENTS = "here is some exciting new contents"

    def setUp(self):
        from paka.cmark import lowlevel

        self.mod = lowlevel

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
