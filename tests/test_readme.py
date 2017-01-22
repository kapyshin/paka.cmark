import os
import doctest
import unittest


# Most recent version is used anyway.
README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.rst")


def load_tests(loader, tests, pattern):
    suite = doctest.DocFileSuite(
        README_PATH, module_relative=False,
        optionflags=doctest.NORMALIZE_WHITESPACE)
    tests.addTests(suite)
    return tests
