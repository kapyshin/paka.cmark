"""Lightweight `cmark`_ wrapper.

.. _cmark: https://github.com/commonmark/cmark

"""

from paka.cmark._cmark import ffi as _ffi
from paka.cmark import lowlevel as _lowlevel


# pylint: disable=useless-object-inheritance
class LineBreaks(object):  # pylint: disable=too-few-public-methods
    """How line breaks will be rendered."""

    soft = "soft"
    r"""As ``\n``\ s."""

    hard = "hard"
    r"""As ``<br />``\ s."""


def _add_breaks_to_opts(breaks, opts):
    if breaks:
        if breaks == "hard":
            opts |= _lowlevel.OPT_HARDBREAKS
    else:
        opts |= _lowlevel.OPT_NOBREAKS
    return opts


def _add_sourcepos_to_opts(sourcepos, opts):
    if sourcepos:
        opts |= _lowlevel.OPT_SOURCEPOS
    return opts


def _add_smart_to_opts(smart, opts):
    if smart:
        opts |= _lowlevel.OPT_SMART
    return opts


def get_version():
    """Return version of underlying C library.

    Returns
    -------
    str
        Version as X.Y.Z.

    """
    return _lowlevel.text_from_c(_lowlevel.version_string())


def to_html(text, breaks=False, safe=False, sourcepos=False, smart=False):
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
    smart: bool
        Use :py:data:`~paka.cmark.lowlevel.OPT_SMART`.

    Returns
    -------
    str
        HTML

    """
    opts = _add_sourcepos_to_opts(
        sourcepos, _add_breaks_to_opts(breaks, _lowlevel.OPT_DEFAULT))
    opts = _add_smart_to_opts(smart, opts)
    if safe:
        opts |= _lowlevel.OPT_SAFE
    text_bytes = _lowlevel.text_to_c(text)
    return _lowlevel.text_from_c(
        _lowlevel.markdown_to_html(text_bytes, len(text_bytes), opts))


def to_xml(text, sourcepos=False, smart=False):
    """Convert markup to XML.

    Parameters
    ----------
    text: str
        Text marked up with `CommonMark <http://commonmark.org>`_.
    sourcepos: bool
        If ``True``, add ``sourcepos`` attribute to all block elements
        (that is, use ``CMARK_OPT_SOURCEPOS``).
    smart: bool
        Use :py:data:`~paka.cmark.lowlevel.OPT_SMART`.

    Returns
    -------
    str
        XML

    """
    opts = _add_smart_to_opts(
        smart, _add_sourcepos_to_opts(sourcepos, _lowlevel.OPT_DEFAULT))
    text_bytes = _lowlevel.text_to_c(text)
    parsed = _lowlevel.parse_document(text_bytes, len(text_bytes), opts)
    root = _ffi.gc(parsed, _lowlevel.node_free)
    return _lowlevel.text_from_c(_lowlevel.render_xml(root, opts))


def to_commonmark(text, breaks=False, width=0, smart=False):
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
    smart: bool
        Use :py:data:`~paka.cmark.lowlevel.OPT_SMART`.

    Returns
    -------
    str
        CommonMark

    """
    opts = _add_smart_to_opts(
        smart, _add_breaks_to_opts(breaks, _lowlevel.OPT_DEFAULT))
    text_bytes = _lowlevel.text_to_c(text)
    parsed = _lowlevel.parse_document(text_bytes, len(text_bytes), opts)
    root = _ffi.gc(parsed, _lowlevel.node_free)
    return _lowlevel.text_from_c(
        _lowlevel.render_commonmark(root, opts, width))


def to_man(text, breaks=False, width=0, smart=False):
    r"""Convert markup to groff man page.

    Parameters
    ----------
    text: str
        Text marked up with `CommonMark <http://commonmark.org>`_.
    breaks: bool or LineBreaks
        How line breaks will be rendered. If ``True``,
        ``"soft"``, or :py:attr:`LineBreaks.soft` -- “soft break nodes”
        (single newlines) are rendered as newlines (``\n``). If ``False``
        -- “soft break nodes” are rendered as spaces. If ``"hard"`` or
        :py:attr:`LineBreaks.hard` -- “soft break nodes” are rendered
        as ``.PD 0\n.P\n.PD\n``.
    width: int
        Wrap width of output by inserting line breaks (default is
        ``0``—no wrapping). Has no effect if ``breaks`` are ``False``.
    smart: bool
        Use :py:data:`~paka.cmark.lowlevel.OPT_SMART`.

    Returns
    -------
    str
        Page without the header.

    """
    opts = _add_smart_to_opts(
        smart, _add_breaks_to_opts(breaks, _lowlevel.OPT_DEFAULT))
    text_bytes = _lowlevel.text_to_c(text)
    parsed = _lowlevel.parse_document(text_bytes, len(text_bytes), opts)
    root = _ffi.gc(parsed, _lowlevel.node_free)
    return _lowlevel.text_from_c(
        _lowlevel.render_man(root, opts, width))


def to_latex(text, breaks=False, width=0, smart=False):
    r"""Convert markup to LaTeX.

    Parameters
    ----------
    text: str
        Text marked up with `CommonMark <http://commonmark.org>`_.
    breaks: bool or LineBreaks
        How line breaks will be rendered. If ``True``,
        ``"soft"``, or :py:attr:`LineBreaks.soft` -- as newlines.
        If ``False`` -- “soft break nodes” (single newlines) are
        rendered as spaces. If ``"hard"`` or :py:attr:`LineBreaks.hard`
        -- “soft break nodes” are rendered as ``\\\n``.
    width: int
        Wrap width of output by inserting line breaks (default is
        ``0``—no wrapping). Has no effect if ``breaks`` are ``False``.
    smart: bool
        Use :py:data:`~paka.cmark.lowlevel.OPT_SMART`.

    Returns
    -------
    str
        LaTeX document.

    """
    opts = _add_smart_to_opts(
        smart, _add_breaks_to_opts(breaks, _lowlevel.OPT_DEFAULT))
    text_bytes = _lowlevel.text_to_c(text)
    parsed = _lowlevel.parse_document(text_bytes, len(text_bytes), opts)
    root = _ffi.gc(parsed, _lowlevel.node_free)
    return _lowlevel.text_from_c(
        _lowlevel.render_latex(root, opts, width))
