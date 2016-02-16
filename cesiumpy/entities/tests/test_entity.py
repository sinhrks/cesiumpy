#!/usr/bin/env python
# coding: utf-8

import nose
import unittest
import traitlets

import cesiumpy


class TestEntity(unittest.TestCase):

    def test_validate_definitions(self):
        entities = [cesiumpy.Point, cesiumpy.Label, cesiumpy.Billboard,
                    cesiumpy.Ellipse, cesiumpy.Ellipsoid,
                    cesiumpy.Corridor, cesiumpy.Cylinder,
                    cesiumpy.Polyline, cesiumpy.PolylineVolume, cesiumpy.Wall,
                    cesiumpy.Rectangle, cesiumpy.Box, cesiumpy.Polygon]

        for entity in entities:
            # validate for development purpose, should be moved to tests
            for p in entity._props:
                self.assertFalse(p in entity._common_props)
            self.assertFalse('name' in entity._props)
            self.assertFalse('position' in entity._props)
            self.assertFalse('name' in entity._common_props)
            self.assertFalse('position' in entity._common_props)

    def test_point(self):
        e = cesiumpy.Point(position=(-110, 40, 0))
        exp = """{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}}"""
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        # create Cartesian3 from 2 elements tuple
        e = cesiumpy.Point(position=(-110, 40))
        self.assertEqual(e.script, exp)

        e = cesiumpy.Point(position=(-110, 40, 0), pixelSize=100, color='blue')
        exp = """{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), point : {pixelSize : 100.0, color : Cesium.Color.BLUE}}"""
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        # create Cartesian3 from 2 elements tuple
        e = cesiumpy.Point(position=(-110, 40), pixelSize=100, color='blue')
        self.assertEqual(e.script, exp)

    def test_label(self):
        e = cesiumpy.Label(position=(-110, 40, 0), text='label_text')
        exp = """{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), label : {text : "label_text"}}"""
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Label(position=(-110, 40, 0), text='label_text', fillColor='blue', scale=0.1)
        exp = """{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), label : {text : "label_text", fillColor : Cesium.Color.BLUE, scale : 0.1}}"""
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

    def test_billboard(self):
        p = cesiumpy.Pin()
        e = cesiumpy.Billboard(position=(-110, 40, 0), image=p)
        exp = """{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}}"""
        self.assertEqual(e.script, exp)

        e = cesiumpy.Billboard(position=(-110, 40, 0))
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        p = cesiumpy.Pin().fromText('?')
        e = cesiumpy.Billboard(position=(-110, 40, 0), image=p)
        exp = """{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromText("?", Cesium.Color.ROYALBLUE, 48.0)}}"""
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        p = cesiumpy.Pin().fromText('!', color='red')
        e = cesiumpy.Billboard(position=(-110, 40, 0), image=p, scale=3)
        exp = """{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromText("!", Cesium.Color.RED, 48.0), scale : 3.0}}"""
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

    def test_billboard_origins(self):
        p = cesiumpy.Pin()

        e = cesiumpy.Billboard(position=[-130, 40, 0], image=p,
                               horizontalOrigin=cesiumpy.HorizontalOrigin.LEFT,
                               verticalOrigin=cesiumpy.VerticalOrigin.BOTTOM)
        exp = """{position : Cesium.Cartesian3.fromDegrees(-130.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0), horizontalOrigin : Cesium.HorizontalOrigin.LEFT, verticalOrigin : Cesium.VerticalOrigin.BOTTOM}}"""
        self.assertEqual(e.script, exp)

        e = cesiumpy.Billboard(position=[-130, 40, 0], image=p,
                               horizontalOrigin=cesiumpy.HorizontalOrigin.CENTER,
                               verticalOrigin=cesiumpy.VerticalOrigin.CENTER)
        exp = """{position : Cesium.Cartesian3.fromDegrees(-130.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0), horizontalOrigin : Cesium.HorizontalOrigin.CENTER, verticalOrigin : Cesium.VerticalOrigin.CENTER}}"""
        self.assertEqual(e.script, exp)

        e = cesiumpy.Billboard(position=[-130, 40, 0], image=p,
                               horizontalOrigin=cesiumpy.HorizontalOrigin.RIGHT,
                               verticalOrigin=cesiumpy.VerticalOrigin.TOP)
        exp = """{position : Cesium.Cartesian3.fromDegrees(-130.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0), horizontalOrigin : Cesium.HorizontalOrigin.RIGHT, verticalOrigin : Cesium.VerticalOrigin.TOP}}"""
        self.assertEqual(e.script, exp)

        msg = "The 'horizontalOrigin' trait of a Billboard instance must be a HorizontalOrigin or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Billboard(position=[-130, 40, 0], image=p,
                               horizontalOrigin=1,
                               verticalOrigin=cesiumpy.VerticalOrigin.TOP)

        msg = "The 'verticalOrigin' trait of a Billboard instance must be a VerticalOrigin or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Billboard(position=[-130, 40, 0], image=p,
                               horizontalOrigin=cesiumpy.HorizontalOrigin.RIGHT,
                               verticalOrigin='xxx')

    def test_billboard_icon(self):
        b = cesiumpy.Billboard(position=[135, 35, 0], image='xxx.png', scale=0.1)
        exp = """{position : Cesium.Cartesian3.fromDegrees(135.0, 35.0, 0.0), billboard : {image : "xxx.png", scale : 0.1}}"""
        self.assertEqual(b.script, exp)

        b = cesiumpy.Billboard(position=[135, 35, 0], image='xxx.png', scale=0.1, eyeOffset=(0, 10e4, 0))
        exp = """{position : Cesium.Cartesian3.fromDegrees(135.0, 35.0, 0.0), billboard : {image : "xxx.png", scale : 0.1, eyeOffset : new Cesium.Cartesian3(0.0, 100000.0, 0.0)}}"""
        self.assertEqual(b.script, exp)

        b = cesiumpy.Billboard(position=[135, 35, 0], image='xxx.png', scale=0.1, pixelOffset=(0, 150))
        exp = """{position : Cesium.Cartesian3.fromDegrees(135.0, 35.0, 0.0), billboard : {image : "xxx.png", scale : 0.1, pixelOffset : new Cesium.Cartesian2(0.0, 150.0)}}"""
        self.assertEqual(b.script, exp)

    def test_ellipse(self):
        e = cesiumpy.Ellipse(position=[-110, 40, 0], semiMinorAxis=25.0, semiMajorAxis=40.0)
        exp = "{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), ellipse : {semiMinorAxis : 25.0, semiMajorAxis : 40.0}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Ellipse(position=[-110, 40, 0], semiMinorAxis=25.0, semiMajorAxis=40.0, material=cesiumpy.color.RED)
        exp = "{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), ellipse : {semiMinorAxis : 25.0, semiMajorAxis : 40.0, material : Cesium.Color.RED}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Ellipse(position=[-110, 40, 0], semiMinorAxis=25.0, semiMajorAxis=40.0, material='red')
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

    def test_ellipse_image_material(self):
        e = cesiumpy.Ellipse(position=[-110, 40, 0], semiMinorAxis=25.0,
                             semiMajorAxis=40.0, material='xxx.png')
        self.assertEqual(repr(e), 'Ellipse(-110.0, 40.0, 0.0)')
        exp = """{position : Cesium.Cartesian3.fromDegrees(-110.0, 40.0, 0.0), ellipse : {semiMinorAxis : 25.0, semiMajorAxis : 40.0, material : new Cesium.ImageMaterialProperty({image : "xxx.png"})}}"""
        self.assertEqual(e.script, exp)

    def test_ellipsoid(self):
        e = cesiumpy.Ellipsoid(position=(-70, 40, 0), radii=(20, 30, 40), material=cesiumpy.color.GREEN)
        exp = "{position : Cesium.Cartesian3.fromDegrees(-70.0, 40.0, 0.0), ellipsoid : {radii : new Cesium.Cartesian3(20.0, 30.0, 40.0), material : Cesium.Color.GREEN}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Ellipsoid(position=(-70, 40, 0), radii=(20, 30, 40), material=cesiumpy.color.RED, name='XXX')
        exp = '{name : "XXX", position : Cesium.Cartesian3.fromDegrees(-70.0, 40.0, 0.0), ellipsoid : {radii : new Cesium.Cartesian3(20.0, 30.0, 40.0), material : Cesium.Color.RED}}'
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        msg = "The 'radii' trait of an Ellipsoid instance must be a Cartesian3"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Ellipsoid(position=(-70, 40, 0), radii=(20, 30, 40, 10, 50))

    def test_cylinder(self):
        e = cesiumpy.Cylinder(position=(-70, 40, 0), length=10, topRadius=100, bottomRadius=200, material=cesiumpy.color.AQUA)
        exp = "{position : Cesium.Cartesian3.fromDegrees(-70.0, 40.0, 0.0), cylinder : {length : 10.0, topRadius : 100.0, bottomRadius : 200.0, material : Cesium.Color.AQUA}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Cylinder(position=(-70, 40, 0), length=10, topRadius=100, bottomRadius=200)
        exp = "{position : Cesium.Cartesian3.fromDegrees(-70.0, 40.0, 0.0), cylinder : {length : 10.0, topRadius : 100.0, bottomRadius : 200.0}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

    def test_polyline(self):
        e = cesiumpy.Polyline(positions=[-77, 35, -77.1, 35], width=5, material=cesiumpy.color.RED)
        exp = "{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([-77, 35, -77.1, 35]), width : 5.0, material : Cesium.Color.RED}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

    def test_polylinevolume(self):
        e = cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20],
                                    shape=[cesiumpy.Cartesian2(-50000, -50000), cesiumpy.Cartesian2(50000, -50000),
                                           cesiumpy.Cartesian2(50000, 50000), cesiumpy.Cartesian2(-50000, 50000)],
                                    material=cesiumpy.color.GREEN)
        exp = "{polylineVolume : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 20, -90, 25, -60, 20]), shape : [new Cesium.Cartesian2(-50000.0, -50000.0), new Cesium.Cartesian2(50000.0, -50000.0), new Cesium.Cartesian2(50000.0, 50000.0), new Cesium.Cartesian2(-50000.0, 50000.0)], material : Cesium.Color.GREEN}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20],
                                    shape=[1, 2, 3, 4], material=cesiumpy.color.GREEN)
        exp = "{polylineVolume : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 20, -90, 25, -60, 20]), shape : [new Cesium.Cartesian2(1.0, 2.0), new Cesium.Cartesian2(3.0, 4.0)], material : Cesium.Color.GREEN}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.PolylineVolume(positions=[(-120, 20), (-90, 25), (-60, 20)],
                                    shape=((1, 2), (3, 4)), material=cesiumpy.color.GREEN)
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.PolylineVolume(positions=[(-120, 20), (-90, 25), (-60, 20)],
                                    shape=((1, 2), (3, 4)), material=cesiumpy.color.GREEN)
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        msg = "shape must be list-likes: 1"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20], shape=1, material=cesiumpy.color.GREEN)

        msg = "shape length must be an even number: \\[1, 2, 4\\]"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20], shape=[1, 2, 4], material=cesiumpy.color.GREEN)

        msg = "shape must be a listlike of Cartesian2: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20],
                                    shape=[cesiumpy.Cartesian2(1, 2), cesiumpy.Cartesian3(1, 2, 3),
                                           cesiumpy.Cartesian2(3, 4)],
                                    material=cesiumpy.color.GREEN)

    def test_corridor(self):
        e = cesiumpy.Corridor(positions=[-120, 30, -90, 35, -60, 30],
                              width=2e5, material=cesiumpy.color.RED)
        exp = "{corridor : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 30, -90, 35, -60, 30]), width : 200000.0, material : Cesium.Color.RED}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Corridor(positions=((-120, 30), (-90, 35), (-60, 30)),
                              width=2e5, material='red')
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        msg = "x length must be an even number: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Corridor(positions=((-120, 30), (35, ), (-60, 30)),
                              width=2e5, material='red')

    def test_corridor_cornertypes(self):
        e = cesiumpy.Corridor(positions=[-130, 40, -120, 30, -110, 40], width=100000,
                              cornerType=cesiumpy.CornerType.BEVELED)
        exp = """{corridor : {positions : Cesium.Cartesian3.fromDegreesArray([-130, 40, -120, 30, -110, 40]), cornerType : Cesium.CornerType.BEVELED, width : 100000.0}}"""
        self.assertEqual(e.script, exp)

        e = cesiumpy.Corridor(positions=[-130, 40, -120, 30, -110, 40], width=100000,
                              cornerType=cesiumpy.CornerType.MITERED)
        exp = """{corridor : {positions : Cesium.Cartesian3.fromDegreesArray([-130, 40, -120, 30, -110, 40]), cornerType : Cesium.CornerType.MITERED, width : 100000.0}}"""
        self.assertEqual(e.script, exp)

        e = cesiumpy.Corridor(positions=[-130, 40, -120, 30, -110, 40], width=100000,
                              cornerType=cesiumpy.CornerType.ROUNDED)
        exp = """{corridor : {positions : Cesium.Cartesian3.fromDegreesArray([-130, 40, -120, 30, -110, 40]), cornerType : Cesium.CornerType.ROUNDED, width : 100000.0}}"""
        self.assertEqual(e.script, exp)

        msg = "The 'cornerType' trait of a Corridor instance must be a CornerType or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Corridor(positions=[-130, 40, -120, 30, -110, 40], width=100000,
                              cornerType='ROUNDED')

    def test_wall(self):
        e = cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45],
                          maximumHeights=100, minimumHeights=0,
                          material=cesiumpy.color.RED)
        exp = "{wall : {positions : Cesium.Cartesian3.fromDegreesArray([-60, 40, -65, 40, -65, 45, -60, 45]), maximumHeights : [100, 100, 100, 100], minimumHeights : [0, 0, 0, 0], material : Cesium.Color.RED}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45],
                          maximumHeights=[100] * 4, minimumHeights=[0] * 4,
                          material=cesiumpy.color.RED)
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Wall(positions=[(-60, 40), (-65, 40), (-65, 45), (-60, 45)],
                          maximumHeights=100, minimumHeights=0,
                          material='red')
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Wall(positions=[(-60, 40), (-65, 40), (-65, 45), (-60, 45)],
                          maximumHeights=[100] * 4, minimumHeights=[0] * 4,
                          material='red')
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        msg = "maximumHeights must has the half length"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45],
                          maximumHeights=[100] * 2, minimumHeights=[0] * 4,
                          material=cesiumpy.color.RED)

        msg = "minimumHeights must has the half length"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45],
                          maximumHeights=[100] * 4, minimumHeights=[0] * 3,
                          material=cesiumpy.color.RED)

    def test_rectangle(self):
        e = cesiumpy.Rectangle(coordinates=(-80, 20, -60, 40), material=cesiumpy.color.GREEN)
        exp = "{rectangle : {coordinates : Cesium.Rectangle.fromDegrees(-80.0, 20.0, -60.0, 40.0), material : Cesium.Color.GREEN}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Rectangle(coordinates=(-80, 20, -60, 40),
                               material=cesiumpy.color.GREEN, outlineColor=cesiumpy.color.RED)
        exp = "{rectangle : {coordinates : Cesium.Rectangle.fromDegrees(-80.0, 20.0, -60.0, 40.0), material : Cesium.Color.GREEN, outlineColor : Cesium.Color.RED}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Rectangle(coordinates=[(-80, 20), (-60, 40)],
                               material='green', outlineColor='red')
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Rectangle(coordinates=(-80, 20, -60, 40), material='green', outlineColor='red')
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        msg = "The 'coordinates' trait of a Rectangle instance must be a Rectangle"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Rectangle(coordinates=[1, 2, 3],
                               material='green', outlineColor='red')

        msg = "The 'north' trait of a Rectangle instance must be a float"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Rectangle(coordinates=(-80, 20, -60, 'X'),
                               material='green', outlineColor='red')

    def test_box(self):
        e = cesiumpy.Box(dimensions=(40e4, 30e4, 50e4),
                         material=cesiumpy.color.RED, position=[-120, 40, 0])
        exp = "{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box : {dimensions : new Cesium.Cartesian3(400000.0, 300000.0, 500000.0), material : Cesium.Color.RED}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        msg = "The 'dimensions' trait of a Box instance must be a Cartesian3"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Box(dimensions=(40e4, 30e4),
                         material=cesiumpy.color.RED, position=[-120, 40, 0])

    def test_polygon(self):
        e = cesiumpy.Polygon([1, 1, 2, 2])
        exp = "{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([1, 1, 2, 2])}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

        e = cesiumpy.Polygon([1, 1, 2, 2], material=cesiumpy.color.AQUA)
        exp = "{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([1, 1, 2, 2]), material : Cesium.Color.AQUA}}"
        self.assertEqual(e.script, exp)

        e = e.copy()
        self.assertEqual(e.script, exp)

    def test_entities_repr(self):
        e = cesiumpy.Point(position=[-110, 40, 0])
        exp = "Point(-110.0, 40.0, 0.0)"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Label(position=[-110, 40, 0], text='xxx')
        exp = "Label(-110.0, 40.0, 0.0)"
        self.assertEqual(repr(e), exp)

        p = cesiumpy.Pin()
        e = cesiumpy.Billboard(position=(-110, 40, 0), image=p)
        exp = "Billboard(-110.0, 40.0, 0.0)"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Box(position=[-110, 40, 0], dimensions=(40e4, 30e4, 50e4))
        exp = "Box(-110.0, 40.0, 0.0)"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Ellipse(position=[-110, 40, 0], semiMinorAxis=25e4,
                             semiMajorAxis=40e4)
        exp = "Ellipse(-110.0, 40.0, 0.0)"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Cylinder(position=[-110, 40, 100], length=100e4,
                              topRadius=10e4, bottomRadius=10e4)
        exp = "Cylinder(-110.0, 40.0, 100.0)"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Polygon(hierarchy=[-90, 40, -95, 40, -95, 45, -90, 40])
        exp = "Polygon([-90, 40, -95, 40, -95, 45, -90, 40])"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Rectangle(coordinates=(-85, 40, -80, 45))
        exp = "Rectangle(west=-85.0, south=40.0, east=-80.0, north=45.0)"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Ellipsoid(position=(-70, 40, 0), radii=(20e4, 20e4, 30e4))
        exp = "Ellipsoid(-70.0, 40.0, 0.0)"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45],
                          maximumHeights=[10e4] * 4, minimumHeights=[0] * 4)
        exp = "Wall([-60, 40, -65, 40, -65, 45, -60, 45])"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Corridor(positions=[-120, 30, -90, 35, -60, 30], width=2e5)
        exp = "Corridor([-120, 30, -90, 35, -60, 30])"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.Polyline(positions=[-120, 25, -90, 30, -60, 25], width=0.5)
        exp = "Polyline([-120, 25, -90, 30, -60, 25])"
        self.assertEqual(repr(e), exp)

        e = cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20],
                                    shape=[-5e4, -5e4, 5e4, -5e4, 5e4, 5e4, -5e4, 5e4])
        exp = "PolylineVolume([-120, 20, -90, 25, -60, 20])"
        self.assertEqual(repr(e), exp)

    def test_material_property(self):
        msg = "The 'material' trait of a Box instance must be a Material or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Box(position=[-120, 40, 0], dimensions=(10, 20, 30),
                         material=1)

        b = cesiumpy.Box(position=[-120, 40, 0], dimensions=(10, 20, 30),
                         material='red')
        exp = """{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box : {dimensions : new Cesium.Cartesian3(10.0, 20.0, 30.0), material : Cesium.Color.RED}}"""
        self.assertEqual(b.script, exp)

        msg = "The 'material' trait of a Box instance must be a Material or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            b.material = 1

        b.material = 'blue'
        exp = """{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box : {dimensions : new Cesium.Cartesian3(10.0, 20.0, 30.0), material : Cesium.Color.BLUE}}"""
        self.assertEqual(b.script, exp)

    def test_color_property(self):
        msg = "The 'color' trait of a Point instance must be a Color or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Point(position=[-120, 40, 0], color=1)

        b = cesiumpy.Point(position=[-120, 40, 0], color='red')
        exp = """{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.RED}}"""
        self.assertEqual(b.script, exp)

        msg = "The 'color' trait of a Point instance must be a Color or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            b.color = 1

        b.color = 'blue'
        exp = """{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.BLUE}}"""
        self.assertEqual(b.script, exp)

    def test_outlineColor_property(self):
        msg = "The 'outlineColor' trait of a Box instance must be a Color or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Box(position=[-120, 40, 0], dimensions=(10, 20, 30),
                         outlineColor=1)

        b = cesiumpy.Box(position=[-120, 40, 0], dimensions=(10, 20, 30),
                         outlineColor='red')
        exp = """{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box : {dimensions : new Cesium.Cartesian3(10.0, 20.0, 30.0), outlineColor : Cesium.Color.RED}}"""
        self.assertEqual(b.script, exp)

        msg = "The 'outlineColor' trait of a Box instance must be a Color or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            b.outlineColor = 1

        b.outlineColor = 'blue'
        exp = """{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), box : {dimensions : new Cesium.Cartesian3(10.0, 20.0, 30.0), outlineColor : Cesium.Color.BLUE}}"""
        self.assertEqual(b.script, exp)

    def test_fillColor_property(self):
        msg = "The 'fillColor' trait of a Label instance must be a Color or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Label(position=[-120, 40, 0], text="xxx", fillColor=1)

        b = cesiumpy.Label(position=[-120, 40, 0], text="xxx", fillColor="red")
        exp = """{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), label : {text : "xxx", fillColor : Cesium.Color.RED}}"""
        self.assertEqual(b.script, exp)

        msg = "The 'fillColor' trait of a Label instance must be a Color or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            b.fillColor = 1

        b.fillColor = 'blue'
        exp = """{position : Cesium.Cartesian3.fromDegrees(-120.0, 40.0, 0.0), label : {text : "xxx", fillColor : Cesium.Color.BLUE}}"""
        self.assertEqual(b.script, exp)


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
