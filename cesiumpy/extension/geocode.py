#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six
from geopy.geocoders import GoogleV3

import cesiumpy.util.common as com

# ToDo: want different geocoders?
_GEOCODER = GoogleV3()


def _maybe_geocode(x, height=None):
    """
    geocode passed str or its list-like
    height can be used to create base data for Cartesian3
    """
    if isinstance(x, six.string_types):
        loc = _GEOCODER.geocode(x)
        if loc is not None:
            if height is None:
                # return x, y order
                return loc.longitude, loc.latitude
            else:
                return loc.longitude, loc.latitude, height
    elif com.is_listlike(x):
        return [_maybe_geocode(e) for e in x]

    return x
