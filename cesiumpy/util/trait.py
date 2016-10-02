#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import collections
import traitlets

from enum import Enum

import cesiumpy.util.common as com
import cesiumpy.util.html as html


class MaybeTrait(traitlets.Instance):

    def validate(self, obj, value):
        if self.allow_none is True and value is None:
            return super(MaybeTrait, self).validate(obj, value)

        try:
            value = self.klass.maybe(value)
        except ValueError:
            self.error(obj, value)
        return super(MaybeTrait, self).validate(obj, value)


class URITrait(traitlets.Unicode):

    def validate(self, obj, value):
        if self.allow_none is True and value is None:
            return super(URITrait, self).validate(obj, value)

        if not html._check_uri(value):
            self.error(obj, value)
        return super(URITrait, self).validate(obj, value)


# --------------------------------------------------
# Container
# --------------------------------------------------


class _HTMLObject(traitlets.HasTraits):

    def __eq__(self, other):
        # conmpare with script
        if isinstance(other, _HTMLObject):
            return self.script == other.script
        return False

    @property
    def script(self):
        raise NotImplementedError


class _JavaScriptObject(_HTMLObject):
    """
    Base class for JavaScript instances, which can be converted to
    JavaScript instance
    """

    @property
    def _klass(self):
        raise NotImplementedError('must be overriden in child classes')
        return "Cesium.{0}".format(self.__class__.__name__)

    @property
    def _props(self):
        raise NotImplementedError('must be overriden in child classes')

    @property
    def _property_dict(self):
        props = collections.OrderedDict()
        for p in self._props:
            props[p] = getattr(self, p)
        return props

    @property
    def script(self):
        props = self._property_dict
        results = com.to_jsobject(props)
        return ''.join(results)


class _JavaScriptEnum(Enum):

    @property
    def script(self):
        return self.value


class _DIV(_HTMLObject):

    divid = traitlets.Unicode()
    width = traitlets.Unicode()
    height = traitlets.Unicode()

    def __init__(self, divid=None, width='100%', height='100%'):

        if divid is None:
            divid = 'container-{0}'.format(id(self))
        self.divid = divid

        self.width = width
        self.height = height

    @property
    def script(self):
        container = """<div id="{0}" style="width:{1}; height:{2};"><div>"""
        return container.format(self.divid, self.width, self.height)
