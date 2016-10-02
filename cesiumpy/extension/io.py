#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import json

from cesiumpy.extension.shapefile import to_entity
import cesiumpy.util.common as com


def read_geojson(path):

    sp = com._check_package('shapely.geometry')

    with open(path) as f:
        geos = json.load(f)

    # shapely can't parse featurecollection directly
    results = []
    for feature in geos['features']:
        shape = sp.shape(feature['geometry'])
        result = to_entity(shape)
        if isinstance(result, list):
            results.extend(result)
        else:
            results.append(result)
    return results


def read_shape(path):
    sp = com._check_package('shapely.geometry')
    fiona = com._check_package('fiona')

    results = []
    with fiona.open(path) as f:
        for shape in f:
            shape = sp.shape(shape['geometry'])
            result = to_entity(shape)
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)
    return results
