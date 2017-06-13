import os

import setuptools


def _get_long_description():
    path = os.path.join(os.path.dirname(__file__), "README.rst")
    with open(path, "rb") as file:
        contents = file.read()
    return contents.decode("utf-8")


setuptools.setup(
    name="paka.cmark",
    description=(
        "Very lightweight CFFI-based Python bindings to cmark library"
        " (CommonMark implementation in C)."),
    long_description=_get_long_description(),
    version="1.29.0",
    packages=setuptools.find_packages(),
    setup_requires=["cffi>=1.0.0"],
    install_requires=["cffi>=1.0.0"],
    extras_require={"testing": []},
    cffi_modules=["paka/cmark/build_cmark.py:ffibuilder"],
    include_package_data=True,
    namespace_packages=["paka"],
    zip_safe=False,
    url="https://github.com/PavloKapyshin/paka.cmark",
    keywords="commonmark cmark c ffi",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"],
    license="BSD",
    author="Pavlo Kapyshin",
    author_email="i@93z.org")
