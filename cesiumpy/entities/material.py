#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import six
import tempfile
import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
import cesiumpy.util.common as com
from cesiumpy.util.trait import URITrait


class Material(_CesiumObject):

    @classmethod
    def maybe(cls, x):
        try:
            x = cesiumpy.color.Color.maybe(x)
        except ValueError:
            pass

        if isinstance(x, six.string_types):
            # regard value as image file path
            x = ImageMaterialProperty(x)
        return x


class ImageMaterialProperty(Material):
    """
    ImageMaterialProperty

    Parameters
    ----------

    image : str
        A Property specifying the Image, URL, Canvas, or Video.
    repeat : Cartesian2, default new Cartesian2(1.0, 1.0)
        A Cartesian2 Property specifying the number of times
    """

    _props = ['image', 'repeat']
    image = URITrait()

    def __init__(self, image, repeat=None):
        if isinstance(image, TemporaryImage):
            image = image.script
        self.image = image
        self.repeat = com.notimplemented(repeat)

    def __repr__(self):
        rep = """ImageMaterialProperty({image})"""
        return rep.format(image=self.image)

    @property
    def script(self):
        props = super(ImageMaterialProperty, self).script
        return 'new Cesium.{klass}({props})'.format(klass=self.__class__.__name__,
                                                    props=props)


class TemporaryImage(_CesiumObject):
    """
    Receive an image and output a temp file

    Parameters
    ----------

    figure : matplotib Figure or Axes
        Instance to be drawn as an image.
        When trim is True, figure should only contain a single Axes.
    trim : bool, default True
        Whether to trim margins of
    """

    path = traitlets.Unicode()
    trim = traitlets.Bool()

    def __init__(self, figure, trim=True):
        _, tmp = tempfile.mkstemp(dir='.', suffix='.png')
        # store full path
        self.path = tmp
        self.trim = trim

        import matplotlib
        if not isinstance(figure, matplotlib.figure.Figure):
            # retrieve figure from Axes and AxesImage
            figure = getattr(figure, 'figure', figure)

        if isinstance(figure, matplotlib.figure.Figure):
            if trim and len(figure.axes) > 1:
                raise ValueError('Unable to trim a Figure contains multiple Axes')
            if trim:
                # result contains axis labels without this
                figure.axes[0].set_axis_off()
                figure.savefig(self.path, format="png", transparent=True,
                               bbox_inches='tight', pad_inches=0)
            else:
                figure.savefig(self.path, format="png", transparent=True)
        else:
            raise ValueError(figure)

    @property
    def script(self):
        return '{0}'.format(os.path.basename(self.path))

    def __del__(self):
        if os.path.exists(self.path):
            os.remove(self.path)
