#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import cesiumpy


class TestColor(unittest.TestCase):

    def test_maybe_color(self):
        blue = cesiumpy.color._maybe_color('blue')
        exp = "Cesium.Color.BLUE"
        self.assertEqual(repr(blue), exp)

        red = cesiumpy.color._maybe_color('RED')
        exp = "Cesium.Color.RED"
        self.assertEqual(repr(red), exp)

        # do not convert
        red = cesiumpy.color._maybe_color('NamedColor')
        exp = "NamedColor"
        self.assertEqual(red, exp)

        red = cesiumpy.color._maybe_color('x')
        exp = "x"
        self.assertEqual(red, exp)

        red = cesiumpy.color._maybe_color(1)
        exp = 1
        self.assertEqual(red, exp)

    def test_numeric_colors(self):
        c = cesiumpy.color.Color(1, 2, 3)
        exp = "Cesium.Color(1, 2, 3)"
        self.assertEqual(repr(c), exp)
        self.assertEqual(c.red, 1)
        self.assertEqual(c.green, 2)
        self.assertEqual(c.blue, 3)

    def test_named_colors(self):
        aqua = cesiumpy.color.AQUA
        exp = "Cesium.Color.AQUA"
        self.assertEqual(repr(aqua), exp)
        self.assertEqual(aqua.name, 'AQUA')

        aqua = aqua.set_alpha(0.5)
        exp = "Cesium.Color.AQUA.withAlpha(0.5)"
        self.assertEqual(repr(aqua), exp)
        self.assertEqual(aqua.name, 'AQUA')

        # confirm set_alpha modifies the constant
        aqua = cesiumpy.color.AQUA
        exp = "Cesium.Color.AQUA"
        self.assertEqual(repr(aqua), exp)
        self.assertEqual(aqua.name, 'AQUA')

        blue = cesiumpy.color.BLUE
        exp = "Cesium.Color.BLUE"
        self.assertEqual(repr(blue), exp)
        self.assertEqual(blue.name, 'BLUE')

    def test_named_colors_constant(self):
        aqua = cesiumpy.color.AQUA

        with nose.tools.assert_raises(AttributeError):
            aqua.name = 'XXX'



if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
