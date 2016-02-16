#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import itertools

import cesiumpy

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


# --------------------------------------------------
# Convert shaply instances to Entity
# --------------------------------------------------

def to_entity(shape):
    """
    Convert shapely.geometry to corresponding entities.
    Result may be a list if geometry is consists from multiple instances.
    """
    if isinstance(shape, ShapelyMultiPoint):
        return [cesiumpy.Point(position=e) for e in shape]

    elif isinstance(shape, ShapelyPoint):
        return cesiumpy.Point(position=shape)

    elif isinstance(shape, ShapelyMultiLineString):
        return [cesiumpy.Polyline(positions=e) for e in shape]

    elif isinstance(shape, (ShapelyLineString, ShapelyLinearRing)):
        return cesiumpy.Polyline(positions=shape)

    elif isinstance(shape, ShapelyMultiPolygon):
        return [cesiumpy.Polygon(hierarchy=e) for e in shape]

    elif isinstance(shape, ShapelyPolygon):
        return cesiumpy.Polygon(hierarchy=shape)

    msg = 'Unable to convert to cesiumpy entity: {shape}'.format(shape=shape)
    raise ValueError(msg)


# --------------------------------------------------
# Convert shaply instances to Cartesian (Coordinates)
# --------------------------------------------------


def _maybe_shapely_point(x):
    if isinstance(x, ShapelyMultiPoint):
        raise NotImplementedError(x)
    elif isinstance(x, ShapelyPoint):
        return list(x.coords[:][0])
    return x


def _maybe_shapely_line(x):
    if isinstance(x, ShapelyMultiLineString):
        raise NotImplementedError(x)
    elif isinstance(x, (ShapelyLineString, ShapelyLinearRing)):
        return list(itertools.chain(*x.coords[:]))
    return x


def _maybe_shapely_polygon(x):
    if isinstance(x, ShapelyMultiPolygon):
        raise NotImplementedError(x)
    elif isinstance(x, ShapelyPolygon):
        polygons = [x]
    else:
        return x

    results = []
    for p in polygons:
        results.extend(list(itertools.chain(*p.exterior.coords)))
    return results
