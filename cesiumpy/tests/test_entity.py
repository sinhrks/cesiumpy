#!/usr/bin/env python
# coding: utf-8

# do not import unicode_literals here to test ASCII in Python 2.7

import unittest
import nose

import cesiumpy


class TestEntity(unittest.TestCase):

    def test_cylinder(self):
        e = cesiumpy.Cylinder(10, 100, 200, cesiumpy.color.AQUA)
        exp = "{length : 10, material : Cesium.Color.AQUA, topRadius : 100, bottomRadius : 200}"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Cylinder(10, 100, 200)
        exp = "{length : 10, topRadius : 100, bottomRadius : 200}"
        self.assertEqual(repr(e), exp)

    def test_polygon(self):
        e = cesiumpy.Polygon([1, 1, 2, 2])
        exp = "{hierarchy : Cesium.Cartesian3.fromDegreesArray([1, 1, 2, 2]), outline : true}"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Polygon([1, 1, 2, 2], cesiumpy.color.AQUA)
        exp = "{hierarchy : Cesium.Cartesian3.fromDegreesArray([1, 1, 2, 2]), material : Cesium.Color.AQUA, outline : true}"
        self.assertEqual(repr(e), exp)

if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
