import pytest

from PROJECT import __author__ as author
from PROJECT import __version__ as version
from PROJECT.cxx import __version__ as cxxversion


def test_version():
    assert version == "0.1.0"


def test_author():
    assert author == "AUTHOR"


def test_cxxversion():
    assert cxxversion == "0.1.0"
