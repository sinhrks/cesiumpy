#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import cesiumpy



class TestTerrainProvider(unittest.TestCase):

    def test_provider_klass(self):
        url = 'x'

        self.assertEqual(cesiumpy.TerrainProvider(url=url)._klass,
                         "Cesium.TerrainProvider")

        self.assertEqual(cesiumpy.ArcGisImageServerTerrainProvider(url=url)._klass,
                         "Cesium.ArcGisImageServerTerrainProvider")
        self.assertEqual(cesiumpy.CesiumTerrainProvider(url=url)._klass,
                         "Cesium.CesiumTerrainProvider")
        self.assertEqual(cesiumpy.EllipsoidTerrainProvider(url=url)._klass,
                         "Cesium.EllipsoidTerrainProvider")
        self.assertEqual(cesiumpy.VRTheWorldTerrainProvider(url=url)._klass,
                         "Cesium.VRTheWorldTerrainProvider")



class TestImageProvider(unittest.TestCase):

    def test_provider_klass(self):
        url = 'x'


        self.assertEqual(cesiumpy.ImageryProvider(url=url)._klass,
                         "Cesium.ImageryProvider")

        self.assertEqual(cesiumpy.ArcGisMapServerImageryProvider(url=url)._klass,
                         "Cesium.ArcGisMapServerImageryProvider")
        self.assertEqual(cesiumpy.BingMapsImageryProvider(url=url)._klass,
                         "Cesium.BingMapsImageryProvider")
        self.assertEqual(cesiumpy.GoogleEarthImageryProvider(url=url)._klass,
                         "Cesium.GoogleEarthImageryProvider")
        self.assertEqual(cesiumpy.GoogleEarthImageryProvider(url=url)._klass,
                         "Cesium.GoogleEarthImageryProvider")
        self.assertEqual(cesiumpy.GridImageryProvider(url=url)._klass,
                         "Cesium.GridImageryProvider")
        self.assertEqual(cesiumpy.MapboxImageryProvider(url=url)._klass,
                         "Cesium.MapboxImageryProvider")
        self.assertEqual(cesiumpy.SingleTileImageryProvider(url=url)._klass,
                         "Cesium.SingleTileImageryProvider")
        self.assertEqual(cesiumpy.TileCoordinatesImageryProvider(url=url)._klass,
                         "Cesium.TileCoordinatesImageryProvider")
        self.assertEqual(cesiumpy.TileMapServiceImageryProvider(url=url)._klass,
                         "Cesium.TileMapServiceImageryProvider")
        self.assertEqual(cesiumpy.UrlTemplateImageryProvider(url=url)._klass,
                         "Cesium.UrlTemplateImageryProvider")
        self.assertEqual(cesiumpy.WebMapServiceImageryProvider(url=url)._klass,
                         "Cesium.WebMapServiceImageryProvider")
        self.assertEqual(cesiumpy.WebMapTileServiceImageryProvider(url=url)._klass,
                         "Cesium.WebMapTileServiceImageryProvider")



if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
