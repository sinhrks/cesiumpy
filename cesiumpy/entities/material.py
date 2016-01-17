#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import six
import tempfile
import traitlets

from cesiumpy.base import _CesiumObject
import cesiumpy.common as com


class MaterialTrait(traitlets.Instance):

    def __init__(self, args=None, kw=None, **metadata):
        super(MaterialTrait, self).__init__(klass=Material, args=args, kw=kw,
                                         **metadata)

    def validate(self, obj, value):
        from cesiumpy.entities.color import _maybe_color
        value = _maybe_color(value)
        if isinstance(value, six.string_types):
            # regard value as image file path
            value = ImageMaterialProperty(value)
        return super(MaterialTrait, self).validate(obj, value)



class Material(_CesiumObject):
    pass


class ImageMaterialProperty(Material):
    """
    ImageMaterialProperty

    Parameters
    ----------

    image: str
        A Property specifying the Image, URL, Canvas, or Video.
    repeat: Cartesian2, default new Cartesian2(1.0, 1.0)
        A Cartesian2 Property specifying the number of times
    """

    _props = ['image', 'repeat']

    image = traitlets.Unicode()

    def __init__(self, image, repeat=None):
        self.image = image
        com._check_uri(self.image)

        self.repeat = com.notimplemented(repeat)

    def __repr__(self):
        rep = """ImageMaterialProperty({image})"""
        return rep.format(image=self.image)

    @property
    def script(self):
        props = super(ImageMaterialProperty, self).script
        return 'new Cesium.{klass}({props})'.format(klass=self.__class__.__name__,
                                                    props=props)


class TemporaryImageMaterialProperty(ImageMaterialProperty):
    """
    ImageMaterialProperty which can handle temporary image.
    Temporary image is output on the current working directory, and will be
    deleted when the instance is deleted.

    Parameters
    ----------

    figure: matplotlib.figure
        A matplotlib figure saved as temporary image
    repeat: Cartesian2, default new Cartesian2(1.0, 1.0)
        A Cartesian2 Property specifying the number of times
    """

    def __init__(self, figure, repeat=None):
        # using absolute path of tempfile doesn't work,
        # thus can't use NamedTemporaryFile
        _, tmp = tempfile.mkstemp(dir='.', suffix='.png')
        # store full path
        self.tempfile = tmp
        figure.savefig(self.tempfile, format="png", transparent=True)

        image = os.path.basename(tmp)
        super(TemporaryImageMaterialProperty, self).__init__(image, repeat=repeat)

        self.image = image
        com._check_uri(self.image)

    @property
    def script(self):
        props = super(ImageMaterialProperty, self).script
        return 'new Cesium.ImageMaterialProperty({props})'.format(props=props)

    def __del__(self):
        if os.path.exists(self.tempfile):
            os.remove(self.tempfile)

