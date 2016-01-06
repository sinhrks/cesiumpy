#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

from cesiumpy.base import _CesiumEnum


class VerticalOrigin(_CesiumEnum):

    BOTTOM = 'Cesium.VerticalOrigin.BOTTOM'
    CENTER = 'Cesium.VerticalOrigin.CENTER'
    TOP = 'Cesium.VerticalOrigin.TOP'


class HorizontalOrigin(_CesiumEnum):

    CENTER = 'Cesium.HorizontalOrigin.CENTER'
    LEFT = 'Cesium.HorizontalOrigin.LEFT'
    RIGHT = 'Cesium.HorizontalOrigin.RIGHT'


class CornerType(_CesiumEnum):
    BEVELED = 'Cesium.CornerType.BEVELED'
    MITERED = 'Cesium.CornerType.MITERED'
    ROUNDED = 'Cesium.CornerType.ROUNDED'