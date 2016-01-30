#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six
import traitlets

from cesiumpy.base import _CesiumObject
import cesiumpy.common as com
import cesiumpy.extension.geocode as geocode
import cesiumpy.extension.shapefile as shapefile


class _Cartesian(_CesiumObject):

    _is_degrees = traitlets.Bool()
    _is_array = traitlets.Bool()

    def __init__(self):
        raise NotImplementedError

    @property
    def script(self):
        if self._is_array or self._is_degrees:
            rep = """Cesium.{self}"""
            return rep.format(self=self)
        else:
            rep = """new Cesium.{self}"""
            return rep.format(self=self)



def _maybe_cartesian2(x, key, degrees=False):
    """ Convert list or tuple to Cartesian2 """
    if isinstance(x, Cartesian2):
        return x

    x = shapefile._maybe_shapely_point(x)
    x = com.validate_listlike(x, key=key)

    if len(x) == 2:
        return Cartesian2(*x, degrees=degrees)
    else:
        msg = '{key} length must be 2 to be converted to Cartesian2: {x}'
        raise ValueError(msg.format(key=key, x=x))


def _maybe_cartesian3(x, key, degrees=False):
    """ Convert list or tuple to Cartesian3 """
    if isinstance(x, Cartesian3):
        return x

    x = shapefile._maybe_shapely_point(x)

    # currently, only Cartesian3 tries to geocode passed loc
    x = geocode._maybe_geocode(x, height=0)

    x = com.validate_listlike(x, key=key)

    if len(x) == 3:
        return Cartesian3(*x, degrees=degrees)
    elif len(x) == 2 and degrees:
        # if degrees is True, z can filled by 0
        # otherwise raise (non-degrees Cartesian is used in Box)
        return Cartesian3(x=x[0], y=x[1], z=0, degrees=degrees)
    else:
        msg = '{key} length must be 3 to be converted to Cartesian3: {x}'
        raise ValueError(msg.format(key=key, x=x))


def _maybe_cartesian4(x, key, degrees=False):
    """ Convert list or tuple to Cartesian4 """
    if isinstance(x, Cartesian4):
        return x

    x = shapefile._maybe_shapely_point(x)
    x = com.validate_listlike(x, key=key)

    if len(x) == 4:
        return Cartesian4(*x, degrees=degrees)
    else:
        msg = '{key} length must be 4 to be converted to Cartesian4: {x}'
        raise ValueError(msg.format(key=key, x=x))


def _maybe_cartesian2_list(x, key):
    """
    Convert list or tuple to list of Cartesian2 instances. Used by PolylineVolume
    """
    if com.is_listlike(x):
        if all(isinstance(e, Cartesian2) for e in x):
            return x
        elif all(isinstance(e, _Cartesian) for e in x):
            # for better error message
            msg = '{key} must be a listlike of Cartesian2: {x}'
            raise ValueError(msg.format(key=key, x=x))

        if com.is_listlike_2elem(x):
            x = com._flatten_list_of_listlike(x)

    x = com.validate_listlike_even(x, key=key)
    x = [Cartesian2(i, j) for (i, j) in zip(x[::2], x[1::2])]
    return x


class Cartesian2(_Cartesian):

    def __init__(self, x, y, degrees=False):

        self.x = com.validate_numeric(x, key='x')
        self.y = com.validate_numeric(y, key='y')

        self._is_degrees = degrees
        self._is_array = False

        if degrees:
            com.validate_longitude(x, key='x')
            com.validate_latitude(y, key='y')

    @classmethod
    def fromDegrees(cls, x, y):
        return Cartesian2(x, y, degrees=True)

    def __len__(self):
        return len(self.x)

    def __repr__(self):
        if self._is_degrees:
            rep = """Cartesian2.fromDegrees({x}, {y})"""
            return rep.format(x=self.x, y=self.y)
        else:
            rep = """Cartesian2({x}, {y})"""
            return rep.format(x=self.x, y=self.y)


class Cartesian3(_Cartesian):

    def __init__(self, x, y, z, degrees=False):
        self.x = com.validate_numeric(x, key='x')
        self.y = com.validate_numeric(y, key='y')
        self.z = com.validate_numeric(z, key='z')

        self._is_degrees = degrees
        self._is_array = False

        if degrees:
            com.validate_longitude(x, key='x')
            com.validate_latitude(y, key='y')

    @classmethod
    def fromDegrees(cls, x, y, z):
        return Cartesian3(x, y, z, degrees=True)

    @classmethod
    def fromDegreesArray(cls, x):

        if isinstance(x, Cartesian3) and x._is_array:
            x = x.x

        # convert shaply.Polygon to coordinateslist
        x = shapefile._maybe_shapely_polygon(x)
        x = shapefile._maybe_shapely_line(x)
        x = geocode._maybe_geocode(x, height=0)

        if com.is_listlike_2elem(x):
            x = com._flatten_list_of_listlike(x)
        elif com.is_listlike_3elem(x):
            raise NotImplementedError

        x = com.validate_listlike_lonlat(x, 'x')
        c = Cartesian3(0, 0, 0)
        c.x = x
        c._is_array = True
        return c

    def __len__(self):
        # it will raise TypeError if myself is not array
        return len(self.x)

    def __repr__(self):
        if self._is_array:
            rep = """Cartesian3.fromDegreesArray({x})"""
            return rep.format(x=self.x)
        elif self._is_degrees:
            rep = """Cartesian3.fromDegrees({x}, {y}, {z})"""
            return rep.format(x=self.x, y=self.y, z=self.z)
        else:
            rep = """Cartesian3({x}, {y}, {z})"""
            return rep.format(x=self.x, y=self.y, z=self.z)


class Cartesian4(_Cartesian):

    x = traitlets.Float()
    y = traitlets.Float()
    z = traitlets.Float()
    w = traitlets.Float()

    def __init__(self, x, y, z, w, degrees=False):

        self.x = x
        self.y = y
        self.z = z
        self.w = w

        self._is_degrees = degrees
        self._is_array = False

        if degrees:
            com.validate_longitude(x, key='x')
            com.validate_latitude(y, key='y')


    @classmethod
    def fromDegrees(cls, x, y, z, w):
        return Cartesian4(x, y, z, w, degrees=True)

    def __repr__(self):
        if self._is_degrees:
            rep = """Cartesian4.fromDegrees({x}, {y}, {z}, {w})"""
            return rep.format(x=self.x, y=self.y, z=self.z, w=self.w)
        else:
            rep = """Cartesian4({x}, {y}, {z}, {w})"""
            return rep.format(x=self.x, y=self.y, z=self.z, w=self.w)


def _maybe_rectangle(x, key):
    if isinstance(x, Rectangle):
        return x

    x = com.validate_listlike(x, key=key)
    if com.is_listlike_2elem(x):
        x = com._flatten_list_of_listlike(x)
    if len(x) == 4:
        return Rectangle.fromDegrees(*x)
    else:
        raise ValueError('{key} length must be 4: {x}'.format(key=key, x=x))


class Rectangle(_Cartesian):

    west = traitlets.Float()
    south = traitlets.Float()
    east = traitlets.Float()
    north = traitlets.Float()

    def __init__(self, west, south, east, north, degrees=False):

        self.west = west
        self.south = south
        self.east = east
        self.north = north

        self._is_degrees = degrees
        self._is_array = False

        if degrees:
            self.west = com.validate_longitude(west, key='west')
            self.south = com.validate_latitude(south, key='south')
            self.east = com.validate_longitude(east, key='east')
            self.north = com.validate_latitude(north, key='north')

    @classmethod
    def fromDegrees(cls, west, south, east, north):
        return Rectangle(west, south, east, north, degrees=True)

    @property
    def _inner_repr(self):
        rep = "west={west}, south={south}, east={east}, north={north}"
        return rep.format(west=self.west, south=self.south, east=self.east, north=self.north)

    def __repr__(self):
        # show more detailed repr, as arg order is not easy to remember
        if self._is_degrees:
            return "Rectangle.fromDegrees({rep})".format(rep=self._inner_repr)
        else:
            return "Rectangle({rep})".format(rep=self._inner_repr)

    @property
    def script(self):
        # we can't use repr as it is like other Cartesian
        if self._is_degrees:
            rep = """Cesium.Rectangle.fromDegrees({west}, {south}, {east}, {north})"""
            return rep.format(west=self.west, south=self.south, east=self.east, north=self.north)
        else:
            rep = """new Cesium.Rectangle({west}, {south}, {east}, {north})"""
            return rep.format(west=self.west, south=self.south, east=self.east, north=self.north)


