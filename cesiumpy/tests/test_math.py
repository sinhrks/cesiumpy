#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import math

import cesiumpy


class TestMath(unittest.TestCase):

    def test_constant(self):
        # check constant can be loaded from root namespace
        pi = cesiumpy.math.PI
        self.assertEqual(pi, math.pi)

        rad = cesiumpy.math.RADIANS_PER_DEGREE
        self.assertEqual(rad, math.pi / 180.0)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
