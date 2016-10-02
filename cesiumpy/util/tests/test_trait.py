#!/usr/bin/env python
# coding: utf-8

import unittest

from cesiumpy.util.trait import _DIV


class TestTrait(unittest.TestCase):

    def test_div(self):
        div1 = _DIV()
        div2 = _DIV()
        self.assertNotEqual(div1, div2)

        div1 = _DIV(divid='xxx')
        div2 = _DIV(divid='xxx')
        self.assertEqual(div1, div2)

        self.assertEqual(div1.script, """<div id="xxx" style="width:100%; height:100%;"><div>""")

        div = _DIV(divid='xxx', width='90%', height='60%')
        self.assertEqual(div.script, """<div id="xxx" style="width:90%; height:60%;"><div>""")
