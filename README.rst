paka.cmark
==========
.. image:: https://travis-ci.org/PavloKapyshin/paka.cmark.svg?branch=master
    :target: https://travis-ci.org/PavloKapyshin/paka.cmark

``paka.cmark`` is a Python library that wraps subset of cmark_ C library.
Wrapping is made with CFFI_, so PyPy is supported in addition to CPython.
Currently only HTML output and limited number of ``cmark``’s options are
supported (``CMARK_OPT_SAFE`` and ``CMARK_OPT_NOBREAKS``).


Examples
--------
.. code-block:: pycon

    >>> from paka import cmark

Render with ``CMARK_OPT_DEFAULT | CMARK_OPT_NOBREAKS`` (unlike ``cmark``,
``paka.cmark`` uses ``CMARK_OPT_NOBREAKS`` by default):

.. code-block:: pycon

    >>> print(cmark.to_html("Hello,\n*World*!"))
    <p>Hello, <em>World</em>!</p>

Render with ``CMARK_OPT_DEFAULT | CMARK_OPT_NOBREAKS | CMARK_OPT_SAFE``:

.. code-block:: pycon

    >>> print(cmark.to_html("<p>nope</p>", safe=True))
    <!-- raw HTML omitted -->

Render with ``CMARK_OPT_DEFAULT``:

.. code-block:: pycon

    >>> print(cmark.to_html("Hello,\n*World*!", breaks=True))
    <p>Hello,
    <em>World</em>!</p>


Installation
------------
.. code-block:: console

    $ pip install paka.cmark


Running tests
-------------
.. code-block:: console

    $ tox


Getting coverage
----------------
Collect info:

.. code-block:: console

    $ tox -e coverage

View HTML report:

.. code-block:: console

    $ sensible-browser .tox/coverage/tmp/cov_html/index.html


.. _cmark: https://github.com/jgm/cmark
.. _CFFI: https://pypi.python.org/pypi/cffi
