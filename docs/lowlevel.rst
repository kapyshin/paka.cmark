Low-level API
=============

.. currentmodule:: paka.cmark.lowlevel

.. automodule:: paka.cmark.lowlevel
  :no-members:
  :no-undoc-members:

.. autofunction:: parse_document
.. autofunction:: node_new
.. autofunction:: node_free
.. autofunction:: node_replace
.. autofunction:: node_get_type
.. autofunction:: node_get_fence_info
.. autofunction:: node_get_literal
.. autofunction:: node_set_literal

Iteration
---------
.. autofunction:: iter_new
.. autofunction:: iter_free
.. autofunction:: iter_next
.. autofunction:: iter_get_node

.. _iteration_event_types:

Iteration event types
---------------------
.. autodata:: EVENT_ENTER
.. autodata:: EVENT_EXIT
.. autodata:: EVENT_DONE

Rendering
---------
.. autofunction:: render_html

.. _options:

Options
-------
.. autodata:: OPT_DEFAULT

.. _node_types:

Node types
----------
.. autodata:: NODE_NONE
.. autodata:: NODE_CODE_BLOCK
.. autodata:: NODE_HTML_BLOCK

Python Helpers
--------------
.. autofunction:: text_to_c
.. autofunction:: text_from_c
