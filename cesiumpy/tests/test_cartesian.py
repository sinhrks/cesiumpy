#!/usr/bin/env python
# coding: utf-8

# do not import unicode_literals here to test ASCII in Python 2.7

import unittest
import nose

import cesiumpy


class TestCartesian(unittest.TestCase):

    def test_cartesian2(self):
        c = cesiumpy.Cartesian2(5, 10)
        exp = "Cesium.Cartesian2.fromDegrees(5, 10)"
        self.assertEqual(repr(c), exp)

    def test_cartesian3(self):
        c = cesiumpy.Cartesian3(5, 10, 20)
        exp = "Cesium.Cartesian3.fromDegrees(5, 10, 20)"
        self.assertEqual(repr(c), exp)

    def test_cartesian4(self):
        c = cesiumpy.Cartesian4(5, 10, 20, 30)
        exp = "Cesium.Cartesian4.fromDegrees(5, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

    def test_maybe_cartesian(self):
        c = cesiumpy.cartesian._maybe_cartesian((0, 10))
        exp = "Cesium.Cartesian2.fromDegrees(0, 10)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian((0, 10, 20))
        exp = "Cesium.Cartesian3.fromDegrees(0, 10, 20)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian((0, 10, 20, 30))
        exp = "Cesium.Cartesian4.fromDegrees(0, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian([0, 10])
        exp = "Cesium.Cartesian2.fromDegrees(0, 10)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian([0, 10, 20])
        exp = "Cesium.Cartesian3.fromDegrees(0, 10, 20)"
        self.assertEqual(repr(c), exp)

        c = cesiumpy.cartesian._maybe_cartesian([0, 10, 20, 30])
        exp = "Cesium.Cartesian4.fromDegrees(0, 10, 20, 30)"
        self.assertEqual(repr(c), exp)

        msg = "unable to convert input to Cartesian"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian(3)

        msg = "length must be 2-4 to be converted to Cartesian"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.cartesian._maybe_cartesian((1, 2, 3, 5, 5))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
