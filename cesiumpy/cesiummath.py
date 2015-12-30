#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import math

# renamed to cesium.math via loading, not to conflict with python math package

EPSILON1 = 0.1
EPSILON2 = 0.01
EPSILON3 = 0.001
EPSILON4 = 0.0001
EPSILON5 = 0.00001
EPSILON6 = 0.000001
EPSILON7 = 0.0000001
EPSILON8 = 0.00000001
EPSILON9 = 0.000000001
EPSILON10 = 0.0000000001
EPSILON11 = 0.00000000001
EPSILON12 = 0.000000000001
EPSILON13 = 0.0000000000001
EPSILON14 = 0.00000000000001
EPSILON15 = 0.000000000000001
EPSILON16 = 0.0000000000000001
EPSILON17 = 0.00000000000000001
EPSILON18 = 0.000000000000000001
EPSILON19 = 0.0000000000000000001
EPSILON20 = 0.00000000000000000001

GRAVITATIONALPARAMETER = 3.986004418e14

# Radius of the sun in meters: 6.955e8
SOLAR_RADIUS = 6.955e8

# The mean radius of the moon, according to the "Report of the IAU/IAG Working Group on
# Cartographic Coordinates and Rotational Elements of the Planets and satellites: 2000",
# Celestial Mechanics 82: 83-110, 2002.
LUNAR_RADIUS = 1737400.0

# 64 * 1024
SIXTY_FOUR_KILOBYTES = 64 * 1024

PI = math.pi
ONE_OVER_PI = 1.0 / PI
PI_OVER_TWO = PI * 0.5
PI_OVER_THREE = PI / 3.0
PI_OVER_FOUR = PI / 4.0
PI_OVER_SIX = PI / 6.0
THREE_PI_OVER_TWO = (3.0 * PI) * 0.5
TWO_PI = 2.0 * PI
ONE_OVER_TWO_PI = 1.0 / (2.0 * PI)

# The number of radians in a degree.
RADIANS_PER_DEGREE = PI / 180.0

# The number of degrees in a radian.
DEGREES_PER_RADIAN = 180.0 / PI

# The number of radians in an arc second.
RADIANS_PER_ARCSECOND = RADIANS_PER_DEGREE / 3600.0
