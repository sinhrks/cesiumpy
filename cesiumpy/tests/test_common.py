#!/usr/bin/env python
# coding: utf-8

import unittest
import nose

import cesiumpy
import cesiumpy.common as com


class TestChecker(unittest.TestCase):

    def test_isnumeric(self):
        self.assertTrue(com.is_numeric(10))
        self.assertTrue(com.is_numeric(1.5))

        self.assertFalse(com.is_numeric(None))
        self.assertFalse(com.is_numeric('1.5'))
        self.assertFalse(com.is_numeric([1.5]))

    def test_lon_lat(self):
        self.assertTrue(com.is_longitude(10))
        self.assertTrue(com.is_longitude(-180))
        self.assertTrue(com.is_longitude(180))
        self.assertTrue(com.is_longitude(10.))

        self.assertTrue(com.is_latitude(10))
        self.assertTrue(com.is_latitude(-90))
        self.assertTrue(com.is_latitude(90))
        self.assertTrue(com.is_latitude(10.))

        self.assertFalse(com.is_longitude(-181))
        self.assertFalse(com.is_latitude(-91))
        self.assertFalse(com.is_longitude(181))
        self.assertFalse(com.is_latitude(91))

        self.assertFalse(com.is_longitude('x'))
        self.assertFalse(com.is_latitude('x'))
        self.assertFalse(com.is_longitude([1]))
        self.assertFalse(com.is_latitude([1]))
        self.assertFalse(com.is_longitude((1, 2)))
        self.assertFalse(com.is_latitude((1, 2)))


class TestConverter(unittest.TestCase):

    def test_to_jsscalar(self):
        self.assertEqual('"x"', com.to_jsscalar('x'))
        self.assertEqual('true', com.to_jsscalar(True))
        self.assertEqual('false', com.to_jsscalar(False))
        self.assertEqual('[false, true]', com.to_jsscalar([False, True]))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
