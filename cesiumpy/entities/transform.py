#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
from cesiumpy.util.trait import MaybeTrait


class Transforms(_CesiumObject):

    origin = MaybeTrait(klass=cesiumpy.Cartesian3)
    transform = traitlets.Unicode()

    def __init__(self, origin, transform):
        self.origin = cesiumpy.Cartesian3.maybe(origin, degrees=True)
        # transformationmethod
        self.transform = transform

    @property
    def script(self):
        script = "Cesium.Transforms.{transform}({script})"
        return script.format(transform=self.transform,
                             script=self.origin.script)

    @classmethod
    def eastNorthUpToFixedFrame(cls, origin):
        """
        Computes a 4x4 transformation matrix from a reference frame with an
        east-north-up axes centered at the provided origin to the provided
        ellipsoid's fixed reference frame. The local axes are defined as:

        - The x axis points in the local east direction.
        - The y axis points in the local north direction.
        - The z axis points in the direction of the ellipsoid surface normal
        which passes through the position.

        Parameters
        ----------

        origin : Cartesian3
            The center point of the local reference frame.
        """
        return Transforms(origin, transform='eastNorthUpToFixedFrame')

    @classmethod
    def northEastDownToFixedFrame(cls, origin):
        """
        Computes a 4x4 transformation matrix from a reference frame with an
        north-east-down axes centered at the provided origin to the provided
        ellipsoid's fixed reference frame. The local axes are defined as:

        - The x axis points in the local north direction.
        - The y axis points in the local east direction.
        - The z axis points in the opposite direction of the ellipsoid surface
        normal which passes through the position.

        Parameters
        ----------

        origin : Cartesian3
            The center point of the local reference frame.
        """
        return Transforms(origin, transform='northEastDownToFixedFrame')

    @classmethod
    def northUpEastToFixedFrame(cls, origin):
        """
        Computes a 4x4 transformation matrix from a reference frame with an
        north-up-east axes centered at the provided origin to the provided
        ellipsoid's fixed reference frame. The local axes are defined as:

        - The x axis points in the local north direction.
        - The y axis points in the direction of the ellipsoid surface normal
          which passes through the position.
        - The z axis points in the local east direction.

        Parameters
        ----------

        origin : Cartesian3
            The center point of the local reference frame.
        """
        return Transforms(origin, transform='northUpEastToFixedFrame')
