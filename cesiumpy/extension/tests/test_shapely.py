#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import cesiumpy
import cesiumpy.entities.cartesian as cartesian
from cesiumpy.testing import _skip_if_no_shapely


class TestShapelyCartesian(unittest.TestCase):

    def test_point_to_cartesian(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.Point(0, 1)
        res = cartesian.Cartesian2.maybe(p)
        exp = cesiumpy.Cartesian2(0., 1.)
        self.assertIsInstance(res, cartesian.Cartesian2)
        self.assertEqual(res.script, exp.script)

        p = shapely.geometry.Point(0, 1, 3)
        res = cartesian.Cartesian3.maybe(p)
        exp = cesiumpy.Cartesian3(0., 1., 3.)
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(res.script, exp.script)

        # ToDo: Point doesn't support more than 4 elem?
        # p = shapely.geometry.Point(0, 1, 3, 5)
        # res = cartesian.Cartesian4.maybe(p, key='x')
        # exp = cesiumpy.Cartesian4(0., 1., 3., 5.)
        # self.assertIsInstance(res, cartesian.Cartesian4)
        # self.assertEqual(res.script, exp.script)

    def test_point_to_cartesian_degrees(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.Point(0, 1)
        res = cartesian.Cartesian2.maybe(p, degrees=True)
        exp = cesiumpy.Cartesian2.fromDegrees(0., 1.)
        self.assertIsInstance(res, cartesian.Cartesian2)
        self.assertEqual(res.script, exp.script)

        # do not convert
        res = cartesian.Cartesian3.maybe(p)
        self.assertEqual(res, [0., 1.])

        p = shapely.geometry.Point(0, 1, 3)
        res = cartesian.Cartesian3.maybe(p, degrees=True)
        exp = cesiumpy.Cartesian3.fromDegrees(0., 1., 3.)
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(res.script, exp.script)

        # do not convert
        res = cartesian.Cartesian2.maybe(p)
        self.assertEqual(res, [0., 1., 3.])

    def test_line_to_cartesian_array(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.LineString([(0, 1), (2, 3)])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        exp = cartesian.Cartesian3.fromDegreesArray([0., 1., 2., 3.])
        self.assertIsInstance(res, cartesian.Cartesian3Array)
        self.assertEqual(res.script, exp.script)

        p = shapely.geometry.LinearRing([(0, 1), (2, 3), (1, 3)])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        # last element is being added
        exp = cartesian.Cartesian3.fromDegreesArray([0., 1., 2., 3., 1., 3., 0., 1.])
        self.assertIsInstance(res, cartesian.Cartesian3Array)
        self.assertEqual(res.script, exp.script)

    def test_polygon_to_cartesian_array(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.Polygon([[1, 1], [1, 2], [2, 2], [2, 1]])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        exp = cartesian.Cartesian3.fromDegreesArray([1., 1., 1., 2., 2., 2., 2., 1., 1., 1.])
        self.assertIsInstance(res, cartesian.Cartesian3Array)
        self.assertEqual(res.script, exp.script)


class TestShapelyEntity(unittest.TestCase):

    def test_point_to_entity(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.Point(0, 1)
        res = cesiumpy.extension.shapefile.to_entity(p)
        exp = """{position : Cesium.Cartesian3.fromDegrees(0.0, 1.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}}"""
        self.assertEqual(res.script, exp)

        p = shapely.geometry.Point(0, 1, 3)
        res = cesiumpy.extension.shapefile.to_entity(p)
        exp = """{position : Cesium.Cartesian3.fromDegrees(0.0, 1.0, 3.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}}"""
        self.assertEqual(res.script, exp)

        # multipoint
        p = shapely.geometry.MultiPoint([[1, 1], [1, 2], [2, 2], [2, 1]])
        res = cesiumpy.extension.shapefile.to_entity(p)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 4)

        exp = ['{position : Cesium.Cartesian3.fromDegrees(1.0, 1.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}}',
               '{position : Cesium.Cartesian3.fromDegrees(1.0, 2.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}}',
               '{position : Cesium.Cartesian3.fromDegrees(2.0, 2.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}}',
               '{position : Cesium.Cartesian3.fromDegrees(2.0, 1.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}}']
        self.assertEqual([e.script for e in res], exp)

    def test_line_to_entity(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.LineString([(0, 1), (2, 3)])
        res = cesiumpy.extension.shapefile.to_entity(p)
        exp = """{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([0.0, 1.0, 2.0, 3.0])}}"""
        self.assertEqual(res.script, exp)

        p = shapely.geometry.LinearRing([(0, 1), (2, 3), (1, 3)])
        res = cesiumpy.extension.shapefile.to_entity(p)
        # last element is being added
        exp = """{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([0.0, 1.0, 2.0, 3.0, 1.0, 3.0, 0.0, 1.0])}}"""
        self.assertEqual(res.script, exp)

        # multilinestring
        p = shapely.geometry.MultiLineString([[[1, 1], [1, 2]], [[2, 2], [2, 1]]])
        res = cesiumpy.extension.shapefile.to_entity(p)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)

        exp = ['{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([1.0, 1.0, 1.0, 2.0])}}',
               '{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([2.0, 2.0, 2.0, 1.0])}}']
        self.assertEqual([e.script for e in res], exp)

    def test_polygon_to_entity(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.Polygon([[1, 1], [1, 2], [2, 2], [2, 1]])
        res = cesiumpy.extension.shapefile.to_entity(p)
        exp = """{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0])}}"""
        self.assertEqual(res.script, exp)

        # multipolygon
        p1 = shapely.geometry.Polygon([[1, 1], [1, 2], [2, 2], [2, 1]])
        p2 = shapely.geometry.Polygon([[3, 3], [3, 4], [4, 4], [4, 3]])
        p = shapely.geometry.MultiPolygon([p1, p2])
        res = cesiumpy.extension.shapefile.to_entity(p)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 2)

        exp = ['{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([1.0, 1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0])}}',
               '{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([3.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 3.0, 3.0, 3.0])}}']
        self.assertEqual([e.script for e in res], exp)


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
