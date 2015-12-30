#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six

from cesiumpy.base import _CesiumInstance
import cesiumpy.cartesian as cartesian
import cesiumpy.color as color
import cesiumpy.common as com


import collections


class _CesiumEntity(_CesiumInstance):

    # name and position should not be included,
    # because these are handled separetedly in _properties_dict
    _common_props = ['width', 'height', 'extrudedHeight', 'show', 'fill',
                     'material', 'outline', 'outlineColor', 'outlineWidth',
                     'numberOfVerticalLines', 'rotation', 'stRotation',
                     'granularity']

    def __init__(self, width=None, height=None, extrudedHeight=None,
                 show=None, fill=None, material=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 numberOfVerticalLines=None, rotation=None, stRotation=None,
                 granularity=None,
                 position=None, name=None):

        self.width = com.validate_numeric_or_none(width, key='width')
        self.height = com.validate_numeric_or_none(height, key='height')
        self.extrudedHeight = com.validate_numeric_or_none(extrudedHeight, key='extrudedHeight')
        self.show = com.validate_bool_or_none(show, key='show')
        self.fill = com.validate_bool_or_none(fill, key='fill')

        if material is not None:
            material = color._maybe_color(material)
            if not isinstance(material, color.Color):
                msg = 'material must be a Color instance: {0}'
                raise ValueError(msg.format(type(material)))
        self.material = material

        self.outline = com.validate_bool_or_none(outline, key='outline')

        if outlineColor is not None:
            outlineColor = color._maybe_color(outlineColor)
            if not isinstance(outlineColor, color.Color):
                msg = 'material must be a Color instance: {0}'
                raise ValueError(msg.format(type(outlineColor)))
        self.outlineColor = outlineColor

        self.outlineWidth = com.validate_numeric_or_none(outlineWidth, key='outlineWidth')
        self.numberOfVerticalLines = com.validate_numeric_or_none(numberOfVerticalLines, key='numberOfVerticalLines')
        self.rotation = com.validate_numeric_or_none(rotation, key='rotation')
        self.stRotation = com.validate_numeric_or_none(stRotation, key='stRotation')
        if granularity is not None:
            raise NotImplementedError
        self.granularity = granularity

        if position is not None:
            position = cartesian._maybe_cartesian_degrees(position)
            if not isinstance(position, cartesian.Cartesian3):
                msg = 'position must be Cartesian3 or its compat: {0}'
                raise ValueError(msg.format(position))
        self.position = position

        self.name = name
        # ToDo: instanciate corredt Cartesian from input

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


class Ellipse(_CesiumEntity):
    """ EllipseGraphics

    Parameters
    ----------

    position: Cartesian3
        A Property specifying the Cartesian3 positions.
    semiMajorAxis: float
        The numeric Property specifying the semi-major axis.
    semiMinorAxis: float
        The numeric Property specifying the semi-minor axis.
    height: float, default 0.
        A numeric Property specifying the altitude of the ellipse.
    extrudedHeight: float, default 0.
        A numeric Property specifying the altitude of the ellipse extrusion.
    show: bool, default True
        A boolean Property specifying the visibility of the ellipse.
    fill: bool, default True
        A boolean Property specifying whether the ellipse is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the ellipse.
    outline: bool, default False
        A boolean Property specifying whether the ellipse is outlined.
    outlineColor: cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    numberOfVerticalLines: int, default 16
        Property specifying the number of vertical lines to draw along the perimeter for the outline.
    rotation: float, default 0.
        A numeric property specifying the rotation of the ellipse counter-clockwise from north.
    stRotation: float, default 0.
        A numeric property specifying the rotation of the ellipse texture counter-clockwise from north.
    granularity: float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between points on the ellipse.
    """

    _klass = 'ellipse'
    _props = ['semiMinorAxis', 'semiMajorAxis']

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
        self.semiMinorAxis = com.validate_numeric(semiMinorAxis, key='semiMinorAxis')
        self.semiMajorAxis = com.validate_numeric(semiMajorAxis, key='semiMajorAxis')


class Ellipsoid(_CesiumEntity):
    """ EllipsoidGraphics

    Parameters
    ----------
    position: Cartesian3
        A Property specifying the Cartesian3 positions.
    radii: Cartesian3
        A Cartesian3 Property specifying the radii of the ellipsoid.
    show: bool, default True
        A boolean Property specifying the visibility of the ellipsoid.
    fill: bool, default True
        A boolean Property specifying whether the ellipsoid is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the ellipsoid.
    outline: bool, default False
        A boolean Property specifying whether the ellipsoid is outlined.
    outlineColor: CeciumColor, BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    subdivisions: int, default 128
        A Property specifying the number of samples per outline ring, determining the granularity of the curvature.
    stackPartitions: int, default 64
        A Property specifying the number of stacks.
    slicePartitions: int, default 64
        A Property specifying the number of radial slices.
    """

    _klass = 'ellipsoid'
    _props = ['radii', 'subdivisions', 'stackPartitions', 'slicePartitions']

    def __init__(self, position, radii, show=None, fill=None, material=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 subdivisions=None, stackPartitions=None, slicePartitions=None,
                 name=None):
        super(Ellipsoid, self).__init__(show=show, fill=fill, material=material,
                                        outline=outline, outlineColor=outlineColor,
                                        outlineWidth=outlineWidth,
                                        position=position, name=name)
        radii = cartesian._maybe_cartesian(radii)
        if not isinstance(radii, cartesian.Cartesian3):
            msg = 'radii must be Cartesian3 or its compat: {0}'
            raise ValueError(msg.format(radii))
        self.radii = radii

        self.subdivisions = com.validate_numeric_or_none(subdivisions, key='subdivisions')
        self.stackPartitions = com.validate_numeric_or_none(stackPartitions, key='stackPartitions')
        self.slicePartitions = com.validate_numeric_or_none(slicePartitions, key='slicePartitions')


class Cylinder(_CesiumEntity):
    """ CylinderGraphics

    Parameters
    ----------

    position: Cartesian3
        A Property specifying the Cartesian3 positions.
    length: float
        A numeric Property specifying the length of the cylinder.
    topRadius: float
        A numeric Property specifying the radius of the top of the cylinder.
    bottomRadius: float
        A numeric Property specifying the radius of the bottom of the cylinder.
    show: bool, default True
        A boolean Property specifying the visibility of the cylinder.
    fill: bool, default True
        A boolean Property specifying whether the cylinder is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the cylinder.
    outline: bool, default False
        A boolean Property specifying whether the cylinder is outlined.
    outlineColor: cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    numberOfVerticalLines: int, default 16
        A numeric Property specifying the number of vertical lines to draw along the perimeter for the outline.
    slices: int, default 128
        The number of edges around perimeter of the cylinder.
    """

    _klass = 'cylinder'
    _props = ['length', 'topRadius', 'bottomRadius', 'slices']

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
        self.length = com.validate_numeric(length, key='length')
        self.topRadius = com.validate_numeric(topRadius, key='topRadius')
        self.bottomRadius = com.validate_numeric(bottomRadius, key='bottomRadius')
        self.slices = com.validate_numeric_or_none(slices, key='slices')


class Polyline(_CesiumEntity):
    """ PolylineGraphics

    Parameters
    ----------

    positions: Cartesian3
        A Property specifying the array of Cartesian3 positions that define the line strip.
    followSurface: bool, default True
        A boolean Property specifying whether the line segments should be great arcs or linearly connected.
    width: float, default 1.
        A numeric Property specifying the width in pixels.
    show: bool, default True
        A boolean Property specifying the visibility of the polyline.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to draw the polyline.
    granularity: float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude if followSurface is true.
    """

    _klass = 'polyline'
    _props = ['positions', 'followSurface']

    def __init__(self, positions, followSurface=None, width=None,
                 show=None, material=None, granularity=None, name=None):
        # polyline uses "posisions", not "position"

        super(Polyline, self).__init__(width=width, show=show, material=material,
                                       granularity=granularity, name=name)

        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)
        self.followSurface = com.validate_bool_or_none(followSurface, key='followSurface')


class PolylineVolume(_CesiumEntity):
    """ PolylineVolumeGraphics

    Parameters
    ----------

    positions: Cartesian3
        A Property specifying the array of Cartesian3 positions which define the line strip.
    shape: Cartesian2
        optional A Property specifying the array of Cartesian2 positions which define the shape to be extruded.
    cornerType: CornerType, default ROUNDED
        A CornerType Property specifying the style of the corners.
    show: bool, default True
        A boolean Property specifying the visibility of the volume.
    fill: bool, default True
        A boolean Property specifying whether the volume is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the volume.
    outline: bool, default False
        A boolean Property specifying whether the volume is outlined.
    outlineColor: cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    granularity: float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    """

    _klass = 'polylineVolume'
    _props = ['positions', 'shape', 'cornerType']

    def __init__(self, positions, shape, cornerType=None, show=None,
                 fill=None, material=None, outline=None, outlineColor=None,
                 outlineWidth=None, granularity=None, name=None):
        # polylineVolume uses "posisions", not "position"

        super(PolylineVolume, self).__init__(show=show, fill=fill, material=material,
                                             outline=outline, outlineColor=outlineColor,
                                             outlineWidth=outlineWidth, granularity=granularity,
                                             name=name)

        self.positions = cartesian.Cartesian3.fromDegreesArray(positions)

        # ToDo: automatic conversion from numeric list
        shape = cartesian._maybe_cartesian2_list(shape)
        self.shape = shape

        if cornerType is not None:
            raise NotImplementedError

        self.cornerType = cornerType


class Corridor(_CesiumEntity):
    """ CorridorGraphics

    Parameters
    ----------

    positions: Cartesian3
        A Property specifying the array of Cartesian3 positions that define the centerline of the corridor.
    width: float
        A numeric Property specifying the distance between the edges of the corridor.
    cornerType: CornerType, default CornerType.ROUNDED
        A CornerType Property specifying the style of the corners.
    height: float, default 0.
        A numeric Property specifying the altitude of the corridor.
    extrudedHeight: float, default 0.
        A numeric Property specifying the altitude of the corridor extrusion.
    show: bool, default True
        A boolean Property specifying the visibility of the corridor.
    fill: bool, default True
        A boolean Property specifying whether the corridor is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the corridor.
    outline: bool, default False
        A boolean Property specifying whether the corridor is outlined.
    outlineColor: cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    granularity: float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the distance between each latitude and longitude.
    """

    _klass = 'corridor'
    _props = ['positions', 'cornerType']

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

        if cornerType is not None:
            raise NotImplementedError
        self.cornerType = cornerType


class Wall(_CesiumEntity):
    """ WallGraphics

    Parameters
    ----------

    positions: Cartesian3
        A Property specifying the array of Cartesian3 positions which define the top of the wall.
    maximumHeights: float or its list
        A Property specifying an array of heights to be used for the top of the wall instead of the height of each position.
    minimumHeights: float or its list
        A Property specifying an array of heights to be used for the bottom of the wall instead of the globe surface.
    show: bool, default True
        A boolean Property specifying the visibility of the wall.
    fill: bool, default True
        A boolean Property specifying whether the wall is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the wall.
    outline: bool, default False
        A boolean Property specifying whether the wall is outlined.
    outlineColor: cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    granularity: float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    """

    _klass = 'wall'
    _props = ['positions', 'maximumHeights', 'minimumHeights']

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
    """ RectangleGraphics

    Parameters
    ----------

    coordinates: list of 4 floats, corresponding to west, south, east, north
        The Property specifying the Rectangle.
    height: float, default 0.
        A numeric Property specifying the altitude of the rectangle.
    extrudedHeight: float, default 0.
        A numeric Property specifying the altitude of the rectangle extrusion.
    closeTop: bool, default True
        A boolean Property specifying whether the rectangle has a top cover when extruded
    closeBottom: bool, default True
        A boolean Property specifying whether the rectangle has a bottom cover when extruded.
    show: bool, default True
        A boolean Property specifying the visibility of the rectangle.
    fill: bool, default True
        A boolean Property specifying whether the rectangle is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the rectangle.
    outline: bool, default False
        A boolean Property specifying whether the rectangle is outlined.
    outlineColor: cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    rotation: float, default 0.
        A numeric property specifying the rotation of the rectangle clockwise from north.
    stRotation: float, default 0.
        A numeric property specifying the rotation of the rectangle texture counter-clockwise from north.
    granularity: float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between points on the rectangle.
    """

    _klass = 'rectangle'
    _props = ['coordinates', 'closeTop', 'closeBottom']

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

        self.coordinates = cartesian._maybe_rectangle(coordinates)

        self.closeTop = com.validate_bool_or_none(closeTop, key='closeTop')
        self.closeBottom = com.validate_bool_or_none(closeBottom, key='closeBottom')


class Box(_CesiumEntity):
    """ BoxGraphics

    Parameters
    ----------

    position: Cartesian3
        A Property specifying the Cartesian3 positions.
    dimensions: Cartesian3
        A Cartesian3 Property specifying the length, width, and height of the box.
    show: bool, default True
        A boolean Property specifying the visibility of the box.
    fill: bool, default True
        A boolean Property specifying whether the box is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the box.
    outline: bool, default False
        A boolean Property specifying whether the box is outlined.
    outlineColor: cesiumpy.color.Color, default BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    """

    _klass = 'box'
    _props = ['dimensions']

    def __init__(self, position, dimensions, show=None, fill=None, material=None,
                 outline=None, outlineColor=None, outlineWidth=None,
                 name=None):

        super(Box, self).__init__(show=show, fill=fill, material=material,
                                  outline=outline, outlineColor=outlineColor,
                                  outlineWidth=outlineWidth,
                                  position=position, name=name)

        dimensions = cartesian._maybe_cartesian(dimensions)
        if not isinstance(dimensions, cartesian.Cartesian3):
            msg = 'dimensions must be Cartesian3 or its compat: {0}'
            raise ValueError(msg.format(dimensions))
        self.dimensions = dimensions


class Polygon(_CesiumEntity):
    """ PolygonGraphics

    Parameters
    ----------

    hierarchy: Cartesian3
        A Property specifying the PolygonHierarchy.
    height: float, default 0.
        A numeric Property specifying the altitude of the polygon.
    extrudedHeight: float, default 0.
        A numeric Property specifying the altitude of the polygon extrusion.
    show: bool, default True
        A boolean Property specifying the visibility of the polygon.
    fill: bool, default True
        A boolean Property specifying whether the polygon is filled with the provided material.
    material: cesiumpy.color.Color, default WHITE
        A Property specifying the material used to fill the polygon.
    outline: bool, default False
        A boolean Property specifying whether the polygon is outlined.
    outlineColor: cesiumpy.color.Color, default Color.BLACK
        A Property specifying the Color of the outline.
    outlineWidth: float, default 1.
        A numeric Property specifying the width of the outline.
    stRotation: float, default 0.
        A numeric property specifying the rotation of the polygon texture counter-clockwise from north.
    granularity: float, default cesiumpy.math.RADIANS_PER_DEGREE
        A numeric Property specifying the angular distance between each latitude and longitude point.
    perPositionHeight: bool, default False
        A boolean specifying whether or not the the height of each position is used.
    """

    _klass = 'polygon'
    _props = ['hierarchy', 'perPositionHeight']

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

        self.perPositionHeight = com.validate_bool_or_none(perPositionHeight, key='perPositionHeight')

