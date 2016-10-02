#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import collections
import six
import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
from cesiumpy.entities.pinbuilder import Pin
import cesiumpy.entities.cartesian as cartesian
import cesiumpy.constants as constants
import cesiumpy.util.common as com
from cesiumpy.util.trait import MaybeTrait


class _CesiumEntity(_CesiumObject):

    # name and position should not be included,
    # because these are handled separetedly in _properties_dict
    _common_props = ['width', 'height', 'extrudedHeight', 'show', 'fill',
                     'material', 'color', 'outline', 'outlineColor', 'outlineWidth',
                     'numberOfVerticalLines', 'rotation', 'stRotation',
                     'granularity', 'scaleByDistance', 'translucencyByDistance',
                     'scale', 'horizontalOrigin', 'verticalOrigin',
                     'eyeOffset', 'pixelOffset', 'pixelOffsetScaleByDistance']

    width = traitlets.Float(allow_none=True)
    height = traitlets.Float(allow_none=True)
    extrudedHeight = traitlets.Float(allow_none=True)
    show = traitlets.Bool(allow_none=True)
    fill = traitlets.Bool(allow_none=True)

    material = MaybeTrait(klass=cesiumpy.entities.material.Material, allow_none=True)
    color = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)
    outline = traitlets.Bool(allow_none=True)
    outlineColor = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    outlineWidth = traitlets.Float(allow_none=True)
    numberOfVerticalLines = traitlets.Float(allow_none=True)
    rotation = traitlets.Float(allow_none=True)
    stRotation = traitlets.Float(allow_none=True)

    scale = traitlets.Float(allow_none=True)

    horizontalOrigin = traitlets.Instance(klass=constants.HorizontalOrigin, allow_none=True)
    verticalOrigin = traitlets.Instance(klass=constants.VerticalOrigin, allow_none=True)

    eyeOffset = MaybeTrait(klass=cartesian.Cartesian3, allow_none=True)
    pixelOffset = MaybeTrait(klass=cartesian.Cartesian2, allow_none=True)

    position = traitlets.Instance(klass=cartesian.Cartesian3, allow_none=True)

    def __init__(self, width=None, height=None, extrudedHeight=None,
                 show=None, fill=None, material=None, color=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 numberOfVerticalLines=None, rotation=None, stRotation=None,
                 granularity=None, scaleByDistance=None, translucencyByDistance=None,
                 scale=None, verticalOrigin=None, horizontalOrigin=None,
                 eyeOffset=None, pixelOffset=None, pixelOffsetScaleByDistance=None,
                 position=None, name=None):

        self.width = width
        self.height = height
        self.extrudedHeight = extrudedHeight
        self.show = show
        self.fill = fill

        # color, validated in setter
        self.material = material
        self.color = color

        self.outline = outline

        # color, validated in setter
        self.outlineColor = outlineColor

        self.outlineWidth = outlineWidth
        self.numberOfVerticalLines = numberOfVerticalLines
        self.rotation = rotation
        self.stRotation = stRotation

        self.granularity = com.notimplemented(granularity)
        self.scaleByDistance = com.notimplemented(scaleByDistance)
        self.translucencyByDistance = com.notimplemented(translucencyByDistance)

        self.scale = scale

        self.horizontalOrigin = horizontalOrigin
        self.verticalOrigin = verticalOrigin

        self.eyeOffset = eyeOffset
        self.pixelOffset = pixelOffset

        self.pixelOffsetScaleByDistance = com.notimplemented(pixelOffsetScaleByDistance)

        if position is not None:
            position = cartesian.Cartesian3.maybe(position, degrees=True)
        self.position = position

        self.name = name

    def copy(self):
        kwds = {}
        for key in self._props + self._common_props + ['name', 'position']:
            val = getattr(self, key)
            if val is not None:
                kwds[key] = val
        return self.__class__(**kwds)

    @property
    def _property_dict(self):
        props = collections.OrderedDict()
        props['name'] = self.name
        props['position'] = self.position

        # properties are handled in _CesiumInstance
        childs = super(_CesiumEntity, self)._property_dict
        for p in self._common_props:
            childs[p] = getattr(self, p)
        props[self._klass] = childs
        return props

    def __repr__(self):
        if self.position is not None:
            rep = """{klass}({x}, {y}, {z})"""
            return rep.format(klass=self.__class__.__name__, x=self.position.x,
                              y=self.position.y, z=self.position.z)

        elif self.positions is not None:
            rep = """{klass}({x})"""
            return rep.format(klass=self.__class__.__name__,
                              x=self.positions.x)
        else:
            # should be defined in each classes
            raise NotImplementedError


class Point(_CesiumEntity):
    """
    PointGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    color : Color, default WHITE
        A Property specifying the Color of the point.
    pixelSize : int, default 10
        A numeric Property specifying the size in pixels.
    outlineColor : Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth : int, default 0
        A numeric Property specifying the the outline width in pixels.
    show : bool, default True
        A boolean Property specifying the visibility of the point.
    scaleByDistance :
        A NearFarScalar Property used to scale the point based on distance.
    translucencyByDistance :
        A NearFarScalar Property used to set translucency based on distance from the camera.
    """

    _klass = 'point'
    # props should contains property which is unique in the class
    # (which is not included in _common_props)
    _props = ['pixelSize']

    pixelSize = traitlets.Float(allow_none=True)

    def __init__(self, position, color=None, pixelSize=10, outlineColor=None, outlineWidth=None,
                 show=None, scaleByDistance=None, translucencyByDistance=None,
                 name=None):

        if color is None:
            # Add default color explicitly to avoid all values to be None
            color = cesiumpy.color.WHITE
        if pixelSize is None:
            pixelSize = 10

        super(Point, self).__init__(show=show, color=color,
                                    outlineColor=outlineColor,
                                    outlineWidth=outlineWidth,
                                    scaleByDistance=scaleByDistance,
                                    translucencyByDistance=translucencyByDistance,
                                    position=position, name=name)

        self.pixelSize = pixelSize


class Label(_CesiumEntity):
    """
    LabelGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    text : str
        A Property specifying the text.
    font : str, default '10px sans-serif'
        A Property specifying the CSS font.
    style : LabeStyle, default LabelStyle.FILL
        A Property specifying the LabelStyle.
    fillColor : Color, default Color.WHITE
        A Property specifying the fill Color.
    outlineColor : Color, default, Color.BLACK
        A Property specifying the outline Color.
    outlineWidth : float, default 1.
        A numeric Property specifying the outline width.
    show : bool, default True
        A boolean Property specifying the visibility of the label.
    scale : float, default 1.
        A numeric Property specifying the scale to apply to the text.
    horizontalOrigin : HorizontalOrigin, default HorizontalOrigin.CENTER
        A Property specifying the HorizontalOrigin.
    verticalOrigin : VerticalOrigin, default VerticalOrigin.CENTER
        A Property specifying the VerticalOrigin.
    eyeOffset : Cartesian3, default Cartesian3.ZERO
        A Cartesian3 Property specifying the eye offset.
    pixelOffset : Cartesian2, default Cartesian2.ZERO
        A Cartesian2 Property specifying the pixel offset.
    translucencyByDistance :
        A NearFarScalar Property used to set translucency based on distance from the camera.
    pixelOffsetScaleByDistance :
        A NearFarScalar Property used to set pixelOffset based on distance from the camera.
    """
    _klass = 'label'
    _props = ['text', 'style', 'fillColor']

    text = traitlets.Unicode()
    fillColor = MaybeTrait(klass=cesiumpy.color.Color, allow_none=True)

    def __init__(self, position, text, style=None, fillColor=None,
                 outlineColor=None, outlineWidth=None, show=None,
                 scale=None, horizontalOrigin=None, verticalOrigin=None,
                 eyeOffset=None, pixelOffset=None, translucencyByDistance=None,
                 pixelOffsetScaleByDistance=None, name=None):

        super(Label, self).__init__(show=show, outlineColor=outlineColor,
                                    outlineWidth=outlineWidth,
                                    translucencyByDistance=translucencyByDistance,
                                    scale=scale, horizontalOrigin=horizontalOrigin,
                                    verticalOrigin=verticalOrigin,
                                    eyeOffset=eyeOffset, pixelOffset=pixelOffset,
                                    pixelOffsetScaleByDistance=pixelOffsetScaleByDistance,
                                    position=position, name=name)

        self.text = text
        self.style = com.notimplemented(style)
        self.fillColor = fillColor


class Billboard(_CesiumEntity):
    """
    PointGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    image : str or Pin, default Pin()
        A Property specifying the Image, URI, or Canvas to use for the billboard.
    show : bool, default True
        A boolean Property specifying the visibility of the billboard.
    scale : float, default 1.
        A numeric Property specifying the scale to apply to the image size.
    horizontalOrigin : HorizontalOrigin, default HorizontalOrigin.CENTER
        A Property specifying the HorizontalOrigin.
    verticalOrigin : VerticalOrigin, default VerticalOrigin.CENTER
        A Property specifying the VerticalOrigin.
    eyeOffset : Cartesian3, default Cartesian3.ZERO
        A Cartesian3 Property specifying the eye offset.
    pixelOffset : Cartesian2, default Cartesian2.ZERO
        A Cartesian2 Property specifying the pixel offset.
    rotation : float, default 0.
        A numeric Property specifying the rotation about the alignedAxis.
    alignedAxis : Cartesian3, default Cartesian3.ZERO
        A Cartesian3 Property specifying the axis of rotation.
    width : float
        A numeric Property specifying the width of the billboard in pixels, overriding the native size.
    height : float
        A numeric Property specifying the height of the billboard in pixels, overriding the native size.
    color : Color, default Color.WHITE
        A Property specifying the tint Color of the image.
    scaleByDistance :
        A NearFarScalar Property used to scale the point based on distance from the camera.
    translucencyByDistance :
        optional A NearFarScalar Property used to set translucency based on distance from the camera.
    pixelOffsetScaleByDistance :
        optional A NearFarScalar Property used to set pixelOffset based on distance from the camera.
    imageSubRegion :
        A Property specifying a BoundingRectangle that defines a sub-region of the image to use for the billboard, rather than the entire image.
    sizeInMeters : bool
        A boolean Property specifying whether this billboard's size should be measured in meters.
    """
    _klass = 'billboard'
    _props = ['image', 'alignedAxis', 'imageSubRegion', 'sizeInMeters']

    image = traitlets.Instance(klass=cesiumpy.entities.pinbuilder._BillboardContents)

    def __init__(self, position, image=None, show=None, scale=None,
                 horizontalOrigin=None, verticalOrigin=None,
                 eyeOffset=None, pixelOffset=None, rotation=None,
                 alignedAxis=None, width=None, height=None, color=None,
                 scaleByDistance=None, translucencyByDistance=None,
                 pixelOffsetScaleByDistance=None, imageSubRegion=None,
                 sizeInMeters=None, name=None):

        super(Billboard, self).__init__(show=show, scale=scale, color=color,
                                        horizontalOrigin=horizontalOrigin,
                                        verticalOrigin=verticalOrigin,
                                        eyeOffset=eyeOffset, pixelOffset=pixelOffset,
                                        rotation=rotation, width=width, height=height,
                                        scaleByDistance=scaleByDistance,
                                        translucencyByDistance=translucencyByDistance,
                                        pixelOffsetScaleByDistance=pixelOffsetScaleByDistance,
                                        position=position, name=name)
        if image is None:
            image = Pin()

        if isinstance(image, six.string_types):
            image = cesiumpy.entities.pinbuilder.Icon(image)
        self.image = image

        self.alignedAxis = com.notimplemented(alignedAxis)
        self.imageSubRegion = com.notimplemented(imageSubRegion)
        self.sizeInMeters = com.notimplemented(sizeInMeters)


class Ellipse(_CesiumEntity):
    """
    EllipseGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    semiMajorAxis : float
        The numeric Property specifying the semi-major axis.
    semiMinorAxis : float
        The numeric Property specifying the semi-minor axis.
    height : float, default 0.
        A numeric Property specifying the altitude of the ellipse.
    extrudedHeight : float, default 0.
        A numeric Property specifying the altitude of the ellipse extrusion.
    show : bool, default True
        A boolean Property specifying the visibility of the ellipse.
    fill : bool, default True
        A boolean Property specifying whether the ellipse is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the ellipse.
    outline : bool, default False
        A boolean Property specifying whether the ellipse is outlined.
    outlineColor : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    numberOfVerticalLines : int, default 16
        Property specifying the number of vertical lines to draw along the perimeter for the outline.
    rotation : float, default 0.
        A numeric property specifying the rotation of the ellipse counter-clockwise from north.
    stRotation : float, default 0.
        A numeric property specifying the rotation of the ellipse texture counter-clockwise from north.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between points on the ellipse.
    """

    _klass = 'ellipse'
    _props = ['semiMinorAxis', 'semiMajorAxis']

    semiMinorAxis = traitlets.Float()
    semiMajorAxis = traitlets.Float()

    def __init__(self, position, semiMinorAxis, semiMajorAxis, height=None,
                 extrudedHeight=None, show=None, fill=None, material=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 numberOfVerticalLines=None, rotation=None, stRotation=None,
                 name=None):

        super(Ellipse, self).__init__(height=height, extrudedHeight=extrudedHeight,
                                      show=show, fill=fill, material=material,
                                      outline=outline, outlineColor=outlineColor,
                                      outlineWidth=outlineWidth,
                                      numberOfVerticalLines=numberOfVerticalLines,
                                      rotation=rotation, stRotation=stRotation,
                                      position=position, name=name)

        self.semiMinorAxis = semiMinorAxis
        self.semiMajorAxis = semiMajorAxis


class Ellipsoid(_CesiumEntity):
    """
    EllipsoidGraphics

    Parameters
    ----------
    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    radii : Cartesian3
        A Cartesian3 Property specifying the radii of the ellipsoid.
    show : bool, default True
        A boolean Property specifying the visibility of the ellipsoid.
    fill : bool, default True
        A boolean Property specifying whether the ellipsoid is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the ellipsoid.
    outline : bool, default False
        A boolean Property specifying whether the ellipsoid is outlined.
    outlineColor : CeciumColor, BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    subdivisions : int, default 128
        A Property specifying the number of samples per outline ring, determining the granularity of the curvature.
    stackPartitions : int, default 64
        A Property specifying the number of stacks.
    slicePartitions : int, default 64
        A Property specifying the number of radial slices.
    """

    _klass = 'ellipsoid'
    _props = ['radii', 'subdivisions', 'stackPartitions', 'slicePartitions']

    radii = MaybeTrait(klass=cartesian.Cartesian3)
    subdivisions = traitlets.Float(allow_none=True)
    stackPartitions = traitlets.Float(allow_none=True)
    slicePartitions = traitlets.Float(allow_none=True)

    def __init__(self, position, radii, show=None, fill=None, material=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 subdivisions=None, stackPartitions=None, slicePartitions=None,
                 name=None):
        super(Ellipsoid, self).__init__(show=show, fill=fill, material=material,
                                        outline=outline, outlineColor=outlineColor,
                                        outlineWidth=outlineWidth,
                                        position=position, name=name)
        self.radii = radii
        self.subdivisions = subdivisions
        self.stackPartitions = stackPartitions
        self.slicePartitions = slicePartitions


class Cylinder(_CesiumEntity):
    """
    CylinderGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    length : float
        A numeric Property specifying the length of the cylinder.
    topRadius : float
        A numeric Property specifying the radius of the top of the cylinder.
    bottomRadius : float
        A numeric Property specifying the radius of the bottom of the cylinder.
    show : bool, default True
        A boolean Property specifying the visibility of the cylinder.
    fill : bool, default True
        A boolean Property specifying whether the cylinder is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the cylinder.
    outline : bool, default False
        A boolean Property specifying whether the cylinder is outlined.
    outlineColor : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    numberOfVerticalLines : int, default 16
        A numeric Property specifying the number of vertical lines to draw along the perimeter for the outline.
    slices : int, default 128
        The number of edges around perimeter of the cylinder.
    """

    _klass = 'cylinder'
    _props = ['length', 'topRadius', 'bottomRadius', 'slices']

    length = traitlets.Float()
    topRadius = traitlets.Float()
    bottomRadius = traitlets.Float()
    slices = traitlets.Float(allow_none=True)

    def __init__(self, position, length, topRadius, bottomRadius,
                 show=None, fill=None, material=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 numberOfVerticalLines=None, slices=None,
                 name=None):

        super(Cylinder, self).__init__(show=show, fill=fill, material=material,
                                       outline=outline, outlineColor=outlineColor,
                                       outlineWidth=outlineWidth,
                                       numberOfVerticalLines=numberOfVerticalLines,
                                       position=position, name=name)
        self.length = length
        self.topRadius = topRadius
        self.bottomRadius = bottomRadius
        self.slices = slices


class Polyline(_CesiumEntity):
    """
    PolylineGraphics

    Parameters
    ----------

    positions : Cartesian3
        A Property specifying the array of Cartesian3 positions that define the line strip.
    followSurface : bool, default True
        A boolean Property specifying whether the line segments should be great arcs or linearly connected.
    width : float, default 1.
        A numeric Property specifying the width in pixels.
    show : bool, default True
        A boolean Property specifying the visibility of the polyline.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to draw the polyline.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude if followSurface is true.
    """

    _klass = 'polyline'
    _props = ['positions', 'followSurface']

    positions = traitlets.Instance(klass=cartesian.Cartesian3Array)
    followSurface = traitlets.Bool(allow_none=True)

    def __init__(self, positions, followSurface=None, width=None,
                 show=None, material=None, granularity=None, name=None):
        # polyline uses "posisions", not "position"

        super(Polyline, self).__init__(width=width, show=show, material=material,
                                       granularity=granularity, name=name)

        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        self.followSurface = followSurface


class PolylineVolume(_CesiumEntity):
    """
    PolylineVolumeGraphics

    Parameters
    ----------

    positions : Cartesian3
        A Property specifying the array of Cartesian3 positions which define the line strip.
    shape : Cartesian2
        optional A Property specifying the array of Cartesian2 positions which define the shape to be extruded.
    cornerType : CornerType, default ROUNDED
        A CornerType Property specifying the style of the corners.
    show : bool, default True
        A boolean Property specifying the visibility of the volume.
    fill : bool, default True
        A boolean Property specifying whether the volume is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the volume.
    outline : bool, default False
        A boolean Property specifying whether the volume is outlined.
    outlineColor : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    """

    _klass = 'polylineVolume'
    _props = ['positions', 'shape', 'cornerType']

    positions = traitlets.Instance(klass=cartesian.Cartesian3Array)
    shape = traitlets.List(minlen=2)
    cornerType = traitlets.Instance(klass=constants.CornerType, allow_none=True)

    def __init__(self, positions, shape, cornerType=None, show=None,
                 fill=None, material=None, outline=None, outlineColor=None,
                 outlineWidth=None, granularity=None, name=None):
        # polylineVolume uses "posisions", not "position"

        super(PolylineVolume, self).__init__(show=show, fill=fill, material=material,
                                             outline=outline, outlineColor=outlineColor,
                                             outlineWidth=outlineWidth, granularity=granularity,
                                             name=name)

        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        self.shape = cartesian._maybe_cartesian2_list(shape, key='shape')
        self.cornerType = cornerType


class Corridor(_CesiumEntity):
    """
    CorridorGraphics

    Parameters
    ----------

    positions : Cartesian3
        A Property specifying the array of Cartesian3 positions that define the centerline of the corridor.
    width : float
        A numeric Property specifying the distance between the edges of the corridor.
    cornerType : CornerType, default CornerType.ROUNDED
        A CornerType Property specifying the style of the corners.
    height : float, default 0.
        A numeric Property specifying the altitude of the corridor.
    extrudedHeight : float, default 0.
        A numeric Property specifying the altitude of the corridor extrusion.
    show : bool, default True
        A boolean Property specifying the visibility of the corridor.
    fill : bool, default True
        A boolean Property specifying whether the corridor is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the corridor.
    outline : bool, default False
        A boolean Property specifying whether the corridor is outlined.
    outlineColor : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the distance between each latitude and longitude.
    """

    _klass = 'corridor'
    _props = ['positions', 'cornerType']

    positions = traitlets.Instance(klass=cartesian.Cartesian3Array)
    cornerType = traitlets.Instance(klass=constants.CornerType, allow_none=True)

    def __init__(self, positions, width, cornerType=None, height=None,
                 extrudedHeight=None, show=None, fill=None, material=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 granularity=None, name=None):
        # corridor uses "posisions", not "position"

        super(Corridor, self).__init__(width=width, height=height,
                                       extrudedHeight=extrudedHeight,
                                       show=show, fill=fill, material=material,
                                       outline=outline, outlineColor=outlineColor,
                                       outlineWidth=outlineWidth,
                                       granularity=granularity, name=name)

        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        self.cornerType = cornerType


class Wall(_CesiumEntity):
    """
    WallGraphics

    Parameters
    ----------

    positions : Cartesian3
        A Property specifying the array of Cartesian3 positions which define the top of the wall.
    maximumHeights : float or its list
        A Property specifying an array of heights to be used for the top of the wall instead of the height of each position.
    minimumHeights : float or its list
        A Property specifying an array of heights to be used for the bottom of the wall instead of the globe surface.
    show : bool, default True
        A boolean Property specifying the visibility of the wall.
    fill : bool, default True
        A boolean Property specifying whether the wall is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the wall.
    outline : bool, default False
        A boolean Property specifying whether the wall is outlined.
    outlineColor : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    """

    _klass = 'wall'
    _props = ['positions', 'maximumHeights', 'minimumHeights']

    positions = traitlets.Instance(klass=cartesian.Cartesian3Array)

    def __init__(self, positions, maximumHeights, minimumHeights, show=None,
                 fill=None, material=None, outline=None, outlineColor=None,
                 outlineWidth=None, granularity=None, name=None):
        # Wall uses "posisions", not "position"
        super(Wall, self).__init__(show=show, fill=fill, material=material,
                                   outline=outline, outlineColor=outlineColor,
                                   outlineWidth=outlineWidth, granularity=granularity,
                                   name=name)

        # ToDo: Support fromDegreesArrayHeights
        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        pos_len = len(self.positions) // 2

        def _init_heights(x, key):
            if not isinstance(x, list):
                com.validate_numeric(x, key=key)
                x = [x] * pos_len
            if len(x) != pos_len:
                msg = '{key} must has the half length ({pos_len}) of positions: {x}'
                raise ValueError(msg.format(key=key, pos_len=pos_len, x=len(maximumHeights)))
            return x

        self.maximumHeights = _init_heights(maximumHeights, key='maximumHeights')
        self.minimumHeights = _init_heights(minimumHeights, key='minimumHeights')


class Rectangle(_CesiumEntity):
    """
    RectangleGraphics

    Parameters
    ----------

    coordinates : list of 4 floats, corresponding to west, south, east, north
        The Property specifying the Rectangle.
    height : float, default 0.
        A numeric Property specifying the altitude of the rectangle.
    extrudedHeight : float, default 0.
        A numeric Property specifying the altitude of the rectangle extrusion.
    closeTop : bool, default True
        A boolean Property specifying whether the rectangle has a top cover when extruded
    closeBottom : bool, default True
        A boolean Property specifying whether the rectangle has a bottom cover when extruded.
    show : bool, default True
        A boolean Property specifying the visibility of the rectangle.
    fill : bool, default True
        A boolean Property specifying whether the rectangle is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the rectangle.
    outline : bool, default False
        A boolean Property specifying whether the rectangle is outlined.
    outlineColor : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    rotation : float, default 0.
        A numeric property specifying the rotation of the rectangle clockwise from north.
    stRotation : float, default 0.
        A numeric property specifying the rotation of the rectangle texture counter-clockwise from north.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between points on the rectangle.
    """

    _klass = 'rectangle'
    _props = ['coordinates', 'closeTop', 'closeBottom']

    coordinates = MaybeTrait(klass=cartesian.Rectangle)
    closeTop = traitlets.Bool(allow_none=True)
    closeBottom = traitlets.Bool(allow_none=True)

    def __init__(self, coordinates, height=None, extrudedHeight=None,
                 closeTop=None, closeBottom=None, show=None,
                 fill=None, material=None, outline=None, outlineColor=None,
                 outlineWidth=None, stRotation=None, granularity=None,
                 name=None):

        super(Rectangle, self).__init__(height=height, extrudedHeight=extrudedHeight,
                                        show=show, fill=fill, material=material,
                                        outline=outline, outlineColor=outlineColor,
                                        outlineWidth=outlineWidth, stRotation=stRotation,
                                        granularity=granularity, name=name)

        self.coordinates = coordinates
        self.closeTop = closeTop
        self.closeBottom = closeBottom

    def __repr__(self):
        rep = """{klass}({rep})""".format(klass=self.__class__.__name__,
                                          rep=self.coordinates._inner_repr)
        return rep


class Box(_CesiumEntity):
    """
    BoxGraphics

    Parameters
    ----------

    position : Cartesian3
        A Property specifying the Cartesian3 positions.
    dimensions : Cartesian3
        A Cartesian3 Property specifying the length, width, and height of the box.
    show : bool, default True
        A boolean Property specifying the visibility of the box.
    fill : bool, default True
        A boolean Property specifying whether the box is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the box.
    outline : bool, default False
        A boolean Property specifying whether the box is outlined.
    outlineColor : cesiumpy.cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    """

    _klass = 'box'
    _props = ['dimensions']

    dimensions = MaybeTrait(klass=cartesian.Cartesian3)

    def __init__(self, position, dimensions, show=None, fill=None, material=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 name=None):

        super(Box, self).__init__(show=show, fill=fill, material=material,
                                  outline=outline, outlineColor=outlineColor,
                                  outlineWidth=outlineWidth,
                                  position=position, name=name)
        self.dimensions = dimensions


class Polygon(_CesiumEntity):
    """
    PolygonGraphics

    Parameters
    ----------

    hierarchy : Cartesian3
        A Property specifying the PolygonHierarchy.
    height : float, default 0.
        A numeric Property specifying the altitude of the polygon.
    extrudedHeight : float, default 0.
        A numeric Property specifying the altitude of the polygon extrusion.
    show : bool, default True
        A boolean Property specifying the visibility of the polygon.
    fill : bool, default True
        A boolean Property specifying whether the polygon is filled with the provided material.
    material : cesiumpy.cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the polygon.
    outline : bool, default False
        A boolean Property specifying whether the polygon is outlined.
    outlineColor : cesiumpy.cesiumpy.color.Color, default cesiumpy.color.BLACK
        A Property specifying the Color of the outline.
    outlineWidth : float, default 1.
        A numeric Property specifying the width of the outline.
    stRotation : float, default 0.
        A numeric property specifying the rotation of the polygon texture counter-clockwise from north.
    granularity : float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    perPositionHeight : bool, default False
        A boolean specifying whether or not the the height of each position is used.
    """

    _klass = 'polygon'
    _props = ['hierarchy', 'perPositionHeight']

    perPositionHeight = traitlets.Bool(allow_none=True)

    def __init__(self, hierarchy, height=None, extrudedHeight=None, show=None,
                 fill=None, material=None, outline=None, outlineColor=None,
                 outlineWidth=None, stRotation=None, granularity=None,
                 perPositionHeight=None, name=None):

        super(Polygon, self).__init__(height=height, extrudedHeight=extrudedHeight,
                                      show=show, fill=fill, material=material,
                                      outline=outline, outlineColor=outlineColor,
                                      outlineWidth=outlineWidth, stRotation=stRotation,
                                      granularity=granularity, name=name)

        self.hierarchy = cartesian.Cartesian3.fromDegreesArray(hierarchy)
        self.perPositionHeight = perPositionHeight

    @property
    def positions(self):
        # for compat
        return self.hierarchy
