#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six
import cesiumpy.cartesian as cartesian
import cesiumpy.color as color
import cesiumpy.common as com


class CesiumEntity(object):

    @property
    def _klass(self):
        raise NotImplementedError('must be overriden in child classes')

    def __init__(self, position, name=None):
        self.position = position
        self.name = name
        # ToDo: instanciate corredt Cartesian from input

    def _make_entity_repr(self, **kwargs):
        result = com.to_jsobject(kwargs)
        return result

class Cylinder(CesiumEntity):

    _klass = 'cylinder'

    def __init__(self, length, topRadius,
                 bottomRadius, material=None):
        self.length = length
        self.topRadius = topRadius
        self.bottomRadius = bottomRadius

        if material is not None:
            if not isinstance(material, color.CesiumColor):
                msg = 'material must be a CesiumColor instance, {0} given'
                raise ValueError(msg.format(type(material)))
        self.material = material

    def __repr__(self):
        results = self._make_entity_repr(length=self.length, topRadius=self.topRadius,
                                         bottomRadius=self.bottomRadius,
                                         material=self.material)
        return ''.join(results)


class Polygon(CesiumEntity):

    _klass = 'polygon'

    def __init__(self, hierarchy,
                 material=None, outline=True, outlineColor=None):

        if not isinstance(hierarchy, list):
            msg = 'hierarchy must be a list, {0} given'
            raise ValueError(msg.format(type(hierarchy)))

        if len(hierarchy) % 2 != 0:
            msg = 'hierarchy lenth must be even number: {0}'
            raise ValueError(msg.format(hierarchy))
        self.hierarchy = cartesian.Cartesian3Array(hierarchy)

        if material is not None:
            if not isinstance(material, color.CesiumColor):
                msg = 'material must be a CesiumColor instance, {0} given'
                raise ValueError(msg.format(type(material)))
        self.material = material

        if not isinstance(outline, bool):
            msg = 'outline must be a bool, {0} given'
            raise ValueError(msg.format(type(outline)))
        self.outline = outline

        if outlineColor is not None:
            if not isinstance(outlineColor, color.CesiumColor):
                msg = 'material must be a CesiumColor instance, {0} given'
                raise ValueError(msg.format(type(outlineColor)))
        self.outlineColor = outlineColor

    def __repr__(self):
        results = self._make_entity_repr(hierarchy=self.hierarchy, material=self.material,
                                         outline=self.outline, outlineColor=self.outlineColor)
        return ''.join(results)
