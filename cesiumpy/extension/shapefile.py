#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import itertools

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
