#!/usr/bin/env python
# coding: utf-8

import unittest
import nose
import traitlets

import cesiumpy


class TestCamera(unittest.TestCase):

    def test_camera_basics(self):
        widget = cesiumpy.CesiumWidget(divid='cesiumwidget')

        c = cesiumpy.Camera(widget)
        self.assertEqual(c.script, '')

        c.flyTo((1, 2, 3))
        exp = '{destination : Cesium.Cartesian3.fromDegrees(1.0, 2.0, 3.0)}'
        self.assertEqual(c.script, exp)

        c.flyTo((4, 5, 6))
        exp = '{destination : Cesium.Cartesian3.fromDegrees(4.0, 5.0, 6.0)}'
        self.assertEqual(c.script, exp)

        c.flyTo((4, 5, 6, 7))
        exp = '{destination : Cesium.Rectangle.fromDegrees(4.0, 5.0, 6.0, 7.0)}'
        self.assertEqual(c.script, exp)

        msg = "x must be longitude, between -180 to 180"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            c.flyTo((200, 2, 3))

        msg = "y must be latitude, between -90 to 90"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            c.flyTo((1, 200, 3))

        msg = "The 'destination' trait of a Camera instance must be a _Cartesian or None"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            c.flyTo(1)

    def test_camera_repr(self):
        widget = cesiumpy.CesiumWidget(divid='cesiumwidget')

        c = cesiumpy.Camera(widget)
        self.assertEqual(repr(c), "Camera(destination=default)")

        c.flyTo((-130, 40, 10000))
        self.assertEqual(repr(c), "Camera(destination=Cartesian3.fromDegrees(-130.0, 40.0, 10000.0))")

    def test_widget(self):
        widget = cesiumpy.CesiumWidget(divid='cesiumwidget')
        widget.camera.flyTo((-117.16, 32.71, 15000.0))
        result = widget.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="cesiumwidget" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.CesiumWidget("cesiumwidget");
  widget.camera.flyTo({destination : Cesium.Cartesian3.fromDegrees(-117.16, 32.71, 15000.0)});
</script>"""
        self.assertEqual(result, exp)

    def test_viewer(self):
        viewer = cesiumpy.Viewer(divid='viewertest')
        viewer.camera.flyTo((135, 30, 145, 45))
        result = viewer.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.camera.flyTo({destination : Cesium.Rectangle.fromDegrees(135.0, 30.0, 145.0, 45.0)});
</script>"""
        self.assertEqual(result, exp)

        # add entity (doesn't change camera position)
        cyl = cesiumpy.Cylinder(position=(120, 35, 5000), length=10000, topRadius=10000,
                                bottomRadius=20000, material='red')
        viewer.entities.add(cyl)
        result = viewer.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(120.0, 35.0, 5000.0), cylinder : {length : 10000.0, topRadius : 10000.0, bottomRadius : 20000.0, material : Cesium.Color.RED}});
  widget.camera.flyTo({destination : Cesium.Rectangle.fromDegrees(135.0, 30.0, 145.0, 45.0)});
</script>"""
        self.assertEqual(result, exp)

        # we can pass entity with position to camera
        viewer.camera.flyTo(cyl)
        result = viewer.to_html()

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(120.0, 35.0, 5000.0), cylinder : {length : 10000.0, topRadius : 10000.0, bottomRadius : 20000.0, material : Cesium.Color.RED}});
  widget.camera.flyTo({destination : Cesium.Cartesian3.fromDegrees(120.0, 35.0, 5000.0)});
</script>"""
        self.assertEqual(result, exp)

    def test_geocode_defaultheight(self):
        import geopy
        try:
            viewer = cesiumpy.Viewer(divid='viewertest')
            viewer.camera.flyTo(u'Los Angeles')
            result = viewer.to_html()

            exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.camera.flyTo({destination : Cesium.Cartesian3.fromDegrees(-118.2436849, 34.0522342, 100000.0)});
</script>"""
            self.assertEqual(result, exp)
        except geopy.exc.GeocoderQuotaExceeded:
            raise nose.SkipTest("exceeded geocoder quota")


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
