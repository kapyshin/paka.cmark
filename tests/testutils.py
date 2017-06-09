import unittest
import textwrap
import functools


def expect_root(source, transformer=lambda mod, root: root):
    """Decorate test method so it'll get root of parsed source as argument."""
    def _wrapper(func):
        @functools.wraps(func)
        def _inner(self):
            text_bytes = self.mod.text_to_c(textwrap.dedent(source))
            root = self.mod.parse_document(
                text_bytes, len(text_bytes), self.mod.OPT_DEFAULT)
            try:
                return func(self, transformer(self.mod, root))
            finally:
                self.mod.node_free(root)
        return _inner
    return _wrapper


expect_first_child = functools.partial(
    expect_root, transformer=lambda mod, root: mod.node_first_child(root))


class LowlevelTestCase(unittest.TestCase):

    def setUp(self):
        from paka.cmark import lowlevel

        self.mod = lowlevel
