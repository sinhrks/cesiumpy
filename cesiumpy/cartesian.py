#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals


class CesiumCartesian(object):
    def __init__(self):
        raise NotImplementedError


def _maybe_cartesian(x):
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


class Cartesian2(CesiumCartesian):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        rep = """Cesium.Cartesian2.fromDegrees({x}, {y})"""
        return rep.format(x=self.x, y=self.y)


class Cartesian3(CesiumCartesian):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        rep = """Cesium.Cartesian3.fromDegrees({x}, {y}, {z})"""
        return rep.format(x=self.x, y=self.y, z=self.z)


class Cartesian4(CesiumCartesian):

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        rep = """Cesium.Cartesian4.fromDegrees({x}, {y}, {z}, {w})"""
        return rep.format(x=self.x, y=self.y, z=self.z, w=self.w)


# ToDo: Cartesian3 should be a factory?
class Cartesian3Array(CesiumCartesian):

    def __init__(self, x):
        if not isinstance(x, list):
            raise ValueError('x must be a list')
        self.x = x

    def __repr__(self):
        rep = """Cesium.Cartesian3.fromDegreesArray({x})"""
        return rep.format(x=self.x)

