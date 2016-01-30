#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import traitlets

import cesiumpy


class TestColor(unittest.TestCase):

    def test_maybe_color(self):
        blue = cesiumpy.entities.color._maybe_color('blue')
        exp = "Color.BLUE"
        self.assertEqual(repr(blue), exp)
        exp = "Cesium.Color.BLUE"
        self.assertEqual(blue.script, exp)

        red = cesiumpy.entities.color._maybe_color('RED')
        exp = "Color.RED"
        self.assertEqual(repr(red), exp)
        exp = "Cesium.Color.RED"
        self.assertEqual(red.script, exp)

        # do not convert
        red = cesiumpy.entities.color._maybe_color('NamedColor')
        exp = "NamedColor"
        self.assertEqual(red, exp)

        red = cesiumpy.entities.color._maybe_color('x')
        exp = "x"
        self.assertEqual(red, exp)

        red = cesiumpy.entities.color._maybe_color(1)
        exp = 1
        self.assertEqual(red, exp)

    def test_numeric_colors(self):
        c = cesiumpy.color.Color(1, 2, 3)
        exp = "Color(1, 2, 3)"
        self.assertEqual(repr(c), exp)
        self.assertEqual(c.red, 1)
        self.assertEqual(c.green, 2)
        self.assertEqual(c.blue, 3)

        exp = "Cesium.Color(1, 2, 3)"
        self.assertEqual(c.script, exp)

    def test_named_colors(self):
        aqua = cesiumpy.color.AQUA
        exp = "Color.AQUA"
        self.assertEqual(repr(aqua), exp)
        self.assertEqual(aqua.name, 'AQUA')
        exp = "Cesium.Color.AQUA"
        self.assertEqual(aqua.script, exp)

        aqua = aqua.set_alpha(0.5)
        exp = "Color.AQUA.withAlpha(0.5)"
        self.assertEqual(repr(aqua), exp)
        self.assertEqual(aqua.name, 'AQUA')
        exp = "Cesium.Color.AQUA.withAlpha(0.5)"
        self.assertEqual(aqua.script, exp)

        # confirm set_alpha modifies the constant
        aqua = cesiumpy.color.AQUA
        exp = "Color.AQUA"
        self.assertEqual(repr(aqua), exp)
        self.assertEqual(aqua.name, 'AQUA')
        exp = "Cesium.Color.AQUA"
        self.assertEqual(aqua.script, exp)

        blue = cesiumpy.color.BLUE
        exp = "Color.BLUE"
        self.assertEqual(repr(blue), exp)
        self.assertEqual(blue.name, 'BLUE')
        exp = "Cesium.Color.BLUE"
        self.assertEqual(blue.script, exp)

    def test_named_colors_constant(self):
        aqua = cesiumpy.color.AQUA

        with nose.tools.assert_raises(AttributeError):
            aqua.name = 'XXX'

    def test_single_char_color(self):
        _m = cesiumpy.entities.color._maybe_color
        self.assertEqual(_m('b'), cesiumpy.color.BLUE)
        self.assertEqual(_m('g'), cesiumpy.color.GREEN)
        self.assertEqual(_m('r'), cesiumpy.color.RED)
        self.assertEqual(_m('c'), cesiumpy.color.CYAN)
        self.assertEqual(_m('m'), cesiumpy.color.MAGENTA)
        self.assertEqual(_m('y'), cesiumpy.color.YELLOW)
        self.assertEqual(_m('k'), cesiumpy.color.BLACK)
        self.assertEqual(_m('w'), cesiumpy.color.WHITE)

        self.assertEqual(_m('B'), cesiumpy.color.BLUE)
        self.assertEqual(_m('G'), cesiumpy.color.GREEN)
        self.assertEqual(_m('R'), cesiumpy.color.RED)
        self.assertEqual(_m('C'), cesiumpy.color.CYAN)
        self.assertEqual(_m('M'), cesiumpy.color.MAGENTA)
        self.assertEqual(_m('Y'), cesiumpy.color.YELLOW)
        self.assertEqual(_m('K'), cesiumpy.color.BLACK)
        self.assertEqual(_m('W'), cesiumpy.color.WHITE)

    def test_alpha(self):
        aqua = cesiumpy.color.AQUA

        res = aqua.set_alpha(0.3)
        exp = "Cesium.Color.AQUA.withAlpha(0.3)"
        self.assertEqual(res.script, exp)

        res = aqua.withAlpha(0.3)
        exp = "Cesium.Color.AQUA.withAlpha(0.3)"
        self.assertEqual(res.script, exp)

        res = aqua.withAlpha(1.0)
        exp = "Cesium.Color.AQUA.withAlpha(1.0)"
        self.assertEqual(res.script, exp)

        res = aqua.withAlpha(0.0)
        exp = "Cesium.Color.AQUA.withAlpha(0.0)"
        self.assertEqual(res.script, exp)

        msg = "The value of the '_alpha' trait of a NamedColor instance should be between"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            aqua.withAlpha(1.1)

if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
