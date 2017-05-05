"""Direct (low-level) bindings to C library.

Using these may be dangerous, as unlike with high-level ones,
you are responsible for error checking and correct memory management
(use of ``node_free``, ``iter_free``, etc.).

Most members of this module are taken directly from C library,
but their names do not have ``cmark_`` or ``CMARK_`` prefixes.

"""

from paka.cmark._cmark import ffi as _ffi, lib as _lib


_ENCODING = "utf-8"

OPT_DEFAULT = _lib.CMARK_OPT_DEFAULT

EVENT_ENTER = _lib.CMARK_EVENT_ENTER
EVENT_DONE = _lib.CMARK_EVENT_DONE

NODE_CODE_BLOCK = _lib.CMARK_NODE_CODE_BLOCK
NODE_HTML_BLOCK = _lib.CMARK_NODE_HTML_BLOCK


# pylint: disable=invalid-name

parse_document = _lib.cmark_parse_document

node_new = _lib.cmark_node_new
node_free = _lib.cmark_node_free

node_replace = _lib.cmark_node_replace

node_get_type = _lib.cmark_node_get_type
node_get_fence_info = _lib.cmark_node_get_fence_info
node_get_literal = _lib.cmark_node_get_literal
node_set_literal = _lib.cmark_node_set_literal

iter_new = _lib.cmark_iter_new
iter_free = _lib.cmark_iter_free
iter_next = _lib.cmark_iter_next
iter_get_node = _lib.cmark_iter_get_node

render_html = _lib.cmark_render_html


def text_to_c(text):
    """Convert text to bytes suitable for passing into C functions."""
    return text.encode(_ENCODING)


def text_from_c(c_string):
    """Convert C string (e.g. returned from C function) to text."""
    return _ffi.string(c_string).decode(_ENCODING)
