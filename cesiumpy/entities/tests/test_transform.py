#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import cesiumpy


class TestTransform(unittest.TestCase):

    def test_transform(self):
        c = cesiumpy.Cartesian3(1, 1, 1)
        res = cesiumpy.Transforms.eastNorthUpToFixedFrame(c)
        exp = """Cesium.Transforms.eastNorthUpToFixedFrame(new Cesium.Cartesian3(1.0, 1.0, 1.0))"""
        self.assertEqual(res.script, exp)

        res = cesiumpy.Transforms.northEastDownToFixedFrame(c)
        exp = """Cesium.Transforms.northEastDownToFixedFrame(new Cesium.Cartesian3(1.0, 1.0, 1.0))"""
        self.assertEqual(res.script, exp)

        res = cesiumpy.Transforms.northUpEastToFixedFrame(c)
        exp = """Cesium.Transforms.northUpEastToFixedFrame(new Cesium.Cartesian3(1.0, 1.0, 1.0))"""
        self.assertEqual(res.script, exp)


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
