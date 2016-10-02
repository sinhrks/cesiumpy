#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import traitlets

import cesiumpy
import cesiumpy.testing as tm


class TestColor(unittest.TestCase):

    def test_maybe_color(self):
        blue = cesiumpy.color.Color.maybe('blue')
        self.assertEqual(repr(blue), "Color.BLUE")
        self.assertEqual(blue.script, "Cesium.Color.BLUE")

        red = cesiumpy.color.Color.maybe('RED')
        self.assertEqual(repr(red), "Color.RED")
        self.assertEqual(red.script, "Cesium.Color.RED")

        msg = "Unable to convert to Color instance: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.color.Color.maybe('NamedColor')

        msg = "Unable to convert to Color instance: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.color.Color.maybe('x')

        msg = "Unable to convert to Color instance: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.color.Color.maybe(1)

    def test_maybe_color_listlike(self):
        # tuple
        c = cesiumpy.color.Color.maybe((0.5, 0.3, 0.5))
        self.assertEqual(repr(c), "Color(0.5, 0.3, 0.5)")
        self.assertEqual(c.script, "new Cesium.Color(0.5, 0.3, 0.5)")

        c = cesiumpy.color.Color.maybe((0.5, 0.3, 0.5, 0.2))
        self.assertEqual(repr(c), "Color(0.5, 0.3, 0.5, 0.2)")
        self.assertEqual(c.script, "new Cesium.Color(0.5, 0.3, 0.5, 0.2)")

        # do not convert
        msg = "Unable to convert to Color instance: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.color.Color.maybe((0.5, 0.3))

        msg = "Unable to convert to Color instance: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.color.Color.maybe((0.5, 0.3, 0.2, 0.1, 0.5))

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

    def test_single_char_color(self):
        _m = cesiumpy.color.Color.maybe
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

        msg = "The value of the 'alpha' trait of a ColorConstant instance should"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            aqua.withAlpha(1.1)

    def test_rgb(self):
        c = cesiumpy.color.Color(1, 0, 0)
        exp = "new Cesium.Color(1.0, 0.0, 0.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.color.Color(1, 0, 0, 0.5)
        exp = "new Cesium.Color(1.0, 0.0, 0.0, 0.5)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.color.Color.fromBytes(255, 0, 255)
        exp = "new Cesium.Color(1.0, 0.0, 1.0)"
        self.assertEqual(c.script, exp)

        c = cesiumpy.color.Color.fromBytes(255, 0, 255, 255)
        exp = "new Cesium.Color(1.0, 0.0, 1.0, 1.0)"
        self.assertEqual(c.script, exp)

    def test_color_string(self):
        c = cesiumpy.color.Color.fromString('#FF0000')
        exp = """Cesium.Color.fromCssColorString("#FF0000")"""
        self.assertEqual(c.script, exp)

    def test_random(self):
        c = cesiumpy.color.choice()
        self.assertIsInstance(c, cesiumpy.color.Color)

        colors = cesiumpy.color.sample(5)
        self.assertIsInstance(colors, list)
        self.assertEqual(len(colors), 5)
        self.assertTrue(all(isinstance(c, cesiumpy.color.Color) for c in colors))

    def test_cmap(self):
        tm._skip_if_no_matplotlib()
        import matplotlib.pyplot as plt

        mpl_cmap = plt.get_cmap('winter')
        cmap = cesiumpy.color.get_cmap('winter')

        exp = """ColorMap("winter")"""
        self.assertEqual(repr(cmap), exp)

        res = cmap(3)
        exp = mpl_cmap(3)
        self.assertEqual(res.red, exp[0])
        self.assertEqual(res.green, exp[1])
        self.assertEqual(res.blue, exp[2])
        self.assertEqual(res.alpha, exp[3])

        res = cmap([2, 4])
        exp = mpl_cmap([2, 4])
        for r, e in zip(res, exp):
            self.assertEqual(r.red, e[0])
            self.assertEqual(r.green, e[1])
            self.assertEqual(r.blue, e[2])
            self.assertEqual(r.alpha, e[3])


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
