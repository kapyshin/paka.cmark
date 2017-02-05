"""CFFI-based bindings to cmark."""

import os
import glob
import functools

from cffi import FFI


# Absolute path of paka/cmark dir.
CURRENT_PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute path of dir containing paka dir.
ROOT_DIR = os.path.normpath(os.path.join(CURRENT_PACKAGE_DIR, "../../"))

# Name of cmark "C sources" dir (with C sources, headers, etc.).
CMARK_SRC_DIR_NAME = "cmark_src"

# Absolute path of cmark "C sources" dir.
CMARK_SRC_DIR_PATH = os.path.join(CURRENT_PACKAGE_DIR, CMARK_SRC_DIR_NAME)

# Contents of cmark.h.
with open(os.path.join(CMARK_SRC_DIR_PATH, "cmark.h"), "rb") as file:
    CMARK_HEADER = file.read().decode("utf-8")
CMARK_HEADER = CMARK_HEADER.encode("ascii", "replace").decode("ascii")


_relativize = functools.partial(  # pylint: disable=invalid-name
    os.path.relpath, start=ROOT_DIR)


def _relativize_paths(paths):
    return list(map(_relativize, paths))


def _get_sources(exclude):
    exclude = set(exclude)
    glob_escape = getattr(glob, "escape", lambda s: s)

    def _get_sources_paths():
        for path in glob.iglob(
                os.path.join(glob_escape(CMARK_SRC_DIR_PATH), "*.c")):
            filename = os.path.basename(path)
            if filename not in exclude:
                yield path
    return _relativize_paths(sorted(_get_sources_paths()))


ffibuilder = FFI()  # pylint: disable=invalid-name
ffibuilder.cdef("""
#define CMARK_OPT_DEFAULT ...
#define CMARK_OPT_NOBREAKS ...
#define CMARK_OPT_HARDBREAKS ...
#define CMARK_OPT_SAFE ...

const char *cmark_version_string();

char *cmark_markdown_to_html(const char *text, size_t len, int options);
""")
ffibuilder.set_source(
    "paka.cmark._cmark",
    CMARK_HEADER,
    sources=_get_sources(exclude=["main.c"]),
    include_dirs=_relativize_paths([CMARK_SRC_DIR_PATH]))


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
