#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six
import traitlets

import cesiumpy.util.common as com
import cesiumpy.util.html as html
from cesiumpy.util.trait import _JavaScriptObject, _JavaScriptEnum, _DIV


class _CesiumObject(_JavaScriptObject):

    @property
    def _klass(self):
        return "Cesium.{0}".format(self.__class__.__name__)


class _CesiumEnum(_JavaScriptEnum):
    pass


class _CesiumBase(_CesiumObject):
    """
    Base class for Cesium Widget / Viewer
    """

    _props = ['clock', 'imageryProvider', 'terrainProvider',
              'skyBox', 'skyAtmosphere', 'sceneMode',
              'scene3DOnly', 'orderIndependentTranslucency',
              'mapProjection', 'globe', 'useDefaultRenderLoop',
              'targetFrameRate', 'showRenderLoopErrors',
              'contextOptions', 'creditContainer',
              'terrainExaggeration']
    _varname = 'widget'

    width = traitlets.Unicode()
    height = traitlets.Unicode()

    scene3DOnly = traitlets.Bool(allow_none=True)
    orderIndependentTranslucency = traitlets.Bool(allow_none=True)

    useDefaultRenderLoop = traitlets.Bool(allow_none=True)
    targetFrameRate = traitlets.Float(allow_none=True)
    showRenderLoopErrors = traitlets.Bool(allow_none=True)

    terrainExaggeration = traitlets.Float(allow_none=True)

    def __init__(self, divid=None, width='100%', height='100%',
                 clock=None, imageryProvider=None, terrainProvider=None,
                 skyBox=None, skyAtmosphere=None, sceneMode=None,
                 scene3DOnly=None, orderIndependentTranslucency=None,
                 mapProjection=None, globe=None, useDefaultRenderLoop=None,
                 targetFrameRate=None, showRenderLoopErrors=None,
                 contextOptions=None, creditContainer=None,
                 terrainExaggeration=None):

        self.div = _DIV(divid=divid, width=width, height=height)

        self.clock = com.notimplemented(clock)

        self.imageryProvider = imageryProvider
        self.terrainProvider = terrainProvider

        self.skyBox = com.notimplemented(skyBox)
        self.skyAtmosphere = com.notimplemented(skyAtmosphere)
        self.sceneMode = com.notimplemented(sceneMode)

        self.scene3DOnly = scene3DOnly
        self.orderIndependentTranslucency = orderIndependentTranslucency

        self.mapProjection = com.notimplemented(mapProjection)
        self.globe = com.notimplemented(globe)

        self.useDefaultRenderLoop = useDefaultRenderLoop
        self.targetFrameRate = targetFrameRate
        self.showRenderLoopErrors = showRenderLoopErrors

        self.contextOptions = com.notimplemented(contextOptions)
        self.creditContainer = com.notimplemented(creditContainer)

        self.terrainExaggeration = terrainExaggeration

        from cesiumpy.camera import Camera
        self._camera = Camera(self)

        from cesiumpy.scene import Scene
        self._scene = Scene(self)

        from cesiumpy.entities.entity import _CesiumEntity
        self._entities = RistrictedList(self, allowed=_CesiumEntity,
                                        propertyname='entities')
        from cesiumpy.datasource import DataSource
        self._dataSources = RistrictedList(self, allowed=DataSource,
                                           propertyname='dataSources')

        self._scripts = RistrictedList(self, allowed=six.string_types,
                                       propertyname='script')

    @property
    def _load_scripts(self):
        js = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>"""
        css = """<link rel="stylesheet" href="https://cesiumjs.org/Cesium/Build/Cesium/Widgets/widgets.css" type="text/css">"""

        return [js, css]

    @property
    def container(self):
        return self.div.script

    def _repr_html_(self):
        return self.to_html()

    def to_html(self):
        headers = self._load_scripts
        container = self.container
        script = html._wrap_script(self.script)

        results = html._build_html(headers, container, script)
        return results

    @property
    def script(self):
        props = com.to_jsobject(self._property_dict)
        props = ''.join(props)
        if props != '':
            script = """var {varname} = new {klass}("{divid}", {props});"""
            script = script.format(varname=self._varname, klass=self._klass,
                                   divid=self.div.divid, props=''.join(props))
        else:
            script = """var {varname} = new {klass}("{divid}");"""
            script = script.format(varname=self._varname, klass=self._klass,
                                   divid=self.div.divid)
        return ([script] +
                self._entities.script +
                self._dataSources.script +
                [self._camera_script] +
                self._scene.script +
                self.scripts._items
                )

    @property
    def camera(self):
        return self._camera

    @property
    def _camera_script(self):
        camera = self.camera.script
        if camera != '':
            script = """{varname}.camera.flyTo({camera});"""
            script = script.format(varname=self._varname,
                                   camera=camera)
            return script
        elif len(self.entities) > 0:
            # zoom to added entities
            script = "{varname}.zoomTo({varname}.entities);"
            return script.format(varname=self._varname)
        else:
            return ''

    @property
    def entities(self):
        return self._entities

    @property
    def dataSources(self):
        return self._dataSources

    @property
    def scene(self):
        return self._scene

    @property
    def scripts(self):
        return self._scripts


class RistrictedList(_CesiumObject):

    widget = traitlets.Instance(klass=_CesiumBase)

    def __init__(self, widget, allowed, propertyname):
        self.widget = widget

        self._items = []
        self._allowed = allowed
        self._propertyname = propertyname

    def add(self, item, **kwargs):
        if com.is_listlike(item):
            for i in item:
                self.add(i, **kwargs)
        elif isinstance(item, self._allowed):
            for key, value in six.iteritems(kwargs):
                setattr(item, key, value)
            self._items.append(item)
        else:
            msg = 'item must be {allowed} instance: {item}'

            if isinstance(self._allowed, tuple):
                allowed = ', '.join([a.__name__ for a in self._allowed])
            else:
                allowed = self._allowed

            raise ValueError(msg.format(allowed=allowed, item=item))

    def clear(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]

    @property
    def script(self):
        """
        return list of scripts built from entities
        each script may be a list of comamnds also
        """
        results = []
        for item in self._items:
            script = """{varname}.{propertyname}.add({item});"""
            script = script.format(varname=self.widget._varname,
                                   propertyname=self._propertyname,
                                   item=item.script)
            results.append(script)
        return results
