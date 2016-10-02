#!/usr/bin/env python
# coding: utf-8

import unittest

import cesiumpy.util.html as html


class TestHTML(unittest.TestCase):

    def test_wrap_uri(self):
        res = html._wrap_uri("https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js")
        exp = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>"""
        self.assertEqual(res, exp)

        res = html._wrap_uri("http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css")
        exp = """<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">"""
        self.assertEqual(res, exp)

    def test_wrap_script(self):
        res = html._wrap_script('aaa')
        exp = ['<script type="text/javascript">', '  aaa', '</script>']
        self.assertEqual(res, exp)

        res = html._wrap_script(['aaa', 'bbb'])
        exp = ['<script type="text/javascript">', '  aaa', '  bbb', '</script>']
        self.assertEqual(res, exp)

    def test_add_indent(self):
        res = html._add_indent('aaa')
        exp = ['  aaa']
        self.assertEqual(res, exp)

        res = html._add_indent(['aaa', 'bbb'])
        exp = ['  aaa', '  bbb']
        self.assertEqual(res, exp)

        res = html._add_indent(['aaa', 'bbb'], indent=3)
        exp = ['   aaa', '   bbb']
        self.assertEqual(res, exp)
