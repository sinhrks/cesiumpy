#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

from cesiumpy.base import _CesiumObject
from cesiumpy.entity import _CesiumEntity

import cesiumpy.cartesian as cartesian
import cesiumpy.common as com
import cesiumpy.geocode as geocode


class Camera(_CesiumObject):

    _props = ['destination', 'orientation']

    def __init__(self):
        self.destination = None
        self.orientation = None

    def __repr__(self):
        if self.destination is None:
            rep = "{klass}(destination=default)"
            return rep.format(klass=self.__class__.__name__)
        else:
            rep = "{klass}(destination={destination})"
            return rep.format(klass=self.__class__.__name__,
                              destination=self.destination)

    def flyTo(self, destination, orientation=None):
        if isinstance(destination, _CesiumEntity):
            # if entity has a position (not positions), use it
            if destination.position is not None:
                destination = destination.position

        destination = geocode._maybe_geocode(destination, height=100000)

        if com.is_listlike(destination) and len(destination) == 4:
            destination = cartesian._maybe_rectangle(destination, key='destination')
        else:
            destination = cartesian._maybe_cartesian3(destination, key='destination',
                                                      degrees=True)
        self.destination = destination
        self.orientation = com.notimplemented(orientation)

        return self
