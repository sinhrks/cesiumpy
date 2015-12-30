#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import cesiumpy
import cesiumpy.cartesian as cartesian

import shapely.geometry


class TestShapely(unittest.TestCase):

    def test_point_to_cartesian(self):
        p = shapely.geometry.Point(0, 1)
        res = cartesian._maybe_cartesian(p)
        exp = cesiumpy.Cartesian2(0., 1.)
        self.assertIsInstance(res, cartesian.Cartesian2)
        self.assertEqual(repr(res), repr(exp))

        p = shapely.geometry.Point(0, 1, 3)
        res = cartesian._maybe_cartesian(p)
        exp = cesiumpy.Cartesian3(0., 1., 3.)
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(repr(res), repr(exp))

        # ToDo: Point doesn't support more than 4 elem?
        p = shapely.geometry.Point(0, 1, 3, 5)
        res = cartesian._maybe_cartesian(p)
        exp = cesiumpy.Cartesian4(0., 1., 3., 5.)
        # self.assertIsInstance(res, cartesian.Cartesian4)
        # self.assertEqual(repr(res), repr(exp))

    def test_point_to_cartesian_degrees(self):
        p = shapely.geometry.Point(0, 1)
        res = cartesian._maybe_cartesian_degrees(p)
        exp = cesiumpy.Cartesian2.fromDegrees(0., 1.)
        self.assertIsInstance(res, cartesian.Cartesian2)
        self.assertEqual(repr(res), repr(exp))

        p = shapely.geometry.Point(0, 1, 3)
        res = cartesian._maybe_cartesian_degrees(p)
        exp = cesiumpy.Cartesian3.fromDegrees(0., 1., 3.)
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(repr(res), repr(exp))

    def test_line_to_cartesian_array(self):
        p = shapely.geometry.LineString([(0, 1), (2, 3)])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        exp = cartesian.Cartesian3.fromDegreesArray([0., 1., 2., 3.])
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(repr(res), repr(exp))

        p = shapely.geometry.LinearRing([(0, 1), (2, 3), (1, 3)])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        # last element is being added
        exp = cartesian.Cartesian3.fromDegreesArray([0., 1., 2., 3., 1., 3., 0., 1.])
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(repr(res), repr(exp))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
