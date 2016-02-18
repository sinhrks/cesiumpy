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


class Math(_CesiumEnum):

    EPSILON1 = 'Cesium.Math.EPSILON1'
    EPSILON2 = 'Cesium.Math.EPSILON2'
    EPSILON3 = 'Cesium.Math.EPSILON3'
    EPSILON4 = 'Cesium.Math.EPSILON4'
    EPSILON5 = 'Cesium.Math.EPSILON5'
    EPSILON6 = 'Cesium.Math.EPSILON6'
    EPSILON7 = 'Cesium.Math.EPSILON7'
    EPSILON8 = 'Cesium.Math.EPSILON8'
    EPSILON9 = 'Cesium.Math.EPSILON9'
    EPSILON10 = 'Cesium.Math.EPSILON10'
    EPSILON11 = 'Cesium.Math.EPSILON11'
    EPSILON12 = 'Cesium.Math.EPSILON12'
    EPSILON13 = 'Cesium.Math.EPSILON13'
    EPSILON14 = 'Cesium.Math.EPSILON14'
    EPSILON15 = 'Cesium.Math.EPSILON15'
    EPSILON16 = 'Cesium.Math.EPSILON16'
    EPSILON17 = 'Cesium.Math.EPSILON17'
    EPSILON18 = 'Cesium.Math.EPSILON18'
    EPSILON19 = 'Cesium.Math.EPSILON19'
    EPSILON20 = 'Cesium.Math.EPSILON20'

    GRAVITATIONALPARAMETER = 'Cesium.Math.GRAVITATIONALPARAMETER'

    # Radius of the sun in meters: 6.955e8
    SOLAR_RADIUS = 'Cesium.Math.SOLAR_RADIUS'

    # The mean radius of the moon, according to the "Report of the IAU/IAG Working Group on
    # Cartographic Coordinates and Rotational Elements of the Planets and satellites: 2000",
    # Celestial Mechanics 82: 83-110, 2002.
    LUNAR_RADIUS = 'Cesium.Math.LUNAR_RADIUS'

    # 64 * 1024
    SIXTY_FOUR_KILOBYTES = 'Cesium.Math.SIXTY_FOUR_KILOBYTES'

    PI = 'Cesium.Math.PI'
    ONE_OVER_PI = 'Cesium.Math.ONE_OVER_PI'
    PI_OVER_TWO = 'Cesium.Math.PI_OVER_TWO'
    PI_OVER_THREE = 'Cesium.Math.PI_OVER_THREE'
    PI_OVER_FOUR = 'Cesium.Math.PI_OVER_FOUR'
    PI_OVER_SIX = 'Cesium.Math.PI_OVER_SIX'
    THREE_PI_OVER_TWO = 'Cesium.Math.THREE_PI_OVER_TWO'
    TWO_PI = 'Cesium.Math.TWO_PI'
    ONE_OVER_TWO_PI = 'Cesium.Math.ONE_OVER_TWO_PI'

    # The number of radians in a degree.
    RADIANS_PER_DEGREE = 'Cesium.Math.RADIANS_PER_DEGREE'

    # The number of degrees in a radian.
    DEGREES_PER_RADIAN = 'Cesium.Math.RADIANS_PER_DEGREE'

    # The number of radians in an arc second.
    RADIANS_PER_ARCSECOND = 'RADIANS_PER_ARCSECOND'
