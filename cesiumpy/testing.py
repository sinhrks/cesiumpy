#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals


def _skip_if_no_numpy():
    try:
        import numpy                # noqa
    except ImportError:
        import nose
        raise nose.SkipTest("no numpy module")


def _skip_if_no_pandas():
    try:
        import pandas               # noqa
    except ImportError:
        import nose
        raise nose.SkipTest("no pandas module")


def _skip_if_no_scipy():
    try:
        import scipy.spatial         # noqa
    except ImportError:
        import nose
        raise nose.SkipTest("no scipy.spatial module")


def _skip_if_no_shapely():
    try:
        import shapely.geometry      # noqa
    except ImportError:
        import nose
        raise nose.SkipTest("no shapely.geometry module")


def _skip_if_no_matplotlib():
    try:
        import matplotlib
        matplotlib.use('Agg')
    except ImportError:
        import nose
        raise nose.SkipTest("no matplotlib.pyplot module")
