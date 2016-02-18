#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import traitlets

import cesiumpy


class TestPinBuilder(unittest.TestCase):

    def test_pinbuilder_default(self):
        p = cesiumpy.Pin()
        exp = """new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48.0)"""
        self.assertEqual(p.script, exp)

    def test_pinbuilder_fromtext(self):
        p = cesiumpy.Pin.fromText('?')
        exp = """new Cesium.PinBuilder().fromText("?", Cesium.Color.ROYALBLUE, 48.0)"""
        self.assertEqual(p.script, exp)

        p = cesiumpy.Pin.fromText('!', color='red', size=52)
        exp = """new Cesium.PinBuilder().fromText("!", Cesium.Color.RED, 52.0)"""
        self.assertEqual(p.script, exp)

        msg = "The 'text' trait of an Unicode instance must be a unicode string"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Pin.fromText(None, color='red', size=52)

    def test_pinbuilder_fromcolor(self):
        p = cesiumpy.Pin.fromColor('red')
        exp = """new Cesium.PinBuilder().fromColor(Cesium.Color.RED, 48.0)"""
        self.assertEqual(p.script, exp)

        p = cesiumpy.Pin.fromColor('green', size=25)
        exp = """new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 25.0)"""
        self.assertEqual(p.script, exp)

        msg = "The 'color' trait of a Pin instance must be a Color"
        with nose.tools.assert_raises_regexp(traitlets.TraitError, msg):
            cesiumpy.Pin.fromColor('xyz')

    def test_pinbuilder_repr(self):
        p = cesiumpy.Pin('red')
        exp = """Pin(Color.RED, 48.0)"""
        self.assertEqual(repr(p), exp)

        p = cesiumpy.Pin.fromText('xxx', color='red')
        exp = """Pin("xxx", Color.RED, 48.0)"""
        self.assertEqual(repr(p), exp)

        p = cesiumpy.Pin.fromText('xxx', color='red', size=10)
        exp = """Pin("xxx", Color.RED, 10.0)"""
        self.assertEqual(repr(p), exp)


if __name__ == '__main__':
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
