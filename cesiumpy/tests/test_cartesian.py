#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import cesiumpy


class TestCartesian(unittest.TestCase):

    def test_cartesian2(self):
        c = cesiumpy.Cartesian2(5, 10)
        exp = "new Cesium.Cartesian2(5, 10)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.Cartesian2.fromDegrees(5, 10)
        exp = "Cesium.Cartesian2.fromDegrees(5, 10)"
        self.assertEqual(c.script, exp)

        msg = "x must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian2.fromDegrees(200, 10)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian2.fromDegrees(50, 100)

    def test_cartesian2_repr(self):
        c = cesiumpy.Cartesian2(5, 10)
        exp = "Cartesian2(5, 10)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian2.fromDegrees(5, 10)
        exp = "Cartesian2.fromDegrees(5, 10)"
        self.assertEqual(repr(c), exp)

    def test_cartesian3(self):
        c = cesiumpy.Cartesian3(5, 10, 20)
        exp = "new Cesium.Cartesian3(5, 10, 20)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.Cartesian3.fromDegrees(5, 10, 20)
        exp = "Cesium.Cartesian3.fromDegrees(5, 10, 20)"
        self.assertEqual(c.script, exp)

        msg = "x must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegrees(200, 10, 20)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegrees(50, 100, 20)

    def test_cartesian3_repr(self):
        c = cesiumpy.Cartesian3(5, 10, 20)
        exp = "Cartesian3(5, 10, 20)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian3.fromDegrees(5, 10, 20)
        exp = "Cartesian3.fromDegrees(5, 10, 20)"
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
            cesiumpy.Cartesian3.fromDegreesArray([('X', 20), (20, 20)])

        msg = "x must be a list consists from longitude and latitude"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian3.fromDegreesArray([10, 20, 20, 91])

    def test_cartesian4(self):
        c = cesiumpy.Cartesian4(5, 10, 20, 30)
        exp = "new Cesium.Cartesian4(5, 10, 20, 30)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.Cartesian4.fromDegrees(5, 10, 20, 30)
        exp = "Cesium.Cartesian4.fromDegrees(5, 10, 20, 30)"
        self.assertEqual(c.script, exp)

        msg = "x must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian4.fromDegrees(200, 10, 20, 50)

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Cartesian4.fromDegrees(50, 100, 20, 50)

    def test_cartesian4_repr(self):
        c = cesiumpy.Cartesian4(5, 10, 20, 30)
        exp = "Cartesian4(5, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.Cartesian4.fromDegrees(5, 10, 20, 30)
        exp = "Cartesian4.fromDegrees(5, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

    def test_maybe_cartesian(self):
        c = cesiumpy.cartesian._maybe_cartesian2((0, 10), key='x')
        exp = "new Cesium.Cartesian2(0, 10)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian3((0, 10, 20), key='x')
        exp = "new Cesium.Cartesian3(0, 10, 20)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian4((0, 10, 20, 30), key='x')
        exp = "new Cesium.Cartesian4(0, 10, 20, 30)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian2([0, 10], key='x')
        exp = "new Cesium.Cartesian2(0, 10)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian3([0, 10, 20], key='x')
        exp = "new Cesium.Cartesian3(0, 10, 20)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian4([0, 10, 20, 30], key='x')
        exp = "new Cesium.Cartesian4(0, 10, 20, 30)"
        self.assertEqual(c.script, exp)

        msg = "x must be list-likes: 3"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian2(3, key='x')

        msg = "x length must be 2 to be converted to Cartesian2:"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian2((1, 2, 3, 5, 5), key='x')

    def test_maybe_cartesian_from_degrees(self):
        c = cesiumpy.cartesian._maybe_cartesian2((0, 10), key='x', degrees=True)
        exp = "Cesium.Cartesian2.fromDegrees(0, 10)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian3((0, 10, 20), key='x', degrees=True)
        exp = "Cesium.Cartesian3.fromDegrees(0, 10, 20)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian4((0, 10, 20, 30), key='x', degrees=True)
        exp = "Cesium.Cartesian4.fromDegrees(0, 10, 20, 30)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian2([0, 10], key='x', degrees=True)
        exp = "Cesium.Cartesian2.fromDegrees(0, 10)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian3([0, 10, 20], key='x', degrees=True)
        exp = "Cesium.Cartesian3.fromDegrees(0, 10, 20)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian._maybe_cartesian4([0, 10, 20, 30], key='x', degrees=True)
        exp = "Cesium.Cartesian4.fromDegrees(0, 10, 20, 30)"
        self.assertEqual(c.script, exp)

        msg = "x must be list-likes: 3"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian3(3, key='x', degrees=True)

        msg = "x length must be 3 to be converted to Cartesian3:"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian3((1, 2, 3, 5, 5), key='x', degrees=True)


    def test_rectangle(self):
        c = cesiumpy.cartesian.Rectangle(5, 10, 20, 30)
        exp = "new Cesium.Rectangle(5, 10, 20, 30)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.cartesian.Rectangle.fromDegrees(5, 10, 20, 30)
        exp = "Cesium.Rectangle.fromDegrees(5, 10, 20, 30)"
        self.assertEqual(c.script, exp)

        msg = "west must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian.Rectangle.fromDegrees(200, 10, 20, 50)

        msg = "south must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian.Rectangle.fromDegrees(50, 100, 20, 50)

        msg = "east must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian.Rectangle.fromDegrees(10, 10, -190, 50)

        msg = "north must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian.Rectangle.fromDegrees(50, 20, 20, -100)

    def test_rectangle_repr(self):
        c = cesiumpy.cartesian.Rectangle(5, 10, 20, 30)
        exp = "Rectangle(west=5, south=10, east=20, north=30)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian.Rectangle.fromDegrees(5, 10, 20, 30)
        exp = "Rectangle.fromDegrees(west=5, south=10, east=20, north=30)"
        self.assertEqual(repr(c), exp)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
