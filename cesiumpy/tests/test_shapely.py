#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import cesiumpy
import cesiumpy.cartesian as cartesian


from cesiumpy.testing import _skip_if_no_shapely


class TestShapely(unittest.TestCase):

    def test_point_to_cartesian(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.Point(0, 1)
        res = cartesian._maybe_cartesian2(p, key='x')
        exp = cesiumpy.Cartesian2(0., 1.)
        self.assertIsInstance(res, cartesian.Cartesian2)
        self.assertEqual(res.script, exp.script)

        p = shapely.geometry.Point(0, 1, 3)
        res = cartesian._maybe_cartesian3(p, key='x')
        exp = cesiumpy.Cartesian3(0., 1., 3.)
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(res.script, exp.script)

        # ToDo: Point doesn't support more than 4 elem?
        # p = shapely.geometry.Point(0, 1, 3, 5)
        # res = cartesian._maybe_cartesian(p, key='x')
        # exp = cesiumpy.Cartesian4(0., 1., 3., 5.)
        # self.assertIsInstance(res, cartesian.Cartesian4)
        # self.assertEqual(res.script, exp.script)

    def test_point_to_cartesian_degrees(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.Point(0, 1)
        res = cartesian._maybe_cartesian2(p, key='x', degrees=True)
        exp = cesiumpy.Cartesian2.fromDegrees(0., 1.)
        self.assertIsInstance(res, cartesian.Cartesian2)
        self.assertEqual(res.script, exp.script)

        msg = "x length must be 3 to be converted to Cartesian3:"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian3(p, key='x')

        p = shapely.geometry.Point(0, 1, 3)
        res = cartesian._maybe_cartesian3(p, key='x', degrees=True)
        exp = cesiumpy.Cartesian3.fromDegrees(0., 1., 3.)
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(res.script, exp.script)

        msg = "x length must be 2 to be converted to Cartesian2:"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian2(p, key='x')

    def test_line_to_cartesian_array(self):

        _skip_if_no_shapely()
        import shapely.geometry

        p = shapely.geometry.LineString([(0, 1), (2, 3)])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        exp = cartesian.Cartesian3.fromDegreesArray([0., 1., 2., 3.])
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(res.script, exp.script)

        p = shapely.geometry.LinearRing([(0, 1), (2, 3), (1, 3)])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        # last element is being added
        exp = cartesian.Cartesian3.fromDegreesArray([0., 1., 2., 3., 1., 3., 0., 1.])
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(res.script, exp.script)

        p = shapely.geometry.Polygon([[1, 1], [1, 2], [2, 2], [2, 1]])
        res = cartesian.Cartesian3.fromDegreesArray(p)
        # last element is being added
        exp = cartesian.Cartesian3.fromDegreesArray([1., 1., 1., 2., 2., 2., 2., 1., 1., 1.])
        self.assertIsInstance(res, cartesian.Cartesian3)
        self.assertEqual(res.script, exp.script)



if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
