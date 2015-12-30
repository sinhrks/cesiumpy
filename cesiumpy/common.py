#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import collections
import itertools
import six


# --------------------------------------------------
# Validators
# --------------------------------------------------

def validate_str(x, key):
    if not isinstance(x, six.string_types):
        raise ValueError('{key} must be str: {x}'.format(key=key, x=x))
    return x


def validate_str_or_none(x, key):
    if x is None:
        return x
    return validate_str(x, key=key)


def validate_bool(x, key):
    if not isinstance(x, bool):
        raise ValueError('{key} must be bool: {x}'.format(key=key, x=x))
    return x


def validate_bool_or_none(x, key):
    if x is None:
        return x
    return validate_bool(x, key=key)


def validate_numeric(x, key):
    if not is_numeric(x):
        raise ValueError('{key} must be numeric: {x}'.format(key=key, x=x))
    return x


def validate_numeric_or_none(x, key):
    if x is None:
        return x
    return validate_numeric(x, key=key)


def validate_longtitude(x, key):
    if not is_longtitude(x):
        raise ValueError('{key} must be longtitude, between -180 to 180: {x}'.format(key=key, x=x))
    return x


def validate_latitude(x, key):
    if not is_latitude(x):
        raise ValueError('{key} must be latitude, between -90 to 90: {x}'.format(key=key, x=x))
    return x

# --------------------------------------------------
# Check Functions
# --------------------------------------------------


def is_numeric(x):
    return isinstance(x, (six.integer_types, float))


def is_longtitude(x):
    if is_numeric(x):
        return -180 <= x <= 180
    return False


def is_latitude(x):
    if is_numeric(x):
        return -90 <= x <= 90
    return False


def to_jsscalar(x):
    """ convert x to JavaScript representation """
    if isinstance(x, bool):
        # convert to JavaScript repr
        x = 'true' if x else 'false'
    elif isinstance(x, six.string_types):
        x = '"{0}"'.format(x)
    elif isinstance(x, dict):
        x = ''.join(to_jsobject(x))
    elif isinstance(x, list):
        x = [to_jsscalar(e) for e in x]
    return x

def to_jsobject(x):
    """ convert x to JavaScript Object """

    results = ['{']

    # filter None
    dic = collections.OrderedDict()
    # do not use dict comprehension to keep property order
    for k, v in six.iteritems(x):
        if v is not None:
            dic[k] = v
    x = dic
    if len(x) == 0:
        return ['']

    # count valid args
    last = len(x) - 1

    for key, val in six.iteritems(x):
        val = to_jsscalar(val)
        results.append('{0} : {1}, '.format(key, val))
    results[-1] = results[-1][:-2] # remove final comma
    results.append('}')
    return results


# --------------------------------------------------
# Check Functions
# --------------------------------------------------


def _maybe_shapely_point(x):
    try:
        import shapely.geometry
    except ImportError:
        return x

    if isinstance(x, shapely.geometry.MultiPoint):
        raise NotImplementedError
    elif isinstance(x, shapely.geometry.Point):
        return list(x.coords[:][0])
    return x


def _maybe_shapely_line(x):
    try:
        import shapely.geometry
    except ImportError:
        return x

    if isinstance(x, shapely.geometry.MultiLineString):
        raise NotImplementedError
    elif isinstance(x, (shapely.geometry.LineString, shapely.geometry.LinearRing)):
        return list(itertools.chain(*x.coords[:]))
    return x


def _maybe_shapely_polygon(x):
    try:
        import shapely.geometry
    except ImportError:
        return x

    if isinstance(x, shapely.geometry.multipolygon.MultiPolygon):
        # Extract polygons included in the MultiPolygon
        raise NotImplementedError
        polygons = [e for e in x]
    elif isinstance(x, shapely.geometry.polygon.Polygon):
        polygons = [x]
    else:
        return x

    results = []
    for p in polygons:
        results.extend(list(itertools.chain(*p.exterior.coords)))
    return results
