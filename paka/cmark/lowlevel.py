"""Direct (low-level) bindings to C library.

Using these may be dangerous, as unlike with high-level ones,
you are responsible for error checking and correct memory management
(e.g. use of :py:func:`node_free` or :py:func:`iter_free` where needed).

Most members of this module are taken directly from C library,
but here their names do not have ``cmark_`` or ``CMARK_`` prefixes.

"""

from paka.cmark._cmark import ffi as _ffi, lib as _lib


ENCODING = "utf-8"
"""Encoding that is used for text manipulation."""

OPT_DEFAULT = _lib.CMARK_OPT_DEFAULT
"""Default options."""
OPT_HARDBREAKS = _lib.CMARK_OPT_HARDBREAKS
"""Render “soft break” nodes as hard line breaks."""
OPT_NOBREAKS = _lib.CMARK_OPT_NOBREAKS
"""Render “soft break” nodes as spaces."""
OPT_SOURCEPOS = _lib.CMARK_OPT_SOURCEPOS
"""Render with “sourcepos” information."""
OPT_SAFE = _lib.CMARK_OPT_SAFE
"""Suppress raw HTML and unsafe links while rendering."""

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
NODE_DOCUMENT = _lib.CMARK_NODE_DOCUMENT
"""Document."""
NODE_BLOCK_QUOTE = _lib.CMARK_NODE_BLOCK_QUOTE
"""Block quote."""
NODE_LIST = _lib.CMARK_NODE_LIST
"""List."""
NODE_ITEM = _lib.CMARK_NODE_ITEM
"""List item."""
NODE_CUSTOM_BLOCK = _lib.CMARK_NODE_CUSTOM_BLOCK
"""Block of custom."""
NODE_PARAGRAPH = _lib.CMARK_NODE_PARAGRAPH
"""Paragraph."""
NODE_HEADING = _lib.CMARK_NODE_HEADING
"""Heading."""
NODE_THEMATIC_BREAK = _lib.CMARK_NODE_THEMATIC_BREAK
"""Thematic break."""
NODE_FIRST_BLOCK = _lib.CMARK_NODE_FIRST_BLOCK
"""First block."""
NODE_LAST_BLOCK = _lib.CMARK_NODE_LAST_BLOCK
"""Last block."""
NODE_TEXT = _lib.CMARK_NODE_TEXT
"""Text."""
NODE_SOFTBREAK = _lib.CMARK_NODE_SOFTBREAK
"""Soft break."""
NODE_LINEBREAK = _lib.CMARK_NODE_LINEBREAK
"""Line break."""
NODE_CODE = _lib.CMARK_NODE_CODE
"""Inline code."""
NODE_HTML_INLINE = _lib.CMARK_NODE_HTML_INLINE
"""Inline HTML."""
NODE_CUSTOM_INLINE = _lib.CMARK_NODE_CUSTOM_INLINE
"""Inline custom."""
NODE_EMPH = _lib.CMARK_NODE_EMPH
"""Emphasis."""
NODE_STRONG = _lib.CMARK_NODE_STRONG
"""Strong emphasis."""
NODE_LINK = _lib.CMARK_NODE_LINK
"""Link."""
NODE_IMAGE = _lib.CMARK_NODE_IMAGE
"""Image."""
NODE_FIRST_INLINE = _lib.CMARK_NODE_FIRST_INLINE
"""First inline."""
NODE_LAST_INLINE = _lib.CMARK_NODE_LAST_INLINE
"""Last inline."""


def version_string():
    """Return C library version as string.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    """
    return _lib.cmark_version_string()


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


def markdown_to_html(buffer, length, options):
    """Render HTML from CommonMark.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

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
    return _lib.cmark_markdown_to_html(buffer, length, options)


def render_html(root, options):
    """Render tree of nodes as HTML.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    Parameters
    ----------
    root
        Root node.
    options
        See :ref:`options <options>`.

    """
    return _lib.cmark_render_html(root, options)


def render_xml(root, options):
    """Render tree of nodes as XML.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    Parameters
    ----------
    root
        Root node.
    options
        See :ref:`options <options>`.

    """
    return _lib.cmark_render_xml(root, options)


def render_man(root, options, width):
    """Render tree of nodes as groff.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    Parameters
    ----------
    root
        Root node.
    options
        See :ref:`options <options>`.
    width: int
        Maximum line width for line wrapping.

    """
    return _lib.cmark_render_man(root, options, width)


def render_commonmark(root, options, width):
    """Render tree of nodes as CommonMark.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    Parameters
    ----------
    root
        Root node.
    options
        See :ref:`options <options>`.
    width: int
        Maximum line width for line wrapping.

    """
    return _lib.cmark_render_commonmark(root, options, width)


def render_latex(root, options, width):
    """Render tree of nodes as LaTeX.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    Parameters
    ----------
    root
        Root node.
    options
        See :ref:`options <options>`.
    width: int
        Maximum line width for line wrapping.

    """
    return _lib.cmark_render_latex(root, options, width)


def text_to_c(text):
    """Convert text to bytes suitable for passing into C functions."""
    return text.encode(ENCODING)


def text_from_c(c_string):
    """Convert C string (e.g. returned from C function) to text."""
    return _ffi.string(c_string).decode(ENCODING)
