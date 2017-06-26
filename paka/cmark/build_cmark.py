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
#define CMARK_OPT_SOURCEPOS ...
#define CMARK_OPT_SMART ...


typedef struct cmark_node cmark_node;
typedef enum {
    /* Error status */
    CMARK_NODE_NONE,

    /* Block */
    CMARK_NODE_DOCUMENT,
    CMARK_NODE_BLOCK_QUOTE,
    CMARK_NODE_LIST,
    CMARK_NODE_ITEM,
    CMARK_NODE_CODE_BLOCK,
    CMARK_NODE_HTML_BLOCK,
    CMARK_NODE_CUSTOM_BLOCK,
    CMARK_NODE_PARAGRAPH,
    CMARK_NODE_HEADING,
    CMARK_NODE_THEMATIC_BREAK,

    CMARK_NODE_FIRST_BLOCK = CMARK_NODE_DOCUMENT,
    CMARK_NODE_LAST_BLOCK = CMARK_NODE_THEMATIC_BREAK,

    /* Inline */
    CMARK_NODE_TEXT,
    CMARK_NODE_SOFTBREAK,
    CMARK_NODE_LINEBREAK,
    CMARK_NODE_CODE,
    CMARK_NODE_HTML_INLINE,
    CMARK_NODE_CUSTOM_INLINE,
    CMARK_NODE_EMPH,
    CMARK_NODE_STRONG,
    CMARK_NODE_LINK,
    CMARK_NODE_IMAGE,

    CMARK_NODE_FIRST_INLINE = CMARK_NODE_TEXT,
    CMARK_NODE_LAST_INLINE = CMARK_NODE_IMAGE,
} cmark_node_type;

typedef enum {
    CMARK_NO_LIST,
    CMARK_BULLET_LIST,
    CMARK_ORDERED_LIST
} cmark_list_type;
typedef enum {
    CMARK_NO_DELIM,
    CMARK_PERIOD_DELIM,
    CMARK_PAREN_DELIM
} cmark_delim_type;

typedef struct cmark_iter cmark_iter;
typedef enum {
    CMARK_EVENT_NONE,
    CMARK_EVENT_DONE,
    CMARK_EVENT_ENTER,
    CMARK_EVENT_EXIT
} cmark_event_type;

typedef struct cmark_parser cmark_parser;


const char *cmark_version_string();

char *cmark_markdown_to_html(const char *text, size_t len, int options);

cmark_node *cmark_parse_document(const char *buffer, size_t len, int options);
cmark_node *cmark_node_new(cmark_node_type type);
void cmark_node_free(cmark_node *node);

cmark_node *cmark_node_next(cmark_node *node);
cmark_node *cmark_node_previous(cmark_node *node);
cmark_node *cmark_node_parent(cmark_node *node);
cmark_node *cmark_node_first_child(cmark_node *node);
cmark_node *cmark_node_last_child(cmark_node *node);

void cmark_node_unlink(cmark_node *node);
int cmark_node_insert_before(cmark_node *node, cmark_node *sibling);
int cmark_node_insert_after(cmark_node *node, cmark_node *sibling);
int cmark_node_replace(cmark_node *oldnode, cmark_node *newnode);
int cmark_node_prepend_child(cmark_node *node, cmark_node *child);
int cmark_node_append_child(cmark_node *node, cmark_node *child);
void cmark_consolidate_text_nodes(cmark_node *root);

cmark_node_type cmark_node_get_type(cmark_node *node);
const char *cmark_node_get_type_string(cmark_node *node);
const char *cmark_node_get_fence_info(cmark_node *node);
int cmark_node_set_fence_info(cmark_node *node, const char *info);
const char *cmark_node_get_literal(cmark_node *node);
int cmark_node_set_literal(cmark_node *node, const char *content);
int cmark_node_get_heading_level(cmark_node *node);
int cmark_node_set_heading_level(cmark_node *node, int level);
cmark_list_type cmark_node_get_list_type(cmark_node *node);
int cmark_node_set_list_type(cmark_node *node, cmark_list_type type);
cmark_delim_type cmark_node_get_list_delim(cmark_node *node);
int cmark_node_set_list_delim(cmark_node *node, cmark_delim_type delim);
int cmark_node_get_list_start(cmark_node *node);
int cmark_node_set_list_start(cmark_node *node, int start);
int cmark_node_get_list_tight(cmark_node *node);
int cmark_node_set_list_tight(cmark_node *node, int tight);
const char *cmark_node_get_url(cmark_node *node);
int cmark_node_set_url(cmark_node *node, const char *url);
const char *cmark_node_get_title(cmark_node *node);
int cmark_node_set_title(cmark_node *node, const char *title);
int cmark_node_get_start_line(cmark_node *node);
int cmark_node_get_start_column(cmark_node *node);
int cmark_node_get_end_line(cmark_node *node);
int cmark_node_get_end_column(cmark_node *node);

char *cmark_render_commonmark(cmark_node *root, int options, int width);
char *cmark_render_xml(cmark_node *root, int options);
char *cmark_render_html(cmark_node *root, int options);
char *cmark_render_man(cmark_node *root, int options, int width);
char *cmark_render_latex(cmark_node *root, int options, int width);

cmark_iter *cmark_iter_new(cmark_node *root);
void cmark_iter_free(cmark_iter *iter);
cmark_event_type cmark_iter_next(cmark_iter *iter);
cmark_node *cmark_iter_get_node(cmark_iter *iter);
cmark_event_type cmark_iter_get_event_type(cmark_iter *iter);
cmark_node *cmark_iter_get_root(cmark_iter *iter);
void cmark_iter_reset(
    cmark_iter *iter, cmark_node *current, cmark_event_type event_type);

cmark_parser *cmark_parser_new(int options);
void cmark_parser_free(cmark_parser *parser);
void cmark_parser_feed(cmark_parser *parser, const char *buffer, size_t len);
cmark_node * cmark_parser_finish(cmark_parser *parser);
""")


ffibuilder.set_source(
    "paka.cmark._cmark",
    CMARK_HEADER,
    sources=_get_sources(exclude=["main.c"]),
    include_dirs=_relativize_paths([CMARK_SRC_DIR_PATH]))


if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
