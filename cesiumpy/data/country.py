#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import json

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, 'countries')


class CountryLoader(object):

    def __init__(self):
        self._countries = None

    @property
    def countries(self):
        if self._countries is None:
            countries = {}
            path = os.path.join(data_path, 'countries.json')

            with open(path) as f:
                data = json.load(f)
                for entry in data:
                    cca3 = entry['cca3'].lower()
                    countries[entry['cca2'].lower()] = cca3
                    countries[entry['name']['official'].lower()] = cca3

            self._countries = countries
        return self._countries

    def get(self, name):
        fname = name.lower()
        fname = self.countries.get(fname, fname)
        path = os.path.join(data_path, 'data', '{0}.geo.json'.format(fname))
        if os.path.exists(path):
            from cesiumpy.extension.io import read_geojson
            return read_geojson(path)
        else:
            msg = "Unable to load country data, file not found: '{name}'"
            raise ValueError(msg.format(name=name))

    def __getattr__(self, name):
        try:
            return self.get(name)
        except ValueError:
            msg = "Unable to load country data, file not found: '{name}'"
            raise AttributeError(msg.format(name=name))
