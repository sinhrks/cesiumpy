#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import geopy

import cesiumpy


class TestGeocode(unittest.TestCase):

    def test_geocode(self):
        try:
            result = cesiumpy.geocode._maybe_geocode('Los Angeles')
            self.assertEqual(result, (-118.2436849, 34.0522342))

            result = cesiumpy.geocode._maybe_geocode(['Los Angeles', 'Las Vegas'])
            self.assertEqual(result, [(-118.2436849, 34.0522342), (-115.1728497, 36.1147074)])

            result = cesiumpy.geocode._maybe_geocode(['Los Angeles', 'Las Vegas', [1, 2]])
            self.assertEqual(result, [(-118.2436849, 34.0522342), (-115.1728497, 36.1147074), [1, 2]])

            # do not convert
            result = cesiumpy.geocode._maybe_geocode(3)
            self.assertEqual(result, 3)

            result = cesiumpy.geocode._maybe_geocode('xxxxx_str_unable_to_be_converted_xxxxxx')
            self.assertEqual(result, 'xxxxx_str_unable_to_be_converted_xxxxxx')
        except geopy.exc.GeocoderQuotaExceeded:
            raise nose.SkipTest("exceeded geocoder quota")

    def test_geocode_unicode(self):
        try:
            result = cesiumpy.geocode._maybe_geocode(u'富士山')
            self.assertEqual(result, (138.7277777, 35.3605555))

            result = cesiumpy.geocode._maybe_geocode(u'xxxxx_変換できない文字列_xxxxxx')
            self.assertEqual(result, u'xxxxx_変換できない文字列_xxxxxx')

            result = cesiumpy.geocode._maybe_geocode([u'富士山', u'赤岳'])
            self.assertEqual(result, [(138.7277777, 35.3605555), (138.3702338, 35.9709019)])
        except geopy.exc.GeocoderQuotaExceeded:
            raise nose.SkipTest("exceeded geocoder quota")

    def test_cartesian3_geocode(self):
        try:
            result = cesiumpy.entities.cartesian.Cartesian3.maybe(u'富士山')
            self.assertEqual(result.script, 'new Cesium.Cartesian3(138.7277777, 35.3605555, 0.0)')

            result = cesiumpy.entities.cartesian.Cartesian3.maybe('Los Angeles')
            self.assertEqual(result.script, 'new Cesium.Cartesian3(-118.2436849, 34.0522342, 0.0)')
        except geopy.exc.GeocoderQuotaExceeded:
            raise nose.SkipTest("exceeded geocoder quota")

    def test_entities_geocode(self):
        try:
            e = cesiumpy.Point(position='Los Angeles')
            exp = """{position : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}}"""
            self.assertEqual(e.script, exp)

            e = cesiumpy.Label(position='Los Angeles', text='xxx')
            exp = """{position : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 0.0), label : {text : "xxx"}}"""
            self.assertEqual(e.script, exp)

            p = cesiumpy.Pin()
            e = cesiumpy.Billboard(position='Los Angeles', image=p)
            exp = """{position : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}}"""
            self.assertEqual(e.script, exp)

            e = cesiumpy.Box(position='Los Angeles', dimensions=(40e4, 30e4, 50e4))
            exp = """{position : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 0.0), box : {dimensions : new Cesium.Cartesian3(400000.0, 300000.0, 500000.0)}}"""
            self.assertEqual(e.script, exp)

            e = cesiumpy.Ellipse(position='Los Angeles', semiMinorAxis=25e4,
                                 semiMajorAxis=40e4)
            exp = """{position : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 0.0), ellipse : {semiMinorAxis : 250000.0, semiMajorAxis : 400000.0}}"""
            self.assertEqual(e.script, exp)

            e = cesiumpy.Cylinder(position='Los Angeles', length=100e4,
                                  topRadius=10e4, bottomRadius=10e4)
            exp = """{position : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 0.0), cylinder : {length : 1000000.0, topRadius : 100000.0, bottomRadius : 100000.0}}"""
            self.assertEqual(e.script, exp)

            e = cesiumpy.Polygon(hierarchy=['Los Angeles', 'Las Vegas', 'San Francisco'])
            exp = """{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([-118.2436849, 34.0522342, -115.1728497, 36.1147074, -122.4194155, 37.7749295])}}"""
            self.assertEqual(e.script, exp)

            # not supported, Unabel to create rectangle from single geolocation
            e = cesiumpy.Rectangle(coordinates=(-85, 40, -80, 45))

            e = cesiumpy.Ellipsoid(position='Los Angeles', radii=(20e4, 20e4, 30e4))
            exp = """{position : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 0.0), ellipsoid : {radii : new Cesium.Cartesian3(200000.0, 200000.0, 300000.0)}}"""
            self.assertEqual(e.script, exp)

            e = cesiumpy.Wall(positions=['Los Angeles', 'Las Vegas', 'San Francisco'],
                              maximumHeights=10e4, minimumHeights=0)
            exp = "{wall : {positions : Cesium.Cartesian3.fromDegreesArray([-118.2436849, 34.0522342, -115.1728497, 36.1147074, -122.4194155, 37.7749295]), maximumHeights : [100000.0, 100000.0, 100000.0], minimumHeights : [0, 0, 0]}}"
            self.assertEqual(e.script, exp)

            e = cesiumpy.Corridor(positions=['Los Angeles', 'Las Vegas', 'San Francisco'], width=2e5)
            exp = """{corridor : {positions : Cesium.Cartesian3.fromDegreesArray([-118.2436849, 34.0522342, -115.1728497, 36.1147074, -122.4194155, 37.7749295]), width : 200000.0}}"""
            self.assertEqual(e.script, exp)

            e = cesiumpy.Polyline(positions=['Los Angeles', 'Las Vegas', 'San Francisco'], width=0.5)
            exp = """{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([-118.2436849, 34.0522342, -115.1728497, 36.1147074, -122.4194155, 37.7749295]), width : 0.5}}"""
            self.assertEqual(e.script, exp)

            e = cesiumpy.PolylineVolume(positions=['Los Angeles', 'Las Vegas', 'San Francisco'],
                                        shape=[-5e4, -5e4, 5e4, -5e4, 5e4, 5e4, -5e4, 5e4])
            exp = """{polylineVolume : {positions : Cesium.Cartesian3.fromDegreesArray([-118.2436849, 34.0522342, -115.1728497, 36.1147074, -122.4194155, 37.7749295]), shape : [new Cesium.Cartesian2(-50000.0, -50000.0), new Cesium.Cartesian2(50000.0, -50000.0), new Cesium.Cartesian2(50000.0, 50000.0), new Cesium.Cartesian2(-50000.0, 50000.0)]}}"""
            self.assertEqual(e.script, exp)
        except geopy.exc.GeocoderQuotaExceeded:
            raise nose.SkipTest("exceeded geocoder quota")

    def test_viewer(self):
        try:
            viewer = cesiumpy.Viewer(divid='viewertest')
            cyl = cesiumpy.Cylinder(position='Los Angeles', length=30000, topRadius=10000,
                                    bottomRadius=10000, material='AQUA')
            viewer.entities.add(cyl)
            viewer.camera.flyTo('Los Angeles')
            result = viewer.to_html()

            exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 0.0), cylinder : {length : 30000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.AQUA}});
  widget.camera.flyTo({destination : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 100000.0)});
</script>"""
            self.assertEqual(result, exp)
        except geopy.exc.GeocoderQuotaExceeded:
            raise nose.SkipTest("exceeded geocoder quota")


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
