#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import six

import cesiumpy


class TestPinBuilder(unittest.TestCase):

    def test_pinbuilder_default(self):
        p = cesiumpy.Pin()
        exp = """new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48)"""
        self.assertEqual(p.script, exp)

    def test_pinbuilder_fromtext(self):
        p = cesiumpy.Pin.fromText('?')
        exp = """new Cesium.PinBuilder().fromText("?", Cesium.Color.ROYALBLUE, 48)"""
        self.assertEqual(p.script, exp)

        p = cesiumpy.Pin.fromText('!', color='red', size=52)
        exp = """new Cesium.PinBuilder().fromText("!", Cesium.Color.RED, 52)"""
        self.assertEqual(p.script, exp)

    def test_pinbuilder_fromcolor(self):
        p = cesiumpy.Pin.fromColor('red')
        exp = """new Cesium.PinBuilder().fromColor(Cesium.Color.RED, 48)"""
        self.assertEqual(p.script, exp)

        p = cesiumpy.Pin.fromColor('green', size=25)
        exp = """new Cesium.PinBuilder().fromColor(Cesium.Color.GREEN, 25)"""
        self.assertEqual(p.script, exp)

    def test_pinbuilder_repr(self):
        p = cesiumpy.Pin('red')
        exp = """Pin(Cesium.Color.RED, 48)"""
        self.assertEqual(repr(p), exp)

        p = cesiumpy.Pin.fromText('xxx', color='red')
        exp = """Pin("xxx", Cesium.Color.RED, 48)"""
        self.assertEqual(repr(p), exp)

        p = cesiumpy.Pin.fromText('xxx', color='red', size=10)
        exp = """Pin("xxx", Cesium.Color.RED, 10)"""
        self.assertEqual(repr(p), exp)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
