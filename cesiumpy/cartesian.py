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
    elif isinstance(x, (tuple, list)):
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
    elif isinstance(x, (tuple, list)):
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

        if not com.is_numeric(x):
            raise ValueError('x must be numeric: {0}'.format(x))
        if degrees and not com.is_longtitude(x):
            raise ValueError('x must be between -180 to 180: {0}'.format(x))

        if not com.is_numeric(y):
            raise ValueError('y must be numeric: {0}'.format(y))
        if degrees and not com.is_latitude(y):
            raise ValueError('y must be between -90 to 90: {0}'.format(y))

        self.x = x
        self.y = y

        self._is_degrees = degrees

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
        if not com.is_numeric(x):
            raise ValueError('x must be numeric: {0}'.format(x))
        if degrees and not com.is_longtitude(x):
            raise ValueError('x must be between -180 to 180: {0}'.format(x))

        if not com.is_numeric(y):
            raise ValueError('y must be numeric: {0}'.format(y))
        if degrees and not com.is_latitude(y):
            raise ValueError('y must be between -90 to 90: {0}'.format(y))

        if not com.is_numeric(z):
            raise ValueError('z must be numeric: {0}'.format(z))

        self.x = x
        self.y = y
        self.z = z

        self._is_degrees = degrees
        self._is_array = False

    @classmethod
    def fromDegrees(cls, x, y, z):
        return Cartesian3(x, y, z, degrees=True)

    @classmethod
    def fromDegreesArray(cls, x):

        # convert shaply.Polygon to coordinateslist
        x = com._maybe_shapely_polygon(x)

        if not isinstance(x, list):
            msg = 'input must be a list: {0}'
            raise ValueError(msg.format(type(x)))

        if len(x) % 2 != 0:
            msg = 'input length must be even number: {0}'
            raise ValueError(msg.format(x))

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
        if not com.is_numeric(x):
            raise ValueError('x must be numeric: {0}'.format(x))
        if degrees and not com.is_longtitude(x):
            raise ValueError('x must be between -180 to 180: {0}'.format(x))

        if not com.is_numeric(y):
            raise ValueError('y must be numeric: {0}'.format(y))
        if degrees and not com.is_latitude(y):
            raise ValueError('y must be between -90 to 90: {0}'.format(y))

        if not com.is_numeric(z):
            raise ValueError('z must be numeric: {0}'.format(z))

        if not com.is_numeric(w):
            raise ValueError('w must be numeric: {0}'.format(w))

        self.x = x
        self.y = y
        self.z = z
        self.w = w

        self._is_degrees = degrees

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


class Rectangle(CesiumCartesian):

    def __init__(self, west, south, east, north):

        if not com.is_numeric(west):
            raise ValueError('west must be numeric: {0}'.format(west))
        if not com.is_numeric(south):
            raise ValueError('south must be numeric: {0}'.format(south))
        if not com.is_numeric(east):
            raise ValueError('east must be numeric: {0}'.format(east))
        if not com.is_numeric(north):
            raise ValueError('north must be numeric: {0}'.format(north))

        self.west = west
        self.south = south
        self.east = east
        self.north = north

    @classmethod
    def from_python(cls, x):
        if isinstance(x, Rectangle):
            return x
        elif isinstance(x, (tuple, list)):
            if len(x) == 4:
                return Rectangle(*x)
            else:
                raise ValueError('length must be 4: {0}'.format(x))
        else:
            raise ValueError('unable to convert input to Rectangle: {0}'.format(x))

    def __repr__(self):
        rep = """Cesium.Rectangle.fromDegrees({west}, {south}, {east}, {north})"""
        return rep.format(west=self.west, south=self.south, east=self.east, north=self.north)

