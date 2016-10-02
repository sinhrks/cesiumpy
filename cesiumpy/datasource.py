#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

from cesiumpy.base import _CesiumObject
import cesiumpy.entities.color
import cesiumpy.util.common as com
from cesiumpy.util.trait import MaybeTrait, URITrait


class DataSource(_CesiumObject):

    _props = []

    sourceUri = URITrait()

    def __init__(self, sourceUri):
        self.sourceUri = sourceUri

    @property
    def script(self):
        props = com.to_jsobject(self._property_dict)
        props = ''.join(props)
        if props != '':
            script = """{klass}.load("{source}", {props})"""
            script = script.format(klass=self._klass,
                                   source=self.sourceUri, props=''.join(props))
        else:
            script = """{klass}.load("{source}")"""
            script = script.format(klass=self._klass, source=self.sourceUri)
        return script

    @classmethod
    def load(cls, sourceUri, *args, **kwargs):
        return cls(sourceUri, *args, **kwargs)


class CustomDataSource(DataSource):
    pass


class CzmlDataSource(DataSource):
    pass

    def __init__(self, sourceUri):
        super(CzmlDataSource, self).__init__(sourceUri=sourceUri)


class GeoJsonDataSource(DataSource):
    """
    GeoJsonDataSource

    Parameters
    ----------

    sourceUri : str
        Overrides the url to use for resolving relative links.
    describe : GeoJsonDataSource~describe, default GeoJsonDataSource.defaultDescribeProperty
        A function which returns a Property object (or just a string), which converts the properties into an html description.
    markerSize : int, default GeoJsonDataSource.markerSize
        The default size of the map pin created for each point, in pixels.
    markerSymbol : str, default GeoJsonDataSource.markerSymbol
        The default symbol of the map pin created for each point.
    markerColor : Color, default GeoJsonDataSource.markerColor
        The default color of the map pin created for each point.
    stroke : Color, default GeoJsonDataSource.stroke
        The default color of polylines and polygon outlines.
    strokeWidth : int, GeoJsonDataSource.strokeWidth
        The default width of polylines and polygon outlines.
    fill : Color, default GeoJsonDataSource.fill
        The default color for polygon interiors.
    """

    _props = ['describe', 'markerSize', 'markerSymbol', 'markerColor',
              'stroke', 'strokeWidth', 'fill']

    markerSize = traitlets.Float(allow_none=True)
    markerSymbol = traitlets.Unicode(allow_none=True)
    markerColor = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    stroke = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    strokeWidth = traitlets.Float(allow_none=True)
    fill = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    def __init__(self, sourceUri, describe=None, markerSize=None,
                 markerSymbol=None, markerColor=None, stroke=None,
                 strokeWidth=None, fill=None):
        super(GeoJsonDataSource, self).__init__(sourceUri=sourceUri)

        self.describe = com.notimplemented(describe)

        self.markerSize = markerSize
        self.markerSymbol = markerSymbol
        self.markerColor = markerColor
        self.stroke = stroke
        self.strokeWidth = strokeWidth
        self.fill = fill


class KmlDataSource(DataSource):
    """
    KmlDataSource

    Parameters
    ----------

    sourceUri : str
        Overrides the url to use for resolving relative links and other KML network features.
    """

    pass
