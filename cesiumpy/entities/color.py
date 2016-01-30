#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import six
import traitlets
import warnings

import cesiumpy
import cesiumpy.common as com
from cesiumpy.entities.material import Material


# matplotlib compat
_SINGLE_COLOR_MAP = {'B': 'BLUE', 'G': 'GREEN', 'R': 'RED',
                     'C': 'CYAN', 'M': 'MAGENTA', 'Y': 'YELLOW',
                     'K': 'BLACK', 'W': 'WHITE'}



class ColorTrait(traitlets.Instance):

    def __init__(self, args=None, kw=None, **metadata):
        super(ColorTrait, self).__init__(klass=Color, args=args, kw=kw,
                                         **metadata)

    def validate(self, obj, value):
        value = _maybe_color(value)
        return super(ColorTrait, self).validate(obj, value)


def _maybe_color(x):
    """ Convert str to NamedColor constant """

    if isinstance(x, six.string_types):
        cname = x.upper()
        cname = _SINGLE_COLOR_MAP.get(cname, cname)

        color = getattr(cesiumpy.color, cname, None)

        if color is not None and isinstance(color, NamedColor):
            return color

    return x



class Color(Material):

    _props = []

    red = traitlets.Int()
    green = traitlets.Int()
    blue = traitlets.Int()
    _alpha = traitlets.Float(min=0., max=1., allow_none=True)

    def __init__(self, red, green, blue, alpha=None):

        self.red = red
        self.green = green
        self.blue = blue
        self._alpha = alpha

    @property
    def alpha(self):
        return self._alpha

    def withAlpha(self, alpha):
        c = self.copy()
        c._alpha = alpha
        return c

    def set_alpha(self, alpha):
        msg = "Color.set_alpha is deprecated. Use Color.withAlpha"
        warnings.warn(msg)
        return self.withAlpha(alpha)

    def __repr__(self):
        if self.alpha is None:
            rep = """Color({red}, {green}, {blue})"""
            return rep.format(red=self.red, green=self.green, blue=self.blue)
        else:
            rep = """Color({red}, {green}, {blue}, {alpha})"""
            return rep.format(red=self.red, green=self.green,
                              blue=self.blue, alpha=self.alpha)

    @property
    def script(self):
        return 'Cesium.{rep}'.format(rep=repr(self))

    def copy(self):
        return CesiumColor(red=self.red, green=self.green,
                           blue=self.blue, alpha=self.alpha)


class NamedColor(Color):

    _name = traitlets.Unicode()

    def __init__(self, name, alpha=None):
        self._name = name
        self._alpha = alpha

    @property
    def name(self):
        return self._name

    def __repr__(self):
        if self.alpha is None:
            rep = """Color.{name}"""
            return rep.format(name=self.name)
        else:
            rep = """Color.{name}.withAlpha({alpha})"""
            return rep.format(name=self.name, alpha=self.alpha)

    def copy(self):
        return NamedColor(name=self.name, alpha=self.alpha)


class ColorFactory(object):

    # mapped to cesiumpy.color

    @property
    def Color(self):
        """ return Color class """
        return Color

    def __getattr__(self, name):
        if name in _COLORS:
            # always return new instance to avoid overwrite
            return NamedColor(name=name)
        else:
            msg = "Unable to find color name: '{name}'"
            raise AttributeError(msg.format(name=name))

# --------------------------------------------------
# COLOR CONSTANTS
# --------------------------------------------------

# How to create
# copy colors from "https://cesiumjs.org/Cesium/Build/Documentation/Color.html"

# colors = [c for c in colors.split() if c.startswith('staticconstant')]
# colors = [c.split('.')[-1] for c in colors]

_COLORS = ['ALICEBLUE',
 'ANTIQUEWHITE',
 'AQUA',
 'AQUAMARINE',
 'AZURE',
 'BEIGE',
 'BISQUE',
 'BLACK',
 'BLANCHEDALMOND',
 'BLUE',
 'BLUEVIOLET',
 'BROWN',
 'BURLYWOOD',
 'CADETBLUE',
 'CHARTREUSE',
 'CHOCOLATE',
 'CORAL',
 'CORNFLOWERBLUE',
 'CORNSILK',
 'CRIMSON',
 'CYAN',
 'DARKBLUE',
 'DARKCYAN',
 'DARKGOLDENROD',
 'DARKGRAY',
 'DARKGREEN',
 'DARKGREY',
 'DARKKHAKI',
 'DARKMAGENTA',
 'DARKOLIVEGREEN',
 'DARKORANGE',
 'DARKORCHID',
 'DARKRED',
 'DARKSALMON',
 'DARKSEAGREEN',
 'DARKSLATEBLUE',
 'DARKSLATEGRAY',
 'DARKSLATEGREY',
 'DARKTURQUOISE',
 'DARKVIOLET',
 'DEEPPINK',
 'DEEPSKYBLUE',
 'DIMGRAY',
 'DIMGREY',
 'DODGERBLUE',
 'FIREBRICK',
 'FLORALWHITE',
 'FORESTGREEN',
 'FUSCHIA',
 'GAINSBORO',
 'GHOSTWHITE',
 'GOLD',
 'GOLDENROD',
 'GRAY',
 'GREEN',
 'GREENYELLOW',
 'GREY',
 'HONEYDEW',
 'HOTPINK',
 'INDIANRED',
 'INDIGO',
 'IVORY',
 'KHAKI',
 'LAVENDAR_BLUSH',
 'LAVENDER',
 'LAWNGREEN',
 'LEMONCHIFFON',
 'LIGHTBLUE',
 'LIGHTCORAL',
 'LIGHTCYAN',
 'LIGHTGOLDENRODYELLOW',
 'LIGHTGRAY',
 'LIGHTGREEN',
 'LIGHTGREY',
 'LIGHTPINK',
 'LIGHTSEAGREEN',
 'LIGHTSKYBLUE',
 'LIGHTSLATEGRAY',
 'LIGHTSLATEGREY',
 'LIGHTSTEELBLUE',
 'LIGHTYELLOW',
 'LIME',
 'LIMEGREEN',
 'LINEN',
 'MAGENTA',
 'MAROON',
 'MEDIUMAQUAMARINE',
 'MEDIUMBLUE',
 'MEDIUMORCHID',
 'MEDIUMPURPLE',
 'MEDIUMSEAGREEN',
 'MEDIUMSLATEBLUE',
 'MEDIUMSPRINGGREEN',
 'MEDIUMTURQUOISE',
 'MEDIUMVIOLETRED',
 'MIDNIGHTBLUE',
 'MINTCREAM',
 'MISTYROSE',
 'MOCCASIN',
 'NAVAJOWHITE',
 'NAVY',
 'OLDLACE',
 'OLIVE',
 'OLIVEDRAB',
 'ORANGE',
 'ORANGERED',
 'ORCHID',
 'PALEGOLDENROD',
 'PALEGREEN',
 'PALETURQUOISE',
 'PALEVIOLETRED',
 'PAPAYAWHIP',
 'PEACHPUFF',
 'PERU',
 'PINK',
 'PLUM',
 'POWDERBLUE',
 'PURPLE',
 'RED',
 'ROSYBROWN',
 'ROYALBLUE',
 'SADDLEBROWN',
 'SALMON',
 'SANDYBROWN',
 'SEAGREEN',
 'SEASHELL',
 'SIENNA',
 'SILVER',
 'SKYBLUE',
 'SLATEBLUE',
 'SLATEGRAY',
 'SLATEGREY',
 'SNOW',
 'SPRINGGREEN',
 'STEELBLUE',
 'TAN',
 'TEAL',
 'THISTLE',
 'TOMATO',
 'TRANSPARENT',
 'TURQUOISE',
 'VIOLET',
 'WHEAT',
 'WHITE',
 'WHITESMOKE',
 'YELLOW',
 'YELLOWGREEN']