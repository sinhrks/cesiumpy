#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import json
import os
import six

import cesiumpy.common as com


class CesiumBase(object):

    def __init__(self, divid=None, width='100%', height='100%'):
        if divid is None:
            divid = 'container-{0}'.format(id(self))
        self.divid = divid

        # ToDo: Py3 compat
        if not isinstance(width, six.string_types):
            raise ValueError('height must be str: {0}'.format(type(width)))
        self.width = width

        if not isinstance(height, six.string_types):
            raise ValueError('height must be str: {0}'.format(type(height)))
        self.height = height

    @property
    def _load_scripts(self):
        js = """<script src="https://cesiumjs.org/Cesium/Build/Cesium/Cesium.js"></script>"""
        css = """<link rel="stylesheet" href="http://cesiumjs.org/Cesium/Build/CesiumUnminified/Widgets/CesiumWidget/CesiumWidget.css" type="text/css">"""
        return [js, css]

    @property
    def container(self):
        container = """<div id="{0}" style="width:{1}; height:{2};"><div>"""
        return container.format(self.divid, self.height, self.width)

    def _repr_html_(self):
        return self.to_html()

    def to_html(self):
        headers = self._load_scripts
        container = self.container
        script = self._wrap_js(self.script)

        results = self._build_html(headers, container, script)
        return results

    def _build_html(self, *args):
        results = []
        for a in args:
            if isinstance(a, list):
                results.extend(a)
            elif isinstance(a, (str, unicode)):
                results.append(a)
            else:
                raise ValueError(type(a))
        return os.linesep.join(results)

    @property
    def script(self):
        raise NotImplementedError

    def _wrap_js(self, script):
        if not isinstance(script, list):
            script = [script]
        script = self._add_indent(script)
        return ["""<script type="text/javascript">"""] + script + ["""</script>"""]

    def _add_indent(self, script, indent=2):
        """ Indent list of script with specfied number of spaces """
        if not isinstance(script, list):
            script = [script]

        indent = ' ' * indent
        return [indent + s for s in script]


class CesiumWidget(CesiumBase):

    @property
    def script(self):
        script = """var widget = new Cesium.CesiumWidget("{divid}");"""
        script = script.format(divid=self.divid)
        return script


class Viewer(CesiumBase):

    # ToDo: Fix the order and default to meet the cesium doc
    def __init__(self, divid=None, width='100%', height='100%',
                 animation=True,
                 baseLayerPicker=True, fullscreenButton=True,
                 geocoder=True, homeButton=True, infoBox=True, sceneModePicker=True,
                 selectionIndicator=True, navigationHelpButton=True,
                 timeline=True, navigationInstructionsInitiallyVisible=True):
        super(Viewer, self).__init__(divid=divid, width=width, height=height)

        self.options = dict(animation=animation,
                            baseLayerPicker=baseLayerPicker,
                            fullscreenButton=fullscreenButton,
                            geocoder=geocoder,
                            homeButton=homeButton,
                            infoBox=infoBox,
                            sceneModePicker=sceneModePicker,
                            selectionIndicator=selectionIndicator,
                            navigationHelpButton=navigationHelpButton,
                            timeline=timeline,
                            navigationInstructionsInitiallyVisible=navigationInstructionsInitiallyVisible)

        # ToDo: API to disable all flags to False
        # store cesium objects as entities
        self.entities = []

    @property
    def script(self):
        script = """var viewer = new Cesium.Viewer("{divid}", {options});"""
        script = script.format(divid=self.divid, options=json.dumps(self.options))
        return [script] + self._build_entities()

    def _build_entities(self):
        """
        return list of scripts built from entities
        each script may be a list of comamnds also
        """

        results = []
        for entity in self.entities:
            script = """viewer.entities.add({entity});""".format(entity=entity)
            results.append(script)

        return results

    def add(self, entity):
        from cesiumpy.entity import CesiumEntity
        if not isinstance(entity, CesiumEntity):
            msg = 'entity must be a CesiumEntity instance: {0}'
            raise ValueError(msg.format(type(entity)))

        self.entities.append(entity)

