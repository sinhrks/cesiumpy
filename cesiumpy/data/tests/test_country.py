#!/usr/bin/env python
# coding: utf-8

import nose
import unittest

import traitlets

import cesiumpy
from cesiumpy.testing import _skip_if_no_shapely


class TestCountry(unittest.TestCase):

    def test_country_getattr_error(self):
        msg = "Unable to load country data, file not found: 'X'"
        with nose.tools.assert_raises_regexp(AttributeError, msg):
            cesiumpy.countries.X

    def test_country_jpn(self):
        _skip_if_no_shapely()
        import shapely.geometry

        jpn = cesiumpy.countries.jpn
        self.assertIsInstance(jpn, list)
        self.assertTrue(all([isinstance(e, cesiumpy.Polygon) for e in jpn]))

        jpn = cesiumpy.countries.JPN
        self.assertIsInstance(jpn, list)
        self.assertTrue(all([isinstance(e, cesiumpy.Polygon) for e in jpn]))

    def test_viewer(self):
        _skip_if_no_shapely()
        v = cesiumpy.Viewer(divid='viewertest')
        v.entities.add(cesiumpy.countries.abw)
        res = v.to_html()
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>
<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="viewertest" style="width:100%; height:100%;"><div>
<script type="text/javascript">
  var widget = new Cesium.Viewer("viewertest");
  widget.entities.add({polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([-69.882233, 12.41111, -69.946945, 12.436666, -70.056122, 12.534443, -70.059448, 12.538055, -70.060287, 12.544167, -70.063339, 12.621666, -70.063065, 12.628611, -70.058899, 12.631109, -70.053345, 12.629721, -70.035278, 12.61972, -70.031113, 12.616943, -69.932236, 12.528055, -69.896957, 12.480833, -69.891403, 12.472221, -69.885559, 12.457777, -69.873901, 12.421944, -69.873337, 12.415833, -69.876114, 12.411665, -69.882233, 12.41111])}});
  widget.zoomTo(widget.entities);
</script>"""



if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
