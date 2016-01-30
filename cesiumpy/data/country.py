#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import json
import six

import cesiumpy
import cesiumpy.common as com


current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, 'countries')


class CountryLoader(object):

    def __init__(self):
        self._countries = None


    """
    def countries(self):
        # ToDo:
        if self._countries is None:
            path = os.path.join(data_path, 'countries.json')
            with open(path) as f:
                self._countries = json.load(f)
        return self._countries
    """

    def __getattr__(self, name):
        fname = name.lower()
        path = os.path.join(data_path, 'data', '{0}.geo.json'.format(fname))
        if os.path.exists(path):
            from cesiumpy.extension.shapefile import read_geojson
            return read_geojson(path)
        else:
            msg = "Unable to load country data, file not found: '{name}'"
            raise AttributeError(msg.format(name=name))
