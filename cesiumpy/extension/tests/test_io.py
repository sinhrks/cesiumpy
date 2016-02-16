#!/usr/bin/env python
# coding: utf-8

import nose
import os
import unittest

import cesiumpy
from cesiumpy.testing import _skip_if_no_shapely


current_dir = os.path.dirname(__file__)


class TestIO(unittest.TestCase):

    def test_geojson(self):
        _skip_if_no_shapely()

        path = os.path.join(current_dir, 'data', 'jpn.geo.json')
        self.assertTrue(os.path.exists(path))
        res = cesiumpy.io.read_geojson(path)
        exp = """{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([153.958588, 24.295, 153.953308, 24.292774, 153.946625, 24.293331, 153.942749, 24.296944, 153.939697, 24.300831, 153.938873, 24.306942, 153.940247, 24.312496, 153.947754, 24.319443, 153.952759, 24.321384, 153.960236, 24.321663, 153.96579, 24.31361, 153.96579, 24.309441, 153.963013, 24.29833, 153.958588, 24.295])}}"""
        self.assertIsInstance(res, list)
        self.assertTrue(all([isinstance(e, cesiumpy.Polygon) for e in res]))
        self.assertEqual(res[0].script, exp)

    def test_shape(self):
        _skip_if_no_shapely()

        path = os.path.join(current_dir, 'data', 'coastl_jpn.shp')
        self.assertTrue(os.path.exists(path))
        res = cesiumpy.io.read_shape(path)
        exp = """{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([136.06983283646417, 20.425446784039757, 136.06989943430338, 20.4254103630917, 136.06994984324314, 20.42536719269311, 136.06998867703822, 20.425312805816333, 136.07000535502831, 20.425227687745696, 136.06997763989327, 20.42514023834311, 136.06994170803583, 20.425077341289573, 136.06981677798885, 20.425014868114573, 136.06967221910506, 20.425023785866852, 136.06956593971367, 20.425117626053517, 136.06954869111786, 20.425169632689283, 136.06952692658533, 20.425285954741376, 136.06955619050734, 20.425353954640368, 136.06961863107628, 20.42540397230762, 136.06966507838203, 20.42543426331992, 136.06969721163566, 20.425443213678243, 136.06975939135629, 20.42545514748933, 136.06983283646417, 20.425446784039757])}}"""
        self.assertIsInstance(res, list)
        self.assertTrue(all([isinstance(e, cesiumpy.Polyline) for e in res]))
        self.assertEqual(res[0].script, exp)


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
