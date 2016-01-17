#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import re
import traitlets

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
        m = cesiumpy.entities.material.TemporaryImageMaterialProperty(ax.figure)
        self.assertTrue(re.match("""new Cesium\\.ImageMaterialProperty\\({image : "\w+\\.png"}\\)""", m.script))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
