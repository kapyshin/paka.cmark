import sys

from paka.cmark._cmark import ffi, lib


_PY2 = sys.version_info.major == 2


def get_version():
    result = ffi.string(lib.cmark_version_string())
    if _PY2:  # pragma: no cover
        return result
    return result.decode("ascii")


def to_html(text):
    encoding = "utf-8"
    text_bytes = text.encode(encoding)
    opts = lib.CMARK_OPT_NOBREAKS
    return ffi.string(
        lib.cmark_markdown_to_html(
            text_bytes, len(text_bytes), opts)).decode(encoding)
