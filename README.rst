paka.cmark
==========
.. image:: https://travis-ci.org/PavloKapyshin/paka.cmark.svg?branch=master
    :target: https://travis-ci.org/PavloKapyshin/paka.cmark

``paka.cmark`` is a Python library that wraps subset of cmark_ C library
(that is one of reference implementations of CommonMark).


Features
--------
- Python 2.7 and 3.5 are supported
- PyPy (Python 2.7) is supported, as wrapping is made with CFFI_
- currently only HTML output and limited number of ``cmark``’s options
  are supported (``CMARK_OPT_SAFE``, ``CMARK_OPT_NOBREAKS``,
  ``CMARK_OPT_HARDBREAKS``)


Examples
--------
.. code-block:: pycon

    >>> from paka import cmark

Render with ``CMARK_OPT_DEFAULT | CMARK_OPT_NOBREAKS`` (unlike ``cmark``,
``paka.cmark`` uses ``CMARK_OPT_NOBREAKS`` by default):

.. code-block:: pycon

    >>> print(cmark.to_html(u"Hello,\n*World*!"))
    <p>Hello, <em>World</em>!</p>

Render with ``CMARK_OPT_DEFAULT | CMARK_OPT_NOBREAKS | CMARK_OPT_SAFE``:

.. code-block:: pycon

    >>> print(cmark.to_html(u"<p>nope</p>", safe=True))
    <!-- raw HTML omitted -->

Render with ``CMARK_OPT_DEFAULT``:

.. code-block:: pycon

    >>> print(cmark.to_html(u"Hello,\n*World*!", breaks=True))
    <p>Hello,
    <em>World</em>!</p>

Render with ``CMARK_OPT_DEFAULT | CMARK_OPT_HARDBREAKS``:

.. code-block:: pycon

    >>> print(cmark.to_html(u"Hello,\n*World*!", breaks="hard"))
    <p>Hello,<br />
    <em>World</em>!</p>


Installation
------------
Library is `available on PyPI <https://pypi.python.org/pypi/paka.cmark>`_,
you can use ``pip`` for installation:

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


Checking code style
-------------------
Run code checkers:

.. code-block:: console

    $ tox -e checks


Getting documentation
---------------------
Build HTML docs:

.. code-block:: console

    $ tox -e docs

View built docs:

.. code-block:: console

    $ sensible-browser .tox/docs/tmp/docs_html/index.html


.. _cmark: https://github.com/jgm/cmark
.. _CFFI: https://pypi.python.org/pypi/cffi
