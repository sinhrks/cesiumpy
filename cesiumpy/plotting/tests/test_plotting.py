#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import cesiumpy
from cesiumpy.testing import _skip_if_no_numpy


class TestScatter(unittest.TestCase):

    def test_scatter_xy(self):
        v = cesiumpy.Viewer(divid='viewertest')
        res = v.plot.scatter([130, 140, 150], [30, 40, 50])
        self.assertIsInstance(v, cesiumpy.Viewer)

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(res.to_html(), exp)
        # entities must be added to original instance
        self.assertEqual(v.to_html(), exp)

    def test_scatter_xyz(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.scatter([130, 140, 150], [30, 40, 50], [1e05, 2e05, 3e05])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 100000.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 200000.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 300000.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_scatter_xy_color_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.scatter([130, 140, 150], [30, 40, 50], color=cesiumpy.color.BLUE)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.BLUE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_scatter_xy_color_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.scatter([130, 140, 150], [30, 40, 50],
                       color=[cesiumpy.color.BLUE, cesiumpy.color.RED, cesiumpy.color.GREEN])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.RED}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.GREEN}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_scatter_xy_size_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.scatter([130, 140, 150], [30, 40, 50], size=50)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point : {pixelSize : 50.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point : {pixelSize : 50.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point : {pixelSize : 50.0, color : Cesium.Color.WHITE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_scatter_xy_size_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.scatter([130, 140, 150], [30, 40, 50], size=[20, 30, 40])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point : {pixelSize : 20.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point : {pixelSize : 30.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point : {pixelSize : 40.0, color : Cesium.Color.WHITE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_scatter_errors(self):
        v = cesiumpy.Viewer(divid='viewertest')

        msg = "y must be list-likes: 0"
        with nose.tools.assert_raises_regexp(ValueError, msg):
            v.plot.scatter([130, 140, 150], 0)

        msg = "y length must be 3: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            v.plot.scatter([130, 140, 150], [30, 40])

        msg = "size length must be 3: "
        with nose.tools.assert_raises_regexp(ValueError, msg):
            v.plot.scatter([130, 140, 150], [30, 40, 50], size=[1, 2])


class TestBar(unittest.TestCase):

    def test_bar_xyz(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.bar([130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder : {length : 1000000.0, topRadius : 10000.0, bottomRadius : 10000.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder : {length : 2000000.0, topRadius : 10000.0, bottomRadius : 10000.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder : {length : 3000000.0, topRadius : 10000.0, bottomRadius : 10000.0}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_bar_color_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.bar([130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5], color=cesiumpy.color.BLUE)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder : {length : 1000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder : {length : 2000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder : {length : 3000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.BLUE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_bar_color_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.bar([130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5],
                   color=[cesiumpy.color.BLUE, cesiumpy.color.RED, cesiumpy.color.GREEN])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder : {length : 1000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder : {length : 2000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.RED}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder : {length : 3000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.GREEN}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_bar_size_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.bar([130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5], size=1e5)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder : {length : 1000000.0, topRadius : 100000.0, bottomRadius : 100000.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder : {length : 2000000.0, topRadius : 100000.0, bottomRadius : 100000.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder : {length : 3000000.0, topRadius : 100000.0, bottomRadius : 100000.0}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_bar_size_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.bar([130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5], size=[1e3, 1e4, 1e5])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder : {length : 1000000.0, topRadius : 1000.0, bottomRadius : 1000.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder : {length : 2000000.0, topRadius : 10000.0, bottomRadius : 10000.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder : {length : 3000000.0, topRadius : 100000.0, bottomRadius : 100000.0}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_bar_bottom(self):
        v = cesiumpy.Viewer('viewertest')
        v.plot.bar([130, 140, 150], [30, 40, 50], [10e5, 20e5, 30e5], color=cesiumpy.color.RED)
        v.plot.bar([130, 140, 150], [30, 40, 50], [30e5, 20e5, 10e5], color=cesiumpy.color.BLUE, bottom=[10e5, 20e5, 30e5])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 500000.0), cylinder : {length : 1000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.RED}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), cylinder : {length : 2000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.RED}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1500000.0), cylinder : {length : 3000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.RED}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 2500000.0), cylinder : {length : 3000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 3000000.0), cylinder : {length : 2000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 3500000.0), cylinder : {length : 1000000.0, topRadius : 10000.0, bottomRadius : 10000.0, material : Cesium.Color.BLUE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)


class TestLabel(unittest.TestCase):

    def test_label_xy(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.label(['A', 'B', 'C'], [130, 140, 150], [30, 40, 50])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label : {text : "A"}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label : {text : "B"}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label : {text : "C"}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_label_xyz(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.label(['A', 'B', 'C'], [130, 140, 150], [30, 40, 50], 10e5)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 1000000.0), label : {text : "A"}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), label : {text : "B"}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1000000.0), label : {text : "C"}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_label_xyz_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.label(['A', 'B', 'C'], [130, 140, 150], [30, 40, 50], [10e4, 10e5, 10e4])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 100000.0), label : {text : "A"}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), label : {text : "B"}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 100000.0), label : {text : "C"}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_label_color_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.label(['A', 'B', 'C'], [130, 140, 150], [30, 40, 50], color=cesiumpy.color.GREEN)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label : {text : "A", fillColor : Cesium.Color.GREEN}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label : {text : "B", fillColor : Cesium.Color.GREEN}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label : {text : "C", fillColor : Cesium.Color.GREEN}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_label_color_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.label(['A', 'B', 'C'], [130, 140, 150], [30, 40, 50],
                     color=[cesiumpy.color.BLUE, cesiumpy.color.RED, cesiumpy.color.GREEN])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label : {text : "A", fillColor : Cesium.Color.BLUE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label : {text : "B", fillColor : Cesium.Color.RED}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label : {text : "C", fillColor : Cesium.Color.GREEN}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_label_size_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.label(['A', 'B', 'C'], [130, 140, 150], [30, 40, 50], size=2)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label : {text : "A", scale : 2.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label : {text : "B", scale : 2.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label : {text : "C", scale : 2.0}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_label_size_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.label(['A', 'B', 'C'], [130, 140, 150], [30, 40, 50], size=[2, 3, 0.5])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), label : {text : "A", scale : 2.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), label : {text : "B", scale : 3.0}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), label : {text : "C", scale : 0.5}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)


class TestPin(unittest.TestCase):

    def test_pin_xy(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_pin_xyz(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50], z=1e6)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 1000000.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 1000000.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_pin_xyz_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50], [10e4, 10e5, 10e4])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 100000.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 1000000.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 100000.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_pin_color_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50], color=cesiumpy.color.GREEN)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 48.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_pin_color_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50],
                   color=[cesiumpy.color.BLUE, cesiumpy.color.RED, cesiumpy.color.GREEN])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.BLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.RED, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 48.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_pin_size_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50], size=24)
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 24.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 24.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 24.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_pin_size_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50], size=[12, 24, 48])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 12.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 24.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_pin_label_scalar(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50], text='!')
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromText("!", Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromText("!", Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromText("!", Cesium.Color.ROYALBLUE, 48.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)

    def test_pin_label_list(self):
        v = cesiumpy.Viewer(divid='viewertest')
        v.plot.pin([130, 140, 150], [30, 40, 50], text=['!', '?', 'XXX'])
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromText("!", Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromText("?", Cesium.Color.ROYALBLUE, 48.0)}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), billboard : {image : new Cesium.PinBuilder().fromText("XXX", Cesium.Color.ROYALBLUE, 48.0)}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(v.to_html(), exp)


class TestNumpyLike(unittest.TestCase):

    def test_scatter_xy(self):
        _skip_if_no_numpy()
        import numpy as np

        v = cesiumpy.Viewer(divid='viewertest')
        res = v.plot.scatter(np.array([130, 140, 150]), np.array([30, 40, 50]))
        self.assertIsInstance(v, cesiumpy.Viewer)

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(res.to_html(), exp)
        # entities must be added to original instance
        self.assertEqual(v.to_html(), exp)

    def test_scatter_array_interface(self):
        _skip_if_no_numpy()
        import numpy as np

        class ExtendedArray(object):

            def __init__(self, values):
                self.values = values

            def __array__(self):
                return np.array(self.values)

        v = cesiumpy.Viewer(divid='viewertest')
        res = v.plot.scatter(ExtendedArray([130, 140, 150]),
                             ExtendedArray([30, 40, 50]))
        self.assertIsInstance(v, cesiumpy.Viewer)

        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(130.0, 30.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(140.0, 40.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.entities.add({position : Cesium.Cartesian3.fromDegrees(150.0, 50.0, 0.0), point : {pixelSize : 10.0, color : Cesium.Color.WHITE}});
  widget.zoomTo(widget.entities);
</script>"""
        self.assertEqual(res.to_html(), exp)
        # entities must be added to original instance
        self.assertEqual(v.to_html(), exp)

if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
