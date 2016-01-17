#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import traitlets

import cesiumpy


class TestImageMaterial(unittest.TestCase):

    def test_imagematerial(self):
        m = cesiumpy.entities.material.ImageMaterialProperty('xxx.png')
        self.assertEqual(repr(m), 'ImageMaterialProperty(xxx.png)')
        self.assertEqual(m.script, """new Cesium.ImageMaterialProperty({image : "xxx.png"})""")


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
