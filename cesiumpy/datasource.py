#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import warnings

from cesiumpy.base import _CesiumObject
import cesiumpy.color
import cesiumpy.common as com


class DataSource(_CesiumObject):

    _props = []

    def __init__(self, sourceUri):
        self.sourceUri = com.validate_str(sourceUri, key='sourceUri')
        self._check_uri(self.sourceUri)

    def _check_uri(self, sourceUri):
        if not os.path.exists(sourceUri):
            msg = "Unable to read specified path, be sure to the output HTML can read the path: {0}"
            warnings.warn(msg.format(sourceUri))

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

class GeoJsonDataSource(DataSource):
    """
    GeoJsonDataSource

    Parameters
    ----------

    sourceUri: str
        Overrides the url to use for resolving relative links.
    describe: GeoJsonDataSource~describe, default GeoJsonDataSource.defaultDescribeProperty
        A function which returns a Property object (or just a string), which converts the properties into an html description.
    markerSize: int, default GeoJsonDataSource.markerSize
        The default size of the map pin created for each point, in pixels.
    markerSymbol: str, default GeoJsonDataSource.markerSymbol
        The default symbol of the map pin created for each point.
    markerColor: Color, default GeoJsonDataSource.markerColor
        The default color of the map pin created for each point.
    stroke: Color, default GeoJsonDataSource.stroke
        The default color of polylines and polygon outlines.
    strokeWidth: int, GeoJsonDataSource.strokeWidth
        The default width of polylines and polygon outlines.
    fill: Color, default GeoJsonDataSource.fill
        The default color for polygon interiors.
    """

    _props = ['describe', 'markerSize', 'markerSymbol', 'markerColor',
              'stroke', 'strokeWidth', 'fill']

    def __init__(self, sourceUri, describe=None, markerSize=None,
                 markerSymbol=None, markerColor=None, stroke=None,
                 strokeWidth=None, fill=None):
        super(GeoJsonDataSource, self).__init__(sourceUri=sourceUri)

        self.describe = com.notimplemented(describe)

        self.markerSize = com.validate_numeric_or_none(markerSize, key='markerSize')
        self.markerSymbol = com.validate_str_or_none(markerSymbol, key='markerSymbol')
        self.markerColor = cesiumpy.color.validate_color_or_none(markerColor, key='markerColor')
        self.stroke = cesiumpy.color.validate_color_or_none(stroke, key='stroke')
        self.strokeWidth = com.validate_numeric_or_none(strokeWidth, key='strokeWidth')
        self.fill = cesiumpy.color.validate_color_or_none(fill, key='fill')


class KmlDataSource(DataSource):
    """
    KmlDataSource

    Parameters
    ----------

    sourceUri: str
        Overrides the url to use for resolving relative links and other KML network features.
    """

    pass

