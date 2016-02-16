#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import cesiumpy


class TestModel(unittest.TestCase):

    def test_basic_model(self):
        m = cesiumpy.Model('xxx.gltf', modelMatrix=(-100, 40, 0), scale=200)
        self.assertEqual(repr(m), """Model("xxx.gltf")""")
        exp = """Cesium.Model.fromGltf({url : "xxx.gltf", modelMatrix : Cesium.Transforms.eastNorthUpToFixedFrame(Cesium.Cartesian3.fromDegrees(-100.0, 40.0, 0.0)), scale : 200.0})"""
        self.assertEqual(m.script, exp)


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
