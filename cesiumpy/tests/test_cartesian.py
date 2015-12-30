#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import cesiumpy


class TestCartesian(unittest.TestCase):

    def test_cartesian2(self):
        c = cesiumpy.Cartesian2(5, 10)
        exp = "new Cesium.Cartesian2(5, 10)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian2.fromDegrees(5, 10)
        exp = "Cesium.Cartesian2.fromDegrees(5, 10)"
        self.assertEqual(repr(c), exp)

        msg = "x must be longtitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian2.fromDegrees(200, 10)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian2.fromDegrees(50, 100)

    def test_cartesian3(self):
        c = cesiumpy.Cartesian3(5, 10, 20)
        exp = "new Cesium.Cartesian3(5, 10, 20)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian3.fromDegrees(5, 10, 20)
        exp = "Cesium.Cartesian3.fromDegrees(5, 10, 20)"
        self.assertEqual(repr(c), exp)

        msg = "x must be longtitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegrees(200, 10, 20)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegrees(50, 100, 20)

    def test_cartesian3_array(self):
        c = cesiumpy.Cartesian3.fromDegreesArray([1, 2, 3, 4])
        exp = "Cesium.Cartesian3.fromDegreesArray([1, 2, 3, 4])"
        self.assertEqual(repr(c), exp)

        msg = "input must be a list"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray(1)

        msg = "input length must be even number: \\[1, 2, 3\\]"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray([1, 2, 3])

        msg = "input must be a list consists from longtitude and latitude"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray([10, 20, 200, 20])

        msg = "input must be a list consists from longtitude and latitude"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray([10, 20, 20, 91])

    def test_cartesian4(self):
        c = cesiumpy.Cartesian4(5, 10, 20, 30)
        exp = "new Cesium.Cartesian4(5, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian4.fromDegrees(5, 10, 20, 30)
        exp = "Cesium.Cartesian4.fromDegrees(5, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        msg = "x must be longtitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian4.fromDegrees(200, 10, 20, 50)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian4.fromDegrees(50, 100, 20, 50)

    def test_maybe_cartesian(self):
        c = cesiumpy.cartesian._maybe_cartesian((0, 10))
        exp = "new Cesium.Cartesian2(0, 10)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian((0, 10, 20))
        exp = "new Cesium.Cartesian3(0, 10, 20)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian((0, 10, 20, 30))
        exp = "new Cesium.Cartesian4(0, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian([0, 10])
        exp = "new Cesium.Cartesian2(0, 10)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian([0, 10, 20])
        exp = "new Cesium.Cartesian3(0, 10, 20)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian([0, 10, 20, 30])
        exp = "new Cesium.Cartesian4(0, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        msg = "unable to convert input to Cartesian"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian(3)

        msg = "length must be 2-4 to be converted to Cartesian"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian((1, 2, 3, 5, 5))

    def test_maybe_cartesian_from_degrees(self):
        c = cesiumpy.cartesian._maybe_cartesian_degrees((0, 10))
        exp = "Cesium.Cartesian2.fromDegrees(0, 10)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian_degrees((0, 10, 20))
        exp = "Cesium.Cartesian3.fromDegrees(0, 10, 20)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian_degrees((0, 10, 20, 30))
        exp = "Cesium.Cartesian4.fromDegrees(0, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian_degrees([0, 10])
        exp = "Cesium.Cartesian2.fromDegrees(0, 10)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian_degrees([0, 10, 20])
        exp = "Cesium.Cartesian3.fromDegrees(0, 10, 20)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian_degrees([0, 10, 20, 30])
        exp = "Cesium.Cartesian4.fromDegrees(0, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        msg = "unable to convert input to Cartesian"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian_degrees(3)

        msg = "length must be 2-4 to be converted to Cartesian"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian_degrees((1, 2, 3, 5, 5))

if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
