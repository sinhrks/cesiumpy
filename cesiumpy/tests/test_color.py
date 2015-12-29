#!/usr/bin/env python
# coding: utf-8

# do not import unicode_literals here to test ASCII in Python 2.7

import nose
import unittest

import cesiumpy


class TestColor(unittest.TestCase):

    def test_named_colors(self):
        aqua = cesiumpy.color.AQUA
        exp = "Cesium.Color.AQUA"
        self.assertEqual(repr(aqua), exp)

        aqua = aqua.set_alpha(0.5)
        exp = "Cesium.Color.AQUA.withAlpha(0.5)"
        self.assertEqual(repr(aqua), exp)

        # confirm set_alpha modifies the constant
        aqua = cesiumpy.color.AQUA
        exp = "Cesium.Color.AQUA"
        self.assertEqual(repr(aqua), exp)

    def test_named_colors_constant(self):
        aqua = cesiumpy.color.AQUA

        with nose.tools.assert_raises(AttributeError):
            aqua.name = 'XXX'



if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
