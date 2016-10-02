#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

from cesiumpy.base import _CesiumObject
from cesiumpy.entities.transform import Transforms
import cesiumpy.util.common as com
from cesiumpy.util.trait import URITrait


class Model(_CesiumObject):
    """
    3D Model

    Parameters
    ----------

    url : str
        The object for the glTF JSON or an arraybuffer of Binary glTF defined by the KHR_binary_glTF extension.
    modelMatrix : Matrix4, default Matrix4.IDENTITY
        The 4x4 transformation matrix that transforms the model from model to world coordinates.
    basePath : str, default ''
        The base path that paths in the glTF JSON are relative to.
    show : bool, default True
        Determines if the model primitive will be shown.
    scale : float, default 1.0
        A uniform scale applied to this model.
    minimumPixelSize : float, default 0.0
        The approximate minimum pixel size of the model regardless of zoom.
    maximumScale : float
        The maximum scale size of a model. An upper limit for minimumPixelSize.
    id :
        A user-defined object to return when the model is picked with Scene#pick.
    allowPicking : bool, default True
        When true, each glTF mesh and primitive is pickable with Scene#pick.
    incrementallyLoadTextures : bool, default True
        Determine if textures may continue to stream in after the model is loaded.
    asynchronous : bool, default True
        Determines if model WebGL resource creation will be spread out over several frames or block until completion once all glTF files are loaded.
    debugShowBoundingVolume : bool, default False
        For debugging only. Draws the bounding sphere for each draw command in the model.
    debugWireframe : bool, default False
        For debugging only. Draws the model in wireframe.
    """

    _props = ['url', 'basePath', 'show', 'modelMatrix', 'scale',
              'minimumPixelSize', 'maximumScale', 'id', 'allowPicking',
              'incrementallyLoadTextures', 'asynchronous',
              'debugShowBoundingVolume', 'debugWireframe']

    url = URITrait()
    modelMatrix = traitlets.Instance(klass=Transforms)

    basePath = traitlets.Unicode(allow_none=True)
    show = traitlets.Bool(allow_none=True)
    scale = traitlets.Float(allow_none=True)
    minimumPixelSize = traitlets.Float(allow_none=True)
    maximumScale = traitlets.Float(allow_none=True)

    allowPicking = traitlets.Bool(allow_none=True)
    incrementallyLoadTextures = traitlets.Bool(allow_none=True)
    asynchronous = traitlets.Bool(allow_none=True)
    debugShowBoundingVolume = traitlets.Bool(allow_none=True)
    debugWireframe = traitlets.Bool(allow_none=True)

    def __init__(self, url, modelMatrix, basePath=None, show=None,
                 scale=None, minimumPixelSize=None, maximumScale=None,
                 id=None, allowPicking=None, incrementallyLoadTextures=None,
                 asynchronous=None, debugShowBoundingVolume=None,
                 debugWireframe=None):

        self.url = url

        self.modelMatrix = Transforms.eastNorthUpToFixedFrame(modelMatrix)

        self.basePath = basePath
        self.show = show
        self.scale = scale
        self.minimumPixelSize = minimumPixelSize
        self.maximumScale = maximumScale
        self.id = com.notimplemented(id)
        self.allowPicking = allowPicking
        self.incrementallyLoadTextures = incrementallyLoadTextures
        self.asynchronous = asynchronous
        self.debugShowBoundingVolume = debugShowBoundingVolume
        self.debugWireframe = debugWireframe

    def __repr__(self):
        rep = """{klass}("{url}")"""
        return rep.format(klass=self.__class__.__name__, url=self.url)

    @property
    def script(self):
        script = """Cesium.Model.fromGltf({script})"""
        return script.format(script=super(Model, self).script)
