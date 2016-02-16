#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject, _CesiumBase, RistrictedList


class Scene(_CesiumObject):

    widget = traitlets.Instance(klass=_CesiumBase)

    def __init__(self, widget):
        self.widget = widget
        self._primitives = RistrictedList(self.widget, allowed=cesiumpy.Model,
                                          propertyname='scene.primitives')

    @property
    def primitives(self):
        return self._primitives

    @property
    def script(self):
        return self._primitives.script
