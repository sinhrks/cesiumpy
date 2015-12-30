#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six
import cesiumpy.common as com


class CesiumCartesian(object):

    def __init__(self):
        raise NotImplementedError


def _maybe_cartesian(x):
    """ Convert list or tuple to corresponding Cartesian """
    if isinstance(x, CesiumCartesian):
        return x

    x = com._maybe_shapely_point(x)

    if isinstance(x, (tuple, list)):
        if len(x) == 2:
            return Cartesian2(*x)
        elif len(x) == 3:
            return Cartesian3(*x)
        elif len(x) == 4:
            return Cartesian4(*x)
        else:
            msg = 'length must be 2-4 to be converted to Cartesian: {0}'
            raise ValueError(msg.format(x))
    else:
        raise ValueError('unable to convert input to Cartesian: {0}'.format(x))


def _maybe_cartesian_degrees(x):
    """ Convert list or tuple to corresponding Cartesian as degrees """
    if isinstance(x, CesiumCartesian):
        return x

    x = com._maybe_shapely_point(x)

    if isinstance(x, (tuple, list)):
        if len(x) == 2:
            return Cartesian2(*x, degrees=True)
        elif len(x) == 3:
            return Cartesian3(*x, degrees=True)
        elif len(x) == 4:
            return Cartesian4(*x, degrees=True)
        else:
            msg = 'length must be 2-4 to be converted to Cartesian: {0}'
            raise ValueError(msg.format(x))
    else:
        raise ValueError('unable to convert input to Cartesian: {0}'.format(x))


def _maybe_cartesian2_list(x):
    """
    Convert list or tuple to list of Cartesian2 instances. Used by PolylineVolume"""
    if isinstance(x, tuple):
        x = list(x)

    if isinstance(x, list):
        if all(isinstance(e, Cartesian2) for e in x):
            return x

        if len(x) % 2 == 0:
            x = [Cartesian2(i, j) for (i, j) in zip(x[::2], x[1::2])]
        else:
            msg = 'length must be even number to be converted to Cartesian: {0}'
            raise ValueError(msg.format(x))
        return x
    else:
        raise ValueError('unable to convert input to list of Cartesian2: {0}'.format(x))



class Cartesian2(CesiumCartesian):

    def __init__(self, x, y, degrees=False):

        self.x = com.validate_numeric(x, key='x')
        self.y = com.validate_numeric(y, key='y')

        self._is_degrees = com.validate_bool(degrees, key='degrees')

        if degrees:
            com.validate_longtitude(x, key='x')
            com.validate_latitude(y, key='y')

    @classmethod
    def fromDegrees(cls, x, y):
        return Cartesian2(x, y, degrees=True)

    def __len__(self):
        return len(self.x)

    def __repr__(self):
        if self._is_degrees:
            rep = """Cesium.Cartesian2.fromDegrees({x}, {y})"""
            return rep.format(x=self.x, y=self.y)
        else:
            rep = """new Cesium.Cartesian2({x}, {y})"""
            return rep.format(x=self.x, y=self.y)


class Cartesian3(CesiumCartesian):

    def __init__(self, x, y, z, degrees=False):
        self.x = com.validate_numeric(x, key='x')
        self.y = com.validate_numeric(y, key='y')
        self.z = com.validate_numeric(z, key='z')

        self._is_degrees = com.validate_bool(degrees, key='degrees')
        self._is_array = False

        if degrees:
            com.validate_longtitude(x, key='x')
            com.validate_latitude(y, key='y')

    @classmethod
    def fromDegrees(cls, x, y, z):
        return Cartesian3(x, y, z, degrees=True)

    @classmethod
    def fromDegreesArray(cls, x):

        # convert shaply.Polygon to coordinateslist
        x = com._maybe_shapely_polygon(x)
        x = com._maybe_shapely_line(x)

        if not isinstance(x, list):
            msg = 'input must be a list: {0}'
            raise ValueError(msg.format(type(x)))

        if len(x) % 2 != 0:
            msg = 'input length must be even number: {0}'
            raise ValueError(msg.format(x))

        try:
            all(com.validate_longtitude(e, key='input') for e in x[::2])
            all(com.validate_latitude(e, key='input') for e in x[1::2])
            # validation will raise ValueError immediately
        except ValueError:
            raise ValueError('input must be a list consists from longtitude and latitude')

        c = Cartesian3(0, 0, 0)
        c.x = x
        c._is_array = True
        return c

    def __len__(self):
        # it will raise TypeError if myself is not array
        return len(self.x)

    def __repr__(self):
        if self._is_array:
            rep = """Cesium.Cartesian3.fromDegreesArray({x})"""
            return rep.format(x=self.x)
        elif self._is_degrees:
            rep = """Cesium.Cartesian3.fromDegrees({x}, {y}, {z})"""
            return rep.format(x=self.x, y=self.y, z=self.z)
        else:
            rep = """new Cesium.Cartesian3({x}, {y}, {z})"""
            return rep.format(x=self.x, y=self.y, z=self.z)


class Cartesian4(CesiumCartesian):

    def __init__(self, x, y, z, w, degrees=False):

        self.x = com.validate_numeric(x, key='x')
        self.y = com.validate_numeric(y, key='y')
        self.z = com.validate_numeric(z, key='z')
        self.w = com.validate_numeric(w, key='w')

        self._is_degrees = com.validate_bool(degrees, key='degrees')

        if degrees:
            com.validate_longtitude(x, key='x')
            com.validate_latitude(y, key='y')

    @classmethod
    def fromDegrees(cls, x, y, z, w):
        return Cartesian4(x, y, z, w, degrees=True)

    def __repr__(self):
        if self._is_degrees:
            rep = """Cesium.Cartesian4.fromDegrees({x}, {y}, {z}, {w})"""
            return rep.format(x=self.x, y=self.y, z=self.z, w=self.w)
        else:
            rep = """new Cesium.Cartesian4({x}, {y}, {z}, {w})"""
            return rep.format(x=self.x, y=self.y, z=self.z, w=self.w)


def _maybe_rectangle(x):
    if isinstance(x, Rectangle):
        return x
    elif isinstance(x, (tuple, list)):
        if len(x) == 4:
            return Rectangle(*x)
        else:
            raise ValueError('length must be 4: {0}'.format(x))
    else:
        raise ValueError('unable to convert input to Rectangle: {0}'.format(x))


class Rectangle(CesiumCartesian):

    def __init__(self, west, south, east, north):

        self.west = com.validate_longtitude(west, key='west')
        self.south = com.validate_latitude(south, key='south')
        self.east = com.validate_longtitude(east, key='east')
        self.north = com.validate_latitude(north, key='north')

    def __repr__(self):
        rep = """Cesium.Rectangle.fromDegrees({west}, {south}, {east}, {north})"""
        return rep.format(west=self.west, south=self.south, east=self.east, north=self.north)

