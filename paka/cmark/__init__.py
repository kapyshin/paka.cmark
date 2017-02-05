"""Lightweight `cmark`_ wrapper.

.. _cmark: https://github.com/jgm/cmark

"""

import sys

from paka.cmark._cmark import ffi, lib


_PY2 = sys.version_info.major == 2


class LineBreaks(object):  # pylint: disable=too-few-public-methods
    """How line breaks will be rendered."""

    soft = "soft"
    r"""As ``\n``\ s."""

    hard = "hard"
    r"""As ``<br />``\ s."""


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


def to_html(text, breaks=False, safe=False):
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

    Returns
    -------
    str
        HTML
    """
    encoding = "utf-8"
    text_bytes = text.encode(encoding)
    opts = lib.CMARK_OPT_DEFAULT
    if breaks:
        if breaks == "hard":
            opts |= lib.CMARK_OPT_HARDBREAKS
    else:
        opts |= lib.CMARK_OPT_NOBREAKS
    if safe:
        opts |= lib.CMARK_OPT_SAFE
    return ffi.string(
        lib.cmark_markdown_to_html(
            text_bytes, len(text_bytes), opts)).decode(encoding)
