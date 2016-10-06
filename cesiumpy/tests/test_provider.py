#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import re
import traitlets

import cesiumpy
import cesiumpy.testing as tm


class TestTerrainProvider(unittest.TestCase):

    def test_provider_klass(self):
        url = 'x'

        self.assertEqual(cesiumpy.TerrainProvider(url=url)._klass,
                         "Cesium.TerrainProvider")

        self.assertEqual(cesiumpy.ArcGisImageServerTerrainProvider(url=url, token='DUMMY')._klass,
                         "Cesium.ArcGisImageServerTerrainProvider")
        self.assertEqual(cesiumpy.CesiumTerrainProvider(url=url)._klass,
                         "Cesium.CesiumTerrainProvider")
        self.assertEqual(cesiumpy.EllipsoidTerrainProvider()._klass,
                         "Cesium.EllipsoidTerrainProvider")
        self.assertEqual(cesiumpy.VRTheWorldTerrainProvider(url=url)._klass,
                         "Cesium.VRTheWorldTerrainProvider")

    def test_viewer(self):
        url = 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer'
        imageryProvider = cesiumpy.ArcGisMapServerImageryProvider(url=url)
        v = cesiumpy.Viewer(divid='viewertest', imageryProvider=imageryProvider)
        result = v.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest", {baseLayerPicker : false, imageryProvider : new Cesium.ArcGisMapServerImageryProvider({url : "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"})});
</script>"""
        self.assertEqual(result, exp)

    def test_CesiumTerrainProvider(self):
        url = '//assets.agi.com/stk-terrain/world'
        terrainProvider = cesiumpy.CesiumTerrainProvider(url=url)
        result = terrainProvider.script
        exp = """new Cesium.CesiumTerrainProvider({url : "//assets.agi.com/stk-terrain/world"})"""
        self.assertEqual(result, exp)

        terrainProvider = cesiumpy.CesiumTerrainProvider(url=url, requestWaterMask=True)
        result = terrainProvider.script
        exp = """new Cesium.CesiumTerrainProvider({url : "//assets.agi.com/stk-terrain/world", requestWaterMask : true})"""
        self.assertEqual(result, exp)

        terrainProvider = cesiumpy.CesiumTerrainProvider(url=url, requestWaterMask=True, requestVertexNormals=True)
        result = terrainProvider.script
        exp = """new Cesium.CesiumTerrainProvider({url : "//assets.agi.com/stk-terrain/world", requestVertexNormals : true, requestWaterMask : true})"""
        self.assertEqual(result, exp)

        msg = "The 'url' trait of a CesiumTerrainProvider instance must be a unicode string"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.CesiumTerrainProvider(url=1)

        msg = "The 'requestWaterMask' trait of a CesiumTerrainProvider instance must be a boolean"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.CesiumTerrainProvider(url=url, requestWaterMask=1)

        msg = "The 'requestVertexNormals' trait of a CesiumTerrainProvider instance must be a boolean"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.CesiumTerrainProvider(url=url, requestVertexNormals=1)

    def test_EllipsoidTerrainProvider(self):
        terrainProvider = cesiumpy.EllipsoidTerrainProvider()
        result = terrainProvider.script
        exp = """new Cesium.EllipsoidTerrainProvider()"""
        self.assertEqual(result, exp)

    def test_EllipsoidTerrainProvider_repr(self):
        terrainProvider = cesiumpy.EllipsoidTerrainProvider()
        exp = """<cesiumpy.provider.EllipsoidTerrainProvider"""
        self.assertTrue(repr(terrainProvider).startswith(exp))

    def test_VRTheWorldTerrainProvider(self):
        url = '//www.vr-theworld.com/vr-theworld/tiles1.0.0/73/'
        credit = 'Terrain data courtesy VT MAK'

        terrainProvider = cesiumpy.VRTheWorldTerrainProvider(url=url, credit=credit)
        result = terrainProvider.script
        exp = """new Cesium.VRTheWorldTerrainProvider({url : "//www.vr-theworld.com/vr-theworld/tiles1.0.0/73/", credit : "Terrain data courtesy VT MAK"})"""
        self.assertEqual(result, exp)


class TestImageProvider(unittest.TestCase):

    def test_provider_klass(self):
        url = 'x'

        self.assertEqual(cesiumpy.ImageryProvider(url=url)._klass,
                         "Cesium.ImageryProvider")

        self.assertEqual(cesiumpy.ArcGisMapServerImageryProvider(url=url)._klass,
                         "Cesium.ArcGisMapServerImageryProvider")
        self.assertEqual(cesiumpy.BingMapsImageryProvider(url=url, key='xx', tileProtocol='xx')._klass,
                         "Cesium.BingMapsImageryProvider")
        self.assertEqual(cesiumpy.GoogleEarthImageryProvider(url=url, channel=1)._klass,
                         "Cesium.GoogleEarthImageryProvider")
        # Not Implemented
        # self.assertEqual(cesiumpy.GridImageryProvider(url=url)._klass,
        #                  "Cesium.GridImageryProvider")
        self.assertEqual(cesiumpy.MapboxImageryProvider(url=url, mapId='xx', accessToken='xx')._klass,
                         "Cesium.MapboxImageryProvider")
        self.assertEqual(cesiumpy.OpenStreetMapImageryProvider(url=url)._klass,
                         "Cesium.OpenStreetMapImageryProvider")
        self.assertEqual(cesiumpy.SingleTileImageryProvider(url=url)._klass,
                         "Cesium.SingleTileImageryProvider")
        self.assertEqual(cesiumpy.TileCoordinatesImageryProvider()._klass,
                         "Cesium.TileCoordinatesImageryProvider")
        self.assertEqual(cesiumpy.TileMapServiceImageryProvider(url=url)._klass,
                         "Cesium.TileMapServiceImageryProvider")
        # Not Implemented
        # self.assertEqual(cesiumpy.UrlTemplateImageryProvider(url=url)._klass,
        #                  "Cesium.UrlTemplateImageryProvider")
        self.assertEqual(cesiumpy.WebMapServiceImageryProvider(url=url, layers='xx')._klass,
                         "Cesium.WebMapServiceImageryProvider")
        self.assertEqual(cesiumpy.WebMapTileServiceImageryProvider(url=url, layer='xx', style='xx')._klass,
                         "Cesium.WebMapTileServiceImageryProvider")

    def test_viewer(self):
        url = '//assets.agi.com/stk-terrain/world'
        terrainProvider = cesiumpy.CesiumTerrainProvider(url=url, requestWaterMask=True)
        v = cesiumpy.Viewer(divid='viewertest', terrainProvider=terrainProvider)
        result = v.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest", {baseLayerPicker : false, terrainProvider : new Cesium.CesiumTerrainProvider({url : "//assets.agi.com/stk-terrain/world", requestWaterMask : true})});
</script>"""
        self.assertEqual(result, exp)

    def test_ArcGisMapServerImageryProvider(self):
        url = 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer'
        imageryProvider = cesiumpy.ArcGisMapServerImageryProvider(url=url)
        result = imageryProvider.script
        exp = """new Cesium.ArcGisMapServerImageryProvider({url : "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"})"""
        self.assertEqual(result, exp)

        url = '//server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer'
        imageryProvider = cesiumpy.ArcGisMapServerImageryProvider(url=url)
        result = imageryProvider.script
        exp = """new Cesium.ArcGisMapServerImageryProvider({url : "//server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer"})"""
        self.assertEqual(result, exp)

    def test_TileMapServiceImageryProvider(self):
        url = '//cesiumjs.org/tilesets/imagery/blackmarble'
        credit = 'Black Marble imagery courtesy NASA Earth Observatory'
        imageryProvider = cesiumpy.TileMapServiceImageryProvider(url=url, maximumLevel=8, credit=credit)
        result = imageryProvider.script
        exp = """new Cesium.TileMapServiceImageryProvider({url : "//cesiumjs.org/tilesets/imagery/blackmarble", maximumLevel : 8.0, credit : "Black Marble imagery courtesy NASA Earth Observatory"})"""
        self.assertEqual(result, exp)

        # ToDo:
        """
        'Natural Earth II (local)',
        new Cesium.TileMapServiceImageryProvider({
            url : require.toUrl('Assets/Textures/NaturalEarthII')
        }));
        """

        url = '../images/cesium_maptiler/Cesium_Logo_Color'
        imageryProvider = cesiumpy.TileMapServiceImageryProvider(url=url)
        result = imageryProvider.script
        exp = """new Cesium.TileMapServiceImageryProvider({url : "../images/cesium_maptiler/Cesium_Logo_Color"})"""
        self.assertEqual(result, exp)

    def test_SingleTileImageryProvider(self):
        url = '../images/Cesium_Logo_overlay.png'
        rectangle = cesiumpy.entities.cartesian.Rectangle.fromDegrees(-75.0, 28.0, -67.0, 29.75)
        imageryProvider = cesiumpy.SingleTileImageryProvider(url=url, rectangle=rectangle)
        result = imageryProvider.script
        exp = """new Cesium.SingleTileImageryProvider({url : "../images/Cesium_Logo_overlay.png", rectangle : Cesium.Rectangle.fromDegrees(-75.0, 28.0, -67.0, 29.75)})"""
        self.assertEqual(result, exp)

        url = '../images/Cesium_Logo_overlay.png'
        rectangle = cesiumpy.entities.cartesian.Rectangle.fromDegrees(-115.0, 38.0, -107, 39.75)
        imageryProvider = cesiumpy.SingleTileImageryProvider(url=url, rectangle=rectangle)
        result = imageryProvider.script
        exp = """new Cesium.SingleTileImageryProvider({url : "../images/Cesium_Logo_overlay.png", rectangle : Cesium.Rectangle.fromDegrees(-115.0, 38.0, -107.0, 39.75)})"""
        self.assertEqual(result, exp)

    def test_SingleTimeImageryProvider_tempfile(self):
        tm._skip_if_no_matplotlib()

        import numpy as np
        import matplotlib.pyplot as plt

        img = np.random.randint(0, 255, (100, 100, 3))
        ax = plt.imshow(img)
        img = cesiumpy.entities.material.TemporaryImage(ax.figure)
        m = cesiumpy.SingleTileImageryProvider(img, rectangle=(-120.0, 40.0, -100, 60))
        self.assertTrue(re.match("""new Cesium\\.SingleTileImageryProvider\\(\\{url : "\w+\\.png", rectangle : Cesium\\.Rectangle\\.fromDegrees\\(-120\\.0, 40\\.0, -100\\.0, 60\\.0\\)\\}\\)""", m.script))
        plt.close()

    def test_BingMapsImageryProvider(self):
        """
        new Cesium.BingMapsImageryProvider({
            url: '//dev.virtualearth.net',
            mapStyle: Cesium.BingMapsStyle.ROAD
        }));
        # ToDo: NotImplemented
        """

    def test_OpenStreetMapImageryProvider(self):
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider()
        result = imageryProvider.script
        exp = """new Cesium.OpenStreetMapImageryProvider()"""
        self.assertEqual(result, exp)

        url = '//otile1-s.mqcdn.com/tiles/1.0.0/osm/'
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider(url=url)
        result = imageryProvider.script
        exp = """new Cesium.OpenStreetMapImageryProvider({url : "//otile1-s.mqcdn.com/tiles/1.0.0/osm/"})"""
        self.assertEqual(result, exp)

        url = '//stamen-tiles.a.ssl.fastly.net/watercolor/'
        credit = 'Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under CC BY SA.'
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider(url=url, credit=credit)
        result = imageryProvider.script
        exp = """new Cesium.OpenStreetMapImageryProvider({url : "//stamen-tiles.a.ssl.fastly.net/watercolor/", credit : "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under CC BY SA."})"""
        self.assertEqual(result, exp)

        imageryProvider = cesiumpy.OpenStreetMapImageryProvider(url=url, fileExtension='jpg', credit=credit)
        result = imageryProvider.script
        exp = """new Cesium.OpenStreetMapImageryProvider({url : "//stamen-tiles.a.ssl.fastly.net/watercolor/", fileExtension : "jpg", credit : "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under CC BY SA."})"""
        self.assertEqual(result, exp)

    def test_OpenStreetMapImageryProvider_repr(self):
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider()
        exp = """<cesiumpy.provider.OpenStreetMapImageryProvider"""
        self.assertTrue(repr(imageryProvider).startswith(exp))

        url = '//otile1-s.mqcdn.com/tiles/1.0.0/osm/'
        imageryProvider = cesiumpy.OpenStreetMapImageryProvider(url=url)
        exp = """OpenStreetMapImageryProvider(url="//otile1-s.mqcdn.com/tiles/1.0.0/osm/")"""
        self.assertEqual(repr(imageryProvider), exp)

    def test_WebMapServiceImageryProvider(self):
        pass

        # Not Implemented
        """
        new Cesium.WebMapServiceImageryProvider({
                url : '//mesonet.agron.iastate.edu/cgi-bin/wms/goes/conus_ir.cgi?',
                layers : 'goes_conus_ir',
                credit : 'Infrared data courtesy Iowa Environmental Mesonet',
                parameters : {
                    transparent : 'true',
                    format : 'image/png'
                },
                proxy : new Cesium.DefaultProxy('/proxy/')
            })

        new Cesium.WebMapServiceImageryProvider({
                url : '//mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi?',
                layers : 'nexrad-n0r',
                credit : 'Radar data courtesy Iowa Environmental Mesonet',
                parameters : {
                    transparent : 'true',
                    format : 'image/png'
                },
                proxy : new Cesium.DefaultProxy('/proxy/')
            })
        """

    def test_WebMapTileServiceImageryProvider(self):
        url = 'http://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/MapServer/WMTS'
        imageryProvider = cesiumpy.WebMapTileServiceImageryProvider(url=url, layer='USGSShadedReliefOnly',
                                                                    style='default', format='image/jpeg',
                                                                    tileMatrixSetID='default028mm', maximumLevel=19,
                                                                    credit='U. S. Geological Survey')
        result = imageryProvider.script
        exp = """new Cesium.WebMapTileServiceImageryProvider({url : "http://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/MapServer/WMTS", layer : "USGSShadedReliefOnly", style : "default", format : "image/jpeg", maximumLevel : 19.0, credit : "U. S. Geological Survey"})"""
        self.assertEqual(result, exp)

    def test_GridImageryProvider(self):
        # Not Implemented
        # imageryProvider = cesiumpy.GridImageryProvider()
        # result = imageryProvider.script
        # exp = """new Cesium.TileCoordinatesImageryProvider()"""
        # self.assertEqual(result, exp)
        pass

    def test_TileCoordinatesImageryProvider(self):
        imageryProvider = cesiumpy.TileCoordinatesImageryProvider()
        result = imageryProvider.script
        exp = """new Cesium.TileCoordinatesImageryProvider()"""
        self.assertEqual(result, exp)


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
