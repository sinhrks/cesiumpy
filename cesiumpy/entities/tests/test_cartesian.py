#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import cesiumpy
import cesiumpy.entities.cartesian as cartesian


class TestCartesian(unittest.TestCase):

    def test_cartesian2(self):
        c = cesiumpy.Cartesian2(5, 10)
        exp = "new Cesium.Cartesian2(5.0, 10.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.Cartesian2.fromDegrees(5, 10)
        exp = "Cesium.Cartesian2.fromDegrees(5.0, 10.0)"
        self.assertEqual(c.script, exp)

        msg = "x must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian2.fromDegrees(200, 10)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian2.fromDegrees(50, 100)

    def test_cartesian2_repr(self):
        c = cesiumpy.Cartesian2(5, 10)
        exp = "Cartesian2(5.0, 10.0)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian2.fromDegrees(5, 10)
        exp = "Cartesian2.fromDegrees(5.0, 10.0)"
        self.assertEqual(repr(c), exp)

    def test_cartesian3(self):
        c = cesiumpy.Cartesian3(5, 10, 20)
        exp = "new Cesium.Cartesian3(5.0, 10.0, 20.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.Cartesian3.fromDegrees(5, 10, 20)
        exp = "Cesium.Cartesian3.fromDegrees(5.0, 10.0, 20.0)"
        self.assertEqual(c.script, exp)

        msg = "x must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegrees(200, 10, 20)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegrees(50, 100, 20)

    def test_cartesian3_repr(self):
        c = cesiumpy.Cartesian3(5, 10, 20)
        exp = "Cartesian3(5.0, 10.0, 20.0)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian3.fromDegrees(5, 10, 20)
        exp = "Cartesian3.fromDegrees(5.0, 10.0, 20.0)"
        self.assertEqual(repr(c), exp)

    def test_cartesian3_array(self):
        c = cesiumpy.Cartesian3.fromDegreesArray([1, 2, 3, 4])
        exp = "Cesium.Cartesian3.fromDegreesArray([1, 2, 3, 4])"
        self.assertEqual(c.script, exp)

        # we can pass tuple
        c = cesiumpy.Cartesian3.fromDegreesArray([(1, 2), (3, 4)])
        self.assertEqual(c.script, exp)

        c = cesiumpy.Cartesian3.fromDegreesArray(((1, 2), (3, 4)))
        self.assertEqual(c.script, exp)

        c = cesiumpy.Cartesian3.fromDegreesArray([1, 2, 3, 4, 5, 6, 7, 8])
        exp = "Cesium.Cartesian3.fromDegreesArray([1, 2, 3, 4, 5, 6, 7, 8])"
        self.assertEqual(c.script, exp)

        # we can pass tuple
        c = cesiumpy.Cartesian3.fromDegreesArray([(1, 2), (3, 4), (5, 6), (7, 8)])
        self.assertEqual(c.script, exp)

        msg = "x must be list-likes: 1"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray(1)

        msg = "x length must be an even number: \\[1, 2, 3\\]"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray([1, 2, 3])

        msg = "x must be a list consists from longitude and latitude"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray([10, 20, 200, 20])

        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray([(10, 20), (200, 20)])

        with nose.tools.assert_raises_regexp(ValueError, msg):
            import geopy
            try:
                # string causes geocode search
                cesiumpy.Cartesian3.fromDegreesArray([('X', 20), (20, 20)])
            except geopy.exc.GeocoderQuotaExceeded:
                raise nose.SkipTest("exceeded geocoder quota")

        msg = "x must be a list consists from longitude and latitude"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray([10, 20, 20, 91])

    def test_cartesian4(self):
        c = cesiumpy.Cartesian4(5, 10, 20, 30)
        exp = "new Cesium.Cartesian4(5.0, 10.0, 20.0, 30.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.Cartesian4.fromDegrees(5, 10, 20, 30)
        exp = "Cesium.Cartesian4.fromDegrees(5.0, 10.0, 20.0, 30.0)"
        self.assertEqual(c.script, exp)

        msg = "x must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian4.fromDegrees(200, 10, 20, 50)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian4.fromDegrees(50, 100, 20, 50)

    def test_cartesian4_repr(self):
        c = cesiumpy.Cartesian4(5, 10, 20, 30)
        exp = "Cartesian4(5.0, 10.0, 20.0, 30.0)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian4.fromDegrees(5, 10, 20, 30)
        exp = "Cartesian4.fromDegrees(5.0, 10.0, 20.0, 30.0)"
        self.assertEqual(repr(c), exp)

    def test_maybe_cartesian(self):
        c = cesiumpy.entities.cartesian.Cartesian2.maybe((0, 10))
        exp = "new Cesium.Cartesian2(0.0, 10.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian3.maybe((0, 10, 20))
        exp = "new Cesium.Cartesian3(0.0, 10.0, 20.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian4.maybe((0, 10, 20, 30))
        exp = "new Cesium.Cartesian4(0.0, 10.0, 20.0, 30.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian2.maybe([0, 10])
        exp = "new Cesium.Cartesian2(0.0, 10.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian3.maybe([0, 10, 20])
        exp = "new Cesium.Cartesian3(0.0, 10.0, 20.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian4.maybe([0, 10, 20, 30])
        exp = "new Cesium.Cartesian4(0.0, 10.0, 20.0, 30.0)"
        self.assertEqual(c.script, exp)

        # do not convert
        res = cartesian.Cartesian2.maybe(3)
        self.assertEqual(res, 3)

        res = cartesian.Cartesian2.maybe((1, 2, 3, 5, 5))
        self.assertEqual(res, (1, 2, 3, 5, 5))

    def test_maybe_cartesian_from_degrees(self):
        c = cesiumpy.entities.cartesian.Cartesian2.maybe((0, 10), degrees=True)
        exp = "Cesium.Cartesian2.fromDegrees(0.0, 10.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian3.maybe((0, 10, 20), degrees=True)
        exp = "Cesium.Cartesian3.fromDegrees(0.0, 10.0, 20.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian4.maybe((0, 10, 20, 30), degrees=True)
        exp = "Cesium.Cartesian4.fromDegrees(0.0, 10.0, 20.0, 30.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian2.maybe([0, 10], degrees=True)
        exp = "Cesium.Cartesian2.fromDegrees(0.0, 10.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian3.maybe([0, 10, 20], degrees=True)
        exp = "Cesium.Cartesian3.fromDegrees(0.0, 10.0, 20.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.entities.cartesian.Cartesian4.maybe([0, 10, 20, 30], degrees=True)
        exp = "Cesium.Cartesian4.fromDegrees(0.0, 10.0, 20.0, 30.0)"
        self.assertEqual(c.script, exp)

        # do not convert
        res = cartesian.Cartesian3.maybe(3, degrees=True)
        self.assertEqual(res, 3)

        res = cartesian.Cartesian3.maybe((1, 2, 3, 5, 5), degrees=True)
        self.assertEqual(res, [1, 2, 3, 5, 5])

    def test_rectangle(self):
        c = cartesian.Rectangle(5, 10, 20, 30)
        exp = "new Cesium.Rectangle(5.0, 10.0, 20.0, 30.0)"
        self.assertEqual(c.script, exp)

        c = cartesian.Rectangle.fromDegrees(5, 10, 20, 30)
        exp = "Cesium.Rectangle.fromDegrees(5.0, 10.0, 20.0, 30.0)"
        self.assertEqual(c.script, exp)

        msg = "west must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cartesian.Rectangle.fromDegrees(200, 10, 20, 50)

        msg = "south must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cartesian.Rectangle.fromDegrees(50, 100, 20, 50)

        msg = "east must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cartesian.Rectangle.fromDegrees(10, 10, -190, 50)

        msg = "north must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cartesian.Rectangle.fromDegrees(50, 20, 20, -100)

    def test_rectangle_repr(self):
        c = cartesian.Rectangle(5, 10, 20, 30)
        exp = "Rectangle(west=5.0, south=10.0, east=20.0, north=30.0)"
        self.assertEqual(repr(c), exp)

        c = cartesian.Rectangle.fromDegrees(5, 10, 20, 30)
        exp = "Rectangle.fromDegrees(west=5.0, south=10.0, east=20.0, north=30.0)"
        self.assertEqual(repr(c), exp)


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
