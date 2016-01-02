#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import collections
import itertools
import six


# --------------------------------------------------
# Validators
# --------------------------------------------------

def notimplemented(x):
    if x is not None:
        raise NotImplementedError
    return x


def validate_str(x, key):
    """ validate whether x is str or unicode """
    if not isinstance(x, six.string_types):
        raise ValueError('{key} must be str: {x}'.format(key=key, x=x))
    return x


def validate_str_or_none(x, key):
    """ validate whether x is str, unicode or None"""
    if x is None:
        return x
    return validate_str(x, key=key)


def validate_bool(x, key):
    """ validate whether x is bool """
    if not isinstance(x, bool):
        raise ValueError('{key} must be bool: {x}'.format(key=key, x=x))
    return x


def validate_bool_or_none(x, key):
    """ validate whether x is bool or None"""
    if x is None:
        return x
    return validate_bool(x, key=key)


def validate_numeric(x, key):
    """ validate whether x is int, long or float"""
    if not is_numeric(x):
        raise ValueError('{key} must be numeric: {x}'.format(key=key, x=x))
    return x


def validate_numeric_or_none(x, key):
    """ validate whether x is int, long, float or None"""
    if x is None:
        return x
    return validate_numeric(x, key=key)


def validate_longitude(x, key):
    """ validate whether x is numeric, and between -180 and 180 """
    if not is_longitude(x):
        raise ValueError('{key} must be longitude, between -180 to 180: {x}'.format(key=key, x=x))
    return x


def validate_latitude(x, key):
    """ validate whether x is numeric, and between -90 and 90 """
    if not is_latitude(x):
        raise ValueError('{key} must be latitude, between -90 to 90: {x}'.format(key=key, x=x))
    return x


def validate_listlike(x, key):
    """ validate whether x is list-likes """
    if not isinstance(x, listlike_types):
        raise ValueError('{key} must be list-likes: {x}'.format(key=key, x=x))
    return x


def validate_listlike_even(x, key):
    """ validate whether x is list-likes which length is even-number """
    x = validate_listlike(x, key)
    if len(x) % 2 != 0:
        raise ValueError('{key} length must be an even number: {x}'.format(key=key, x=x))
    return x

def validate_listlike_lonlat(x, key):
    """ validate whether x is list-likes consists from lon, lat pairs """
    x = validate_listlike_even(x, key)
    try:
        all(validate_longitude(e, key=key) for e in x[::2])
        all(validate_latitude(e, key=key) for e in x[1::2])
        # validation will raise ValueError immediately
    except ValueError:
        msg = '{key} must be a list consists from longitude and latitude: {x}'
        raise ValueError(msg.format(key=key, x=x))

    return x


# --------------------------------------------------
# Check Functions
# --------------------------------------------------

# There is not is_bool and is_str, because these are single expression

def is_numeric(x):
    return isinstance(x, (six.integer_types, float))


def is_longitude(x):
    if is_numeric(x):
        return -180 <= x <= 180
    return False


def is_latitude(x):
    if is_numeric(x):
        return -90 <= x <= 90
    return False

# may support np.array?
listlike_types = (list, tuple)


def is_listlike(x):
    """ whether the input can be regarded as list """
    return isinstance(x, listlike_types)


def is_listlike_2elem(x):
    if isinstance(x, listlike_types):
        if all(isinstance(e, listlike_types) and len(e) == 2 for e in x):
            return True
    return False


def is_listlike_3elem(x):
    if isinstance(x, list):
        if all(isinstance(e, listlike_types) and len(e) == 2 for e in x):
            return True
    return False


# --------------------------------------------------
# Converter Functions
# --------------------------------------------------

def to_jsscalar(x):
    """ convert x to JavaScript representation """

    from cesiumpy.base import _CesiumObject
    if isinstance(x, _CesiumObject):
        return x.script

    if isinstance(x, bool):
        # convert to JavaScript repr
        x = 'true' if x else 'false'
    elif isinstance(x, six.string_types):
        x = '"{0}"'.format(x)
    elif isinstance(x, dict):
        x = ''.join(to_jsobject(x))
    elif isinstance(x, list):
        x = [str(to_jsscalar(e)) for e in x]
        x = '[{0}]'.format(', '.join(x))
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


def _flatten_list_of_listlike(x):
    return list(itertools.chain(*x))


# --------------------------------------------------
# Shapely Functions
# --------------------------------------------------

try:
    import shapely.geometry

    ShapelyPoint = shapely.geometry.Point
    ShapelyMultiPoint = shapely.geometry.MultiPoint
    ShapelyLineString = shapely.geometry.LineString
    ShapelyMultiLineString = shapely.geometry.MultiLineString
    ShapelyLinearRing = shapely.geometry.LinearRing
    ShapelyPolygon = shapely.geometry.Polygon
    ShapelyMultiPolygon = shapely.geometry.MultiPolygon

except ImportError:
    class DummyClass(object):
        pass

    ShapelyPoint = DummyClass
    ShapelyMultiPoint = DummyClass
    ShapelyLineString = DummyClass
    ShapelyMultiLineString = DummyClass
    ShapelyLinearRing = DummyClass
    ShapelyPolygon = DummyClass
    ShapelyMultiPolygon = DummyClass


def _maybe_shapely_point(x):
    if isinstance(x, ShapelyMultiPoint):
        raise NotImplementedError
    elif isinstance(x, ShapelyPoint):
        return list(x.coords[:][0])
    return x


def _maybe_shapely_line(x):
    if isinstance(x, ShapelyMultiLineString):
        raise NotImplementedError
    elif isinstance(x, (ShapelyLineString, ShapelyLinearRing)):
        return list(itertools.chain(*x.coords[:]))
    return x


def _maybe_shapely_polygon(x):
    if isinstance(x, ShapelyMultiPolygon):
        # Extract polygons included in the MultiPolygon
        raise NotImplementedError
        polygons = [e for e in x]
    elif isinstance(x, ShapelyPolygon):
        polygons = [x]
    else:
        return x

    results = []
    for p in polygons:
        results.extend(list(itertools.chain(*p.exterior.coords)))
    return results
