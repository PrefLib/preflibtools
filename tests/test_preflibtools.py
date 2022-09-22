#!/usr/bin/env python

"""Tests for `preflibtools` package."""

import pytest

from .instance import test_read, test_write, test_populate, test_order_handling
from .property import test_basic, distance_test, single_peakedness_test, single_crossing_test


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    test_read()
    test_write()
    test_populate()
    test_order_handling()
    test_basic()
    distance_test()
    single_peakedness_test()
    single_crossing_test()
