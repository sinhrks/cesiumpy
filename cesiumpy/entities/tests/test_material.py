#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import re

import cesiumpy
import cesiumpy.testing as tm


class TestImageMaterial(unittest.TestCase):

    def test_imagematerial(self):
        m = cesiumpy.entities.material.ImageMaterialProperty('xxx.png')
        self.assertEqual(repr(m), 'ImageMaterialProperty(xxx.png)')
        self.assertEqual(m.script, """new Cesium.ImageMaterialProperty({image : "xxx.png"})""")


class TestTempImageMaterial(unittest.TestCase):

    def test_matplotlibimage(self):
        tm._skip_if_no_matplotlib()

        import numpy as np
        import matplotlib.pyplot as plt

        img = np.random.randint(0, 255, (100, 100, 3))
        ax = plt.imshow(img)
        img = cesiumpy.entities.material.TemporaryImage(ax.figure)
        m = cesiumpy.entities.material.ImageMaterialProperty(img)
        self.assertTrue(re.match("""new Cesium\\.ImageMaterialProperty\\({image : "\w+\\.png"}\\)""", m.script))

        img = cesiumpy.entities.material.TemporaryImage(ax)
        m = cesiumpy.entities.material.ImageMaterialProperty(img)
        self.assertTrue(re.match("""new Cesium\\.ImageMaterialProperty\\({image : "\w+\\.png"}\\)""", m.script))
        plt.close()

        fig, axes = plt.subplots(2, 2)
        msg = "Unable to trim a Figure contains multiple Axes"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            img = cesiumpy.entities.material.TemporaryImage(fig)
            cesiumpy.entities.material.ImageMaterialProperty(img)
        plt.close()

if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
