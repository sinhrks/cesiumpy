#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

from cesiumpy.base import _CesiumObject
import cesiumpy.entities.cartesian as cartesian
import cesiumpy.util.common as com


class Camera(_CesiumObject):

    _props = ['destination', 'orientation']

    destination = traitlets.Instance(klass=cartesian._Cartesian, allow_none=True)

    def __init__(self, widget):
        self.widget = widget
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
        from cesiumpy.entities.entity import _CesiumEntity
        import cesiumpy.extension.geocode as geocode

        if isinstance(destination, _CesiumEntity):
            # if entity has a position (not positions), use it
            if destination.position is not None:
                destination = destination.position

        destination = geocode._maybe_geocode(destination, height=100000)

        if com.is_listlike(destination) and len(destination) == 4:
            destination = cartesian.Rectangle.maybe(destination)
        else:
            destination = cartesian.Cartesian3.maybe(destination, degrees=True)
        self.destination = destination
        self.orientation = com.notimplemented(orientation)

        return self
