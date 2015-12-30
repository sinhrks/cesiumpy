#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six

from cesiumpy.base import _CesiumInstance
import cesiumpy.common as com


class _CesiumProvider(_CesiumInstance):

    _props = ['url']

    def __repr__(self):
        props = super(_CeciumProvider, self).__repr__()
        rep = """new {klass}({props})"""
        return rep.format(klass=self._klass, props=props)


# --------------------------------------------------
# Terrain Provider
# --------------------------------------------------


class TerrainProvider(_CesiumProvider):

    def __init__(self, url, requestVertexNormals=None,
                 requestWaterMask=None):
        self.url = com.validate_str(url, key='url')
        self.requestVertexNormals = com.validate_bool_or_none(requestVertexNormals, key='requestVertexNormals')
        self.requestWaterMask = com.validate_bool_or_none(requestWaterMask, key='requestWaterMask')


class ArcGisImageServerTerrainProvider(TerrainProvider):
    pass


class CesiumTerrainProvider(TerrainProvider):
    pass


class EllipsoidTerrainProvider(TerrainProvider):
    pass


class VRTheWorldTerrainProvider(TerrainProvider):
    pass


# --------------------------------------------------
# Imagery Provider
# --------------------------------------------------


class ImageryProvider(_CesiumProvider):

    @property
    def _klass(self):
        return "Cesium.{0}".format(self.__class__.__name__)

    _props = ['url', 'baseLayerPicker']

    def __init__(self, url, baseLayerPicker=None,
                 maximumLevel=None, credit=None):
        self.url = com.validate_str(url, key='url')
        self.baseLayerPicker = com.validate_bool_or_none(baseLayerPicker, key='baseLayerPicker')
        self.maximumLevel = com.validate_numeric_or_none(maximumLevel, key='maximumLevel')
        self.credit = com.validate_str_or_none(credit, key='credit')


class ArcGisMapServerImageryProvider(ImageryProvider):
    pass


class BingMapsImageryProvider(ImageryProvider):
    pass


class GoogleEarthImageryProvider(ImageryProvider):
    pass


class GridImageryProvider(ImageryProvider):
    pass


class MapboxImageryProvider(ImageryProvider):
    pass


class OpenStreetMapImageryProvider(ImageryProvider):
    pass


class SingleTileImageryProvider(ImageryProvider):
    pass


class TileCoordinatesImageryProvider(ImageryProvider):
    pass


class TileMapServiceImageryProvider(ImageryProvider):
    pass


class UrlTemplateImageryProvider(ImageryProvider):
    pass


class WebMapServiceImageryProvider(ImageryProvider):
    pass


class WebMapTileServiceImageryProvider(ImageryProvider):
    pass

