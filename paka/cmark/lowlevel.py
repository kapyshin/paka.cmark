"""Direct (low-level) bindings to C library.

Using these may be dangerous, as unlike with high-level ones,
you are responsible for error checking and correct memory management
(e.g. use of :py:func:`node_free` or :py:func:`iter_free` where needed).

Most members of this module are taken directly from C library,
but here their names do not have ``cmark_`` or ``CMARK_`` prefixes.

"""

from paka.cmark._cmark import ffi as _ffi, lib as _lib


_ENCODING = "utf-8"

OPT_DEFAULT = _lib.CMARK_OPT_DEFAULT
"""Default options."""

EVENT_ENTER = _lib.CMARK_EVENT_ENTER
"""Entering node."""
EVENT_EXIT = _lib.CMARK_EVENT_EXIT
"""Exiting node."""
EVENT_DONE = _lib.CMARK_EVENT_DONE
"""Done iteration."""

NODE_NONE = _lib.CMARK_NODE_NONE
"""Error status."""
NODE_CODE_BLOCK = _lib.CMARK_NODE_CODE_BLOCK
"""Block of code."""
NODE_HTML_BLOCK = _lib.CMARK_NODE_HTML_BLOCK
"""Raw HTML block."""


def parse_document(buffer, length, options):
    """Parse CommonMark document into tree of nodes.

    .. warning::

        Returned tree of nodes must be freed with :py:func:`node_free`.

    Parameters
    ----------
    buffer: bytes
        CommonMark document.

        .. hint::

            Use :py:func:`text_to_c` to convert text into bytes.

    length: int
        Length of ``buffer``.
    options
        See :ref:`options <options>`.

    """
    return _lib.cmark_parse_document(buffer, length, options)


def node_new(node_type):
    """Create node of particular type.

    .. warning::

        Returned node must be freed with :py:func:`node_free`.

    Parameters
    ----------
    node_type
        One of :ref:`node types <node_types>`.

    """
    return _lib.cmark_node_new(node_type)


def node_free(node):
    """Free memory for node and its children (if any)."""
    return _lib.cmark_node_free(node)


def node_replace(old_node, new_node):
    """Replace old node with new one.

    .. warning::

        ``old_node`` is unlinked, but its memory still must be
        freed with :py:func:`node_free`.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_replace(old_node, new_node)


def node_get_type(node):
    """Return type of node.

    :returns: One of :ref:`node types <node_types>`.

    """
    return _lib.cmark_node_get_type(node)


def node_get_fence_info(node):
    """Return info string from fenced code block.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    """
    return _lib.cmark_node_get_fence_info(node)


def node_get_literal(node):
    """Return string contents of node.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    """
    return _lib.cmark_node_get_literal(node)


def node_set_literal(node, contents):
    """Set string contents of node.

    Parameters
    ----------
    node
        Node on which to operate.
    contents: bytes
        New contents of node.

        .. hint::

            Use :py:func:`text_to_c` to convert text into bytes.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_literal(node, contents)


def iter_new(root):
    """Create new "iterator" starting at root node.

    .. warning::

        Returned "iterator" must be freed with :py:func:`iter_free`
        when it is no longer needed.

    Parameters
    ----------
    root
        Root node.

    """
    return _lib.cmark_iter_new(root)


def iter_free(iter_):
    """Free memory of "iterator"."""
    return _lib.cmark_iter_free(iter_)


def iter_next(iter_):
    """Advance to next node and return event type.

    :returns: One of :ref:`iteration event types <iteration_event_types>`.

    """
    return _lib.cmark_iter_next(iter_)


def iter_get_node(iter_):
    """Return current node."""
    return _lib.cmark_iter_get_node(iter_)


def render_html(root, options):
    """Render tree of nodes as HTML.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    """
    return _lib.cmark_render_html(root, options)


def text_to_c(text):
    """Convert text to bytes suitable for passing into C functions."""
    return text.encode(_ENCODING)


def text_from_c(c_string):
    """Convert C string (e.g. returned from C function) to text."""
    return _ffi.string(c_string).decode(_ENCODING)
