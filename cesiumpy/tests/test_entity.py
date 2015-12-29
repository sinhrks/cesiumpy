#!/usr/bin/env python
# coding: utf-8

# do not import unicode_literals here to test ASCII in Python 2.7

import unittest
import nose

import cesiumpy


class TestEntity(unittest.TestCase):

    def test_ellipse(self):
        e = cesiumpy.Ellipse(semiMinorAxis=25.0, semiMajorAxis=40.0)
        exp = "{ellipse : {semiMinorAxis : 25.0, semiMajorAxis : 40.0}}"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Ellipse(semiMinorAxis=25.0, semiMajorAxis=40.0, material=cesiumpy.color.RED)
        exp = "{ellipse : {semiMinorAxis : 25.0, semiMajorAxis : 40.0, material : Cesium.Color.RED}}"
        self.assertEqual(repr(e), exp)

    def test_ellipsoid(self):
        e = cesiumpy.Ellipsoid(position=(-70, 40, 0), radii=(20, 30, 40), material=cesiumpy.color.GREEN)
        exp = "{position : Cesium.Cartesian3.fromDegrees(-70, 40, 0), ellipsoid : {radii : new Cesium.Cartesian3(20, 30, 40), material : Cesium.Color.GREEN}}"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Ellipsoid(position=(-70, 40, 0), radii=(20, 30, 40), material=cesiumpy.color.RED, name='XXX')
        exp = '{name : "XXX", position : Cesium.Cartesian3.fromDegrees(-70, 40, 0), ellipsoid : {radii : new Cesium.Cartesian3(20, 30, 40), material : Cesium.Color.RED}}'
        self.assertEqual(repr(e), exp)

    def test_cylinder(self):
        e = cesiumpy.Cylinder(10, 100, 200, material=cesiumpy.color.AQUA)
        exp = "{cylinder : {length : 10, topRadius : 100, bottomRadius : 200, material : Cesium.Color.AQUA}}"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Cylinder(10, 100, 200)
        exp = "{cylinder : {length : 10, topRadius : 100, bottomRadius : 200}}"
        self.assertEqual(repr(e), exp)

    def test_polyline(self):
        e = cesiumpy.Polyline(positions=[-77, 35, -77.1, 35], width=5, material=cesiumpy.color.RED)
        exp = "{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([-77, 35, -77.1, 35]), width : 5, material : Cesium.Color.RED}}"
        self.assertEqual(repr(e), exp)

    def test_polylinevolume(self):
        e = cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20],
                                    shape=[cesiumpy.Cartesian2(-50000, -50000), cesiumpy.Cartesian2(50000, -50000),
                                           cesiumpy.Cartesian2(50000, 50000), cesiumpy.Cartesian2(-50000, 50000)],
                                    material=cesiumpy.color.GREEN)
        exp = "{polylineVolume : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 20, -90, 25, -60, 20]), shape : [new Cesium.Cartesian2(-50000, -50000), new Cesium.Cartesian2(50000, -50000), new Cesium.Cartesian2(50000, 50000), new Cesium.Cartesian2(-50000, 50000)], material : Cesium.Color.GREEN}}"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20], shape=[1, 2, 3, 4], material=cesiumpy.color.GREEN)
        exp = "{polylineVolume : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 20, -90, 25, -60, 20]), shape : [new Cesium.Cartesian2(1, 2), new Cesium.Cartesian2(3, 4)], material : Cesium.Color.GREEN}}"
        self.assertEqual(repr(e), exp)

        msg = "unable to convert input to list of Cartesian2: 1"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20], shape=1, material=cesiumpy.color.GREEN)

    def test_corridor(self):
        e = cesiumpy.Corridor(positions=[-120, 30, -90, 35, -60, 30], width=2e5, material=cesiumpy.color.RED)
        exp = "{corridor : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 30, -90, 35, -60, 30]), width : 200000.0, material : Cesium.Color.RED}}"
        self.assertEqual(repr(e), exp)

    def test_wall(self):
        e = cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45], maximumHeights=100, minimumHeights=0,
                          material=cesiumpy.color.RED)
        exp = "{wall : {positions : Cesium.Cartesian3.fromDegreesArray([-60, 40, -65, 40, -65, 45, -60, 45]), maximumHeights : [100, 100, 100, 100], minimumHeights : [0, 0, 0, 0], material : Cesium.Color.RED}}"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45], maximumHeights=[100] * 4, minimumHeights=[0] * 4,
                          material=cesiumpy.color.RED)
        self.assertEqual(repr(e), exp)

        msg = "maximumHeights must has the half length"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45], maximumHeights=[100] * 2, minimumHeights=[0] * 4,
                          material=cesiumpy.color.RED)

        msg = "minimumHeights must has the half length"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45], maximumHeights=[100] * 4, minimumHeights=[0] * 3,
                          material=cesiumpy.color.RED)

    def test_rectangle(self):
        e = cesiumpy.Rectangle(coordinates=(-80, 20, -60, 40), material=cesiumpy.color.GREEN)
        exp = "{rectangle : {coordinates : Cesium.Rectangle.fromDegrees(-80, 20, -60, 40), material : Cesium.Color.GREEN}}"
        self.assertEqual(repr(e), exp)

    def test_box(self):
        e = cesiumpy.Box(dimensions=(40e4, 30e4, 50e4), material=cesiumpy.color.RED, position=[-120, 40, 0])
        exp = "{position : Cesium.Cartesian3.fromDegrees(-120, 40, 0), box : {dimensions : new Cesium.Cartesian3(400000.0, 300000.0, 500000.0), material : Cesium.Color.RED}}"
        self.assertEqual(repr(e), exp)

    def test_polygon(self):
        e = cesiumpy.Polygon([1, 1, 2, 2])
        exp = "{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([1, 1, 2, 2])}}"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Polygon([1, 1, 2, 2], material=cesiumpy.color.AQUA)
        exp = "{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([1, 1, 2, 2]), material : Cesium.Color.AQUA}}"
        self.assertEqual(repr(e), exp)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
