import doctest
import unittest


def load_tests(loader, tests, pattern):
    suite = doctest.DocFileSuite(
        "../README.rst", optionflags=doctest.NORMALIZE_WHITESPACE)
    tests.addTests(suite)
    return tests
