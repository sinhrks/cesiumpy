#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six
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
