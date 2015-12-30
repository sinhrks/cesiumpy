#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import six

import cesiumpy


class TestWidget(unittest.TestCase):

    def setUp(self):
        self.widget = cesiumpy.CesiumWidget(divid='widgettest')

    def test_repr(self):
        # should not be to_html output
        result = repr(self.widget)
        self.assertTrue(result.startswith("<cesiumpy.widget.CesiumWidget object"))

    def test_html(self):
        result = self.widget.to_html()
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/CesiumWidget/CesiumWidget.css" type="text/css">
<div id="widgettest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.CesiumWidget("widgettest");
</script>"""
        self.assertEqual(result, exp)

    def test_widget_props(self):
        widget = cesiumpy.CesiumWidget(divid='namechange', height='50%', width='70%')
        result = widget.to_html()
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/CesiumWidget/CesiumWidget.css" type="text/css">
<div id="namechange" style="width:50%; height:70%;"><div>
<script type="text/javascript">
  var widget = new Cesium.CesiumWidget("namechange");
</script>"""
        self.assertEqual(result, exp)

    def test_repr_html(self):
        self.assertEqual(self.widget.to_html(), self.widget._repr_html_())

    def test_random_divid(self):
        widget = cesiumpy.CesiumWidget()
        self.assertIsInstance(widget.divid, six.string_types)


class TestViewer(unittest.TestCase):

    def setUp(self):
        self.options = dict(animation=True, baseLayerPicker=False, fullscreenButton=False,
                            geocoder=False, homeButton=False, infoBox=False, sceneModePicker=True,
                            selectionIndicator=False, navigationHelpButton=False,
                            timeline=False, navigationInstructionsInitiallyVisible=False)
        self.viewer = cesiumpy.Viewer(divid='viewertest', **self.options)

    def test_repr(self):
        # should not be to_html output
        result = repr(self.viewer)
        self.assertTrue(result.startswith("<cesiumpy.viewer.Viewer object"))

    def test_html(self):
        result = self.viewer.to_html()
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/CesiumWidget/CesiumWidget.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest", {animation : true, baseLayerPicker : false, fullscreenButton : false, geocoder : false, homeButton : false, infoBox : false, sceneModePicker : true, selectionIndicator : false, timeline : false, navigationHelpButton : false, navigationInstructionsInitiallyVisible : false});
</script>"""
        self.assertEqual(result, exp)

    def test_add_cylinder(self):
        viewer = cesiumpy.Viewer(divid='viewertest', **self.options)
        cyl = cesiumpy.Cylinder(position=(-110, 50, 2000000), length=4000000,
                                topRadius=100000, bottomRadius=100000,
                                material=cesiumpy.color.AQUA, name='x')
        viewer.entities.add(cyl)
        result = viewer.to_html()

        # entity name must come first
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/CesiumWidget/CesiumWidget.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest", {animation : true, baseLayerPicker : false, fullscreenButton : false, geocoder : false, homeButton : false, infoBox : false, sceneModePicker : true, selectionIndicator : false, timeline : false, navigationHelpButton : false, navigationInstructionsInitiallyVisible : false});
  widget.entities.add({name : "x", position : Cesium.Cartesian3.fromDegrees(-110, 50, 2000000), cylinder : {length : 4000000, topRadius : 100000, bottomRadius : 100000, material : Cesium.Color.AQUA}});
</script>"""
        self.assertEqual(result, exp)

    def test_entities_attribute(self):
        with nose.tools.assert_raises(AttributeError):
            self.viewer.entities = None

    def test_add_polygon(self):
        viewer = cesiumpy.Viewer(divid="viewertest", **self.options)
        pol = cesiumpy.Polygon([-109.080842, 45.002073, -105.91517, 45.002073,
                                -104.058488, 44.996596, -104.053011, 43.002989,
                                -104.053011, 41.003906, -105.728954, 40.998429,
                                -107.919731, 41.003906, -109.04798, 40.998429,
                                -111.047063, 40.998429, -111.047063, 42.000709,
                                -111.047063, 44.476286, -111.05254, 45.002073],
                               material=cesiumpy.color.RED, name='x')
        viewer.entities.add(pol)
        result = viewer.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/CesiumWidget/CesiumWidget.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest", {animation : true, baseLayerPicker : false, fullscreenButton : false, geocoder : false, homeButton : false, infoBox : false, sceneModePicker : true, selectionIndicator : false, timeline : false, navigationHelpButton : false, navigationInstructionsInitiallyVisible : false});
  widget.entities.add({name : "x", polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([-109.080842, 45.002073, -105.91517, 45.002073, -104.058488, 44.996596, -104.053011, 43.002989, -104.053011, 41.003906, -105.728954, 40.998429, -107.919731, 41.003906, -109.04798, 40.998429, -111.047063, 40.998429, -111.047063, 42.000709, -111.047063, 44.476286, -111.05254, 45.002073]), material : Cesium.Color.RED}});
</script>"""
        self.assertEqual(result, exp)

    def test_add_entities(self):

        viewer = cesiumpy.Viewer(divid="viewertest", **self.options)
        viewer.entities.add(cesiumpy.Box(dimensions=(40e4, 30e4, 50e4),
                                         material=cesiumpy.color.RED, position=[-120, 40, 0]))
        viewer.entities.add(cesiumpy.Ellipse(semiMinorAxis=25e4, semiMajorAxis=40e4,
                                             material=cesiumpy.color.BLUE, position=[-110, 40, 0]))
        cyl = cesiumpy.Cylinder(position=[-100, 40, 50e4], length=100e4, topRadius=10e4,
                                bottomRadius=10e4, material=cesiumpy.color.AQUA)
        viewer.entities.add(cyl)
        viewer.entities.add(cesiumpy.Polygon([-90, 40, -95, 40, -95, 45, -90, 40],
                                             material=cesiumpy.color.ORANGE))
        viewer.entities.add(cesiumpy.Rectangle(coordinates=(-85, 40, -80, 45),
                                               material=cesiumpy.color.GREEN))
        viewer.entities.add(cesiumpy.Ellipsoid(position=(-70, 40, 0), radii=(20e4, 20e4, 30e4),
                                               material=cesiumpy.color.GREEN))
        wall = cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45],
                             maximumHeights=[10e4] * 4, minimumHeights=[0] * 4,
                             material=cesiumpy.color.RED)
        viewer.entities.add(wall)
        viewer.entities.add(cesiumpy.Corridor(positions=[-120, 30, -90, 35, -60, 30],
                                              width=2e5, material=cesiumpy.color.RED))
        viewer.entities.add(cesiumpy.Polyline(positions=[-120, 25, -90, 30, -60, 25], width=0.5,
                                              material=cesiumpy.color.BLUE))
        pol = cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20],
                                      shape=[cesiumpy.Cartesian2(-50000, -50000),
                                             cesiumpy.Cartesian2(50000, -50000),
                                             cesiumpy.Cartesian2(50000, 50000),
                                             cesiumpy.Cartesian2(-50000, 50000)],
                                      material=cesiumpy.color.GREEN)
        viewer.entities.add(pol)
        result = viewer.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/CesiumWidget/CesiumWidget.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest", {animation : true, baseLayerPicker : false, fullscreenButton : false, geocoder : false, homeButton : false, infoBox : false, sceneModePicker : true, selectionIndicator : false, timeline : false, navigationHelpButton : false, navigationInstructionsInitiallyVisible : false});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(-120, 40, 0), box : {dimensions : new Cesium.Cartesian3(400000.0, 300000.0, 500000.0), material : Cesium.Color.RED}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(-110, 40, 0), ellipse : {semiMinorAxis : 250000.0, semiMajorAxis : 400000.0, material : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(-100, 40, 500000.0), cylinder : {length : 1000000.0, topRadius : 100000.0, bottomRadius : 100000.0, material : Cesium.Color.AQUA}});
  widget.entities.add({polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([-90, 40, -95, 40, -95, 45, -90, 40]), material : Cesium.Color.ORANGE}});
  widget.entities.add({rectangle : {coordinates : Cesium.Rectangle.fromDegrees(-85, 40, -80, 45), material : Cesium.Color.GREEN}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(-70, 40, 0), ellipsoid : {radii : new Cesium.Cartesian3(200000.0, 200000.0, 300000.0), material : Cesium.Color.GREEN}});
  widget.entities.add({wall : {positions : Cesium.Cartesian3.fromDegreesArray([-60, 40, -65, 40, -65, 45, -60, 45]), maximumHeights : [100000.0, 100000.0, 100000.0, 100000.0], minimumHeights : [0, 0, 0, 0], material : Cesium.Color.RED}});
  widget.entities.add({corridor : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 30, -90, 35, -60, 30]), width : 200000.0, material : Cesium.Color.RED}});
  widget.entities.add({polyline : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 25, -90, 30, -60, 25]), width : 0.5, material : Cesium.Color.BLUE}});
  widget.entities.add({polylineVolume : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 20, -90, 25, -60, 20]), shape : [new Cesium.Cartesian2(-50000, -50000), new Cesium.Cartesian2(50000, -50000), new Cesium.Cartesian2(50000, 50000), new Cesium.Cartesian2(-50000, 50000)], material : Cesium.Color.GREEN}});
</script>"""
        self.assertEqual(result, exp)

        # clear entities
        viewer.entities.clear()
        result = viewer.to_html()
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/CesiumWidget/CesiumWidget.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest", {animation : true, baseLayerPicker : false, fullscreenButton : false, geocoder : false, homeButton : false, infoBox : false, sceneModePicker : true, selectionIndicator : false, timeline : false, navigationHelpButton : false, navigationInstructionsInitiallyVisible : false});
</script>"""
        self.assertEqual(result, exp)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
