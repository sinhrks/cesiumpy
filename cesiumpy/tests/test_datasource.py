#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import six

import cesiumpy


class TestDataSource(unittest.TestCase):

    def test_geojsondatasource(self):
        ds = cesiumpy.GeoJsonDataSource('xxx.geojson')

        exp = 'Cesium.GeoJsonDataSource.load("xxx.geojson")'
        self.assertEqual(ds.script, exp)

        ds = cesiumpy.GeoJsonDataSource('xxx.geojson', markerColor=cesiumpy.color.RED,
                                        stroke=cesiumpy.color.BLUE, fill=cesiumpy.color.GREEN)
        exp = 'Cesium.GeoJsonDataSource.load("xxx.geojson", {markerColor : Cesium.Color.RED, stroke : Cesium.Color.BLUE, fill : Cesium.Color.GREEN})'
        self.assertEqual(ds.script, exp)

        ds = cesiumpy.GeoJsonDataSource('xxx.geojson', markerColor='red',
                                        stroke='blue', fill='green')
        self.assertEqual(ds.script, exp)

    def test_geojson_viewer(self):
        ds = cesiumpy.GeoJsonDataSource('./test.geojson', markerSymbol='?')
        viewer = cesiumpy.Viewer(divid='viewertest')
        viewer.dataSources.add(ds)
        viewer.camera.flyTo((-105.01621, 39.57422, 1000))
        result = viewer.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.dataSources.add(Cesium.GeoJsonDataSource.load("./test.geojson", {markerSymbol : "?"}));
  widget.camera.flyTo({destination : Cesium.Cartesian3.fromDegrees(-105.01621, 39.57422, 1000)});
</script>"""
        self.assertEqual(result, exp)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
