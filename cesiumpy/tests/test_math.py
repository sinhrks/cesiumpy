#!/usr/bin/env python
# coding: utf-8

import nose
import unittest


import cesiumpy


class TestMath(unittest.TestCase):

    def test_constant(self):
        # check constant can be loaded from root namespace
        pi = cesiumpy.Math.PI
        self.assertEqual(pi.script, 'Cesium.Math.PI')

        rad = cesiumpy.Math.RADIANS_PER_DEGREE
        self.assertEqual(rad.script, 'Cesium.Math.RADIANS_PER_DEGREE')


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
