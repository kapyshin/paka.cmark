"""Lightweight `cmark`_ wrapper.

.. _cmark: https://github.com/jgm/cmark

"""

import sys

from paka.cmark._cmark import ffi, lib


_PY2 = sys.version_info.major == 2
_ENCODING = "utf-8"


class LineBreaks(object):  # pylint: disable=too-few-public-methods
    """How line breaks will be rendered."""

    soft = "soft"
    r"""As ``\n``\ s."""

    hard = "hard"
    r"""As ``<br />``\ s."""


def _add_breaks_to_opts(breaks, opts):
    if breaks:
        if breaks == "hard":
            opts |= lib.CMARK_OPT_HARDBREAKS
    else:
        opts |= lib.CMARK_OPT_NOBREAKS
    return opts


def _add_sourcepos_to_opts(sourcepos, opts):
    if sourcepos:
        opts |= lib.CMARK_OPT_SOURCEPOS
    return opts


def get_version():
    """Return version of underlying C library.

    Returns
    -------
    str
        Version as X.Y.Z.

    """
    result = ffi.string(lib.cmark_version_string())
    if _PY2:  # pragma: no cover
        return result
    return result.decode("ascii")


def to_html(text, breaks=False, safe=False, sourcepos=False):
    r"""Convert markup to HTML.

    Parameters
    ----------
    text: str
        Text marked up with `CommonMark <http://commonmark.org>`_.
    breaks: bool or LineBreaks
        How line breaks in text will be rendered. If ``True``,
        ``"soft"``, or :py:attr:`LineBreaks.soft` -- as newlines
        (``\n``). If ``False`` -- as spaces. If ``"hard"`` or
        :py:attr:`LineBreaks.hard` -- as ``<br />``\ s.
    safe: bool
        If ``True``, replace raw HTML (that was present in ``text``)
        with HTML comment.
    sourcepos: bool
        If ``True``, add ``data-sourcepos`` attribute to block elements
        (that is, use ``CMARK_OPT_SOURCEPOS``).

    Returns
    -------
    str
        HTML

    """
    text_bytes = text.encode(_ENCODING)
    opts = _add_sourcepos_to_opts(
        sourcepos, _add_breaks_to_opts(breaks, lib.CMARK_OPT_DEFAULT))
    if safe:
        opts |= lib.CMARK_OPT_SAFE
    return ffi.string(
        lib.cmark_markdown_to_html(
            text_bytes, len(text_bytes), opts)).decode(_ENCODING)


def to_xml(text, sourcepos=False):
    """Convert markup to XML.

    Parameters
    ----------
    text: str
        Text marked up with `CommonMark <http://commonmark.org>`_.
    sourcepos: bool
        If ``True``, add ``sourcepos`` attribute to all block elements
        (that is, use ``CMARK_OPT_SOURCEPOS``).

    Returns
    -------
    str
        XML

    """
    opts = _add_sourcepos_to_opts(sourcepos, lib.CMARK_OPT_DEFAULT)
    text_bytes = text.encode(_ENCODING)
    parsed = lib.cmark_parse_document(text_bytes, len(text_bytes), opts)
    root = ffi.gc(parsed, lib.cmark_node_free)
    rendered = lib.cmark_render_xml(root, opts)
    return ffi.string(rendered).decode(_ENCODING)


def to_commonmark(text, breaks=False, width=0):
    r"""Convert markup to CommonMark.

    Parameters
    ----------
    text: str
        Text marked up with `CommonMark <http://commonmark.org>`_.
    breaks: bool or LineBreaks
        How line breaks will be rendered. If ``True``,
        ``"soft"``, or :py:attr:`LineBreaks.soft` -- as newlines
        (``\n``). If ``False`` -- as spaces. If ``"hard"`` or
        :py:attr:`LineBreaks.hard` -- “soft break nodes” (single
        newlines) are rendered as two spaces and ``\n``.
    width: int
        Wrap width of output by inserting line breaks (default is
        ``0``—no wrapping). Has no effect if ``breaks`` are set to be
        ``"hard"`` (e.g. with :py:attr:`LineBreaks.hard`).

    Returns
    -------
    str
        CommonMark

    """
    opts = _add_breaks_to_opts(breaks, lib.CMARK_OPT_DEFAULT)
    text_bytes = text.encode(_ENCODING)
    parsed = lib.cmark_parse_document(text_bytes, len(text_bytes), opts)
    root = ffi.gc(parsed, lib.cmark_node_free)
    rendered = lib.cmark_render_commonmark(root, opts, width)
    return ffi.string(rendered).decode(_ENCODING)
