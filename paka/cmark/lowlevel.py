"""Direct (low-level) bindings to C library.

Using these may be dangerous, as unlike with high-level ones,
you are responsible for error checking and correct memory management
(e.g. use of :py:func:`node_free` or :py:func:`iter_free` where needed).

Most members of this module are taken directly from C library,
but here their names do not have ``cmark_`` or ``CMARK_`` prefixes.

"""

import functools

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

BULLET_LIST = _lib.CMARK_BULLET_LIST
"""Bullet list."""
ORDERED_LIST = _lib.CMARK_ORDERED_LIST
"""Ordered list."""
NO_LIST = _lib.CMARK_NO_LIST
"""Node is not a list."""

PAREN_DELIM = _lib.CMARK_PAREN_DELIM
"""``)``"""
PERIOD_DELIM = _lib.CMARK_PERIOD_DELIM
"""``.``"""
NO_DELIM = _lib.CMARK_NO_DELIM
"""No list delimiter."""


def _nullable(func):
    """Convert returned cffi's NULL into None."""
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result != _ffi.NULL:
            return result
    return _wrapper


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
    _lib.cmark_node_free(node)


@_nullable
def node_next(node):
    """Return next node, if available.

    :returns: A node or None.

    """
    return _lib.cmark_node_next(node)


@_nullable
def node_previous(node):
    """Return previous node, if available.

    :returns: A node or None.

    """
    return _lib.cmark_node_previous(node)


@_nullable
def node_parent(node):
    """Return a parent of node, if available.

    :returns: A node or None.

    """
    return _lib.cmark_node_parent(node)


@_nullable
def node_first_child(node):
    """Return first child of node, if available.

    :returns: A node or None.

    """
    return _lib.cmark_node_first_child(node)


@_nullable
def node_last_child(node):
    """Return last child of node, if available.

    :returns: A node or None.

    """
    return _lib.cmark_node_last_child(node)


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


def node_unlink(node):
    """Unlink node from tree.

    .. warning::

        ``node`` is unlinked, but its memory still must be
        freed with :py:func:`node_free`.

    """
    _lib.cmark_node_unlink(node)


def node_insert_before(node, sibling):
    """Insert sibling before node.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_insert_before(node, sibling)


def node_insert_after(node, sibling):
    """Insert sibling after node.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_insert_after(node, sibling)


def node_prepend_child(node, child):
    """Prepend child to children of node.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_prepend_child(node, child)


def node_append_child(node, child):
    """Append child to children of node.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_append_child(node, child)


def consolidate_text_nodes(root):
    """Merge adjacent text nodes in the tree."""
    _lib.cmark_consolidate_text_nodes(root)


def node_get_type(node):
    """Return type of node.

    :returns: One of :ref:`node types <node_types>`.

    """
    return _lib.cmark_node_get_type(node)


def node_get_type_string(node):
    """Return type of node as string.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    """
    return _lib.cmark_node_get_type_string(node)


@_nullable
def node_get_fence_info(node):
    """Return fence info from fenced code block.

    For nodes having type other than :py:data:`NODE_CODE_BLOCK`
    returns None.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    """
    return _lib.cmark_node_get_fence_info(node)


def node_set_fence_info(node, info):
    """Set fence info of fenced code block.

    Parameters
    ----------
    node
        Node on which to operate.
    info: bytes
        Fence info.

        .. hint::

            Use :py:func:`text_to_c` to convert text into bytes.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_fence_info(node, info)


@_nullable
def node_get_literal(node):
    """Return string contents of node.

    Returns None for nodes having type other than
    :py:data:`NODE_HTML_BLOCK`, :py:data:`NODE_TEXT`,
    :py:data:`NODE_HTML_INLINE`, :py:data:`NODE_CODE`
    or :py:data:`NODE_CODE_BLOCK`.

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


def node_get_heading_level(node):
    """Return level of heading.

    Returns
    -------
    int
        ``[1, 6]`` for headings, ``0`` for non-heading nodes.

    """
    return _lib.cmark_node_get_heading_level(node)


def node_set_heading_level(node, level):
    """Set level of heading.

    Parameters
    ----------
    node
        Node on which to operate.
    level: int
        ``[1, 6]``

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_heading_level(node, level)


def node_get_list_type(node):
    """Return list type of node.

    :returns: One of :ref:`list types <list_types>`.

    """
    return _lib.cmark_node_get_list_type(node)


def node_set_list_type(node, list_type):
    """Set the list type of node.

    Parameters
    ----------
    node
        Node on which to operate.
    list_type
        One of :ref:`list types <list_types>`.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_list_type(node, list_type)


def node_get_list_delim(node):
    """Return type of list delimiter.

    :returns: One of :ref:`list delimiters <list_delimiters>`.

    """
    return _lib.cmark_node_get_list_delim(node)


def node_set_list_delim(node, list_delim):
    """Set the type of list delimiter for node.

    Parameters
    ----------
    node
        Node on which to operate.
    list_delim
        One of :ref:`list delimiters <list_delimiters>`.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_list_delim(node, list_delim)


def node_get_list_start(node):
    """Return starting number of list.

    Returns
    -------
    int
        Starting number of an ordered list or ``0``.

    """
    return _lib.cmark_node_get_list_start(node)


def node_set_list_start(node, start):
    """Set starting number of ordered list.

    Parameters
    ----------
    node
        Ordered list.
    start: int
        Starting number.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_list_start(node, start)


def node_get_list_tight(node):
    """Return 1 if node is a tight list.

    Returns
    -------
    int
        ``1`` if node is a tight list, ``0`` otherwise.

    """
    return _lib.cmark_node_get_list_tight(node)


def node_set_list_tight(node, tight):
    """Set tightness of list.

    Parameters
    ----------
    node
        List.
    tight: int
        ``1`` for tight, ``0`` for loose.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_list_tight(node, tight)


@_nullable
def node_get_url(node):
    """Return URL of image or link, or None.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    """
    return _lib.cmark_node_get_url(node)


def node_set_url(node, url):
    """Set URL of image or link.

    Parameters
    ----------
    node
        Image or link.
    url: bytes
        New URL.

        .. hint::

            Use :py:func:`text_to_c` to convert text into bytes.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_url(node, url)


@_nullable
def node_get_title(node):
    """Return title of image or link, or None.

    .. hint::

        Use :py:func:`text_from_c` to convert value returned
        by this function into text.

    """
    return _lib.cmark_node_get_title(node)


def node_set_title(node, title):
    """Set title of image or link.

    Parameters
    ----------
    node
        Image or link.
    title: bytes
        New title.

        .. hint::

            Use :py:func:`text_to_c` to convert text into bytes.

    Returns
    -------
    int
        ``1`` on success, ``0`` on failure.

    """
    return _lib.cmark_node_set_title(node, title)


def node_get_start_line(node):
    """Return line on which node begins.

    Returns
    -------
    int
        Line number (starts from ``1``).

    """
    return _lib.cmark_node_get_start_line(node)


def node_get_start_column(node):
    """Return column at which node begins.

    Returns
    -------
    int
        Column number (starts from ``1``).

    """
    return _lib.cmark_node_get_start_column(node)


def node_get_end_line(node):
    """Return line on which node ends.

    Returns
    -------
    int
        Line number (starts from ``1``).

    """
    return _lib.cmark_node_get_end_line(node)


def node_get_end_column(node):
    """Return column at which node ends.

    Returns
    -------
    int
        Column number (starts from ``1``).

    """
    return _lib.cmark_node_get_end_column(node)


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
    _lib.cmark_iter_free(iter_)


def iter_next(iter_):
    """Advance to next node and return event type.

    :returns: One of :ref:`iteration event types <iteration_event_types>`.

    """
    return _lib.cmark_iter_next(iter_)


def iter_get_node(iter_):
    """Return current node."""
    return _lib.cmark_iter_get_node(iter_)


def iter_get_event_type(iter_):
    """Return current event type.

    :returns: One of :ref:`iteration event types <iteration_event_types>`.

    """
    return _lib.cmark_iter_get_event_type(iter_)


def iter_get_root(iter_):
    """Return root node."""
    return _lib.cmark_iter_get_root(iter_)


def iter_reset(iter_, node, event):
    """Reset the iterator.

    Parameters
    ----------
    iter_
        "Iterator".
    node
        Node to make current.
    event
        :ref:`Event type <iteration_event_types>` to make current.

    """
    return _lib.cmark_iter_reset(iter_, node, event)


def parser_new(options):
    """Create parser object.

    .. warning::

        Returned parser object must be freed with :py:func:`parser_free`.

    Parameters
    ----------
    options
        See :ref:`options <options>`.

    """
    return _lib.cmark_parser_new(options)


def parser_free(parser):
    """Free memory allocated for parser object."""
    _lib.cmark_parser_free(parser)


def parser_feed(parser, buffer, length):
    """Feed string to parser object.

    Parameters
    ----------
    parser
        Parser object.
    buffer: bytes
        String to "feed" to parser.

        .. hint::

            Use :py:func:`text_to_c` to convert text into bytes.

    length: int
        Length of ``buffer``.

    """
    _lib.cmark_parser_feed(parser, buffer, length)


def parser_finish(parser):
    """Finish parsing and return tree of nodes.

    .. warning::

        Returned tree of nodes must be freed with :py:func:`node_free`.

    """
    return _lib.cmark_parser_finish(parser)


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
    if c_string is None:  # convenience for ones not willing to check :)
        return ""
    return _ffi.string(c_string).decode(ENCODING)
