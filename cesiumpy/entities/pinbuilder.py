#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
from cesiumpy.util.trait import MaybeTrait, URITrait


class _BillboardContents(_CesiumObject):
    pass


class Icon(_BillboardContents):

    # different from ImageMaterialProperty

    image = URITrait()

    def __init__(self, image):
        self.image = image

    @property
    def script(self):
        return '"{path}"'.format(path=self.image)


class Pin(_BillboardContents):

    # default color, all attrs are mandatory
    color = MaybeTrait(klass=cesiumpy.color.Color)
    size = traitlets.Float()
    text = traitlets.Unicode(allow_none=True)

    def __init__(self, color=None, size=48, text=None):

        if color is None:
            # default color, all attrs are mandatory
            color = cesiumpy.color.ROYALBLUE
        if size is None:
            size = 48

        self.color = color
        self.size = size
        # text may be set against Pin
        self.text = text

    @classmethod
    def fromColor(self, color, size=48):
        """
        Create pin specifying color and size

        Parameters
        ----------

        color : Color
            A Property specifying the Color of the pin.
        size : int, default 48
            A Property specifying the size of the pin.
        """
        return Pin(color=color, size=size)

    @classmethod
    def fromText(self, text, color=None, size=48):
        """
        Create pin specifying text, color and size

        Parameters
        ----------

        text : str
            A Property specifying the text of the pin.
        color : Color
            A Property specifying the Color of the pin.
        size : int, default 48
            A Property specifying the size of the pin.
        """
        # validate text is not None
        if text is None:
            self.text.error(self.text, text)
        return Pin(color=color, size=size, text=text)

    def __repr__(self):
        if self.text is None:
            rep = """Pin({color}, {size})"""
            return rep.format(color=self.color, size=self.size)
        else:
            rep = """Pin("{text}", {color}, {size})"""
            return rep.format(text=self.text, color=self.color, size=self.size)

    @property
    def script(self):
        # ToDo: make "pinBuilder" as global variable?
        if self.text is None:
            rep = """new Cesium.PinBuilder().fromColor({color}, {size})"""
            return rep.format(color=self.color.script, size=self.size)
        else:
            rep = """new Cesium.PinBuilder().fromText("{text}", {color}, {size})"""
            return rep.format(text=self.text, color=self.color.script, size=self.size)
