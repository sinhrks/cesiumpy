#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import random
import six
import traitlets
import warnings

from cesiumpy.base import _CesiumObject
import cesiumpy.util.common as com
from cesiumpy.entities.material import Material


class Color(Material):

    _props = ['red', 'green', 'blue', 'alpha']

    red = traitlets.Float(min=0., max=1.)
    green = traitlets.Float(min=0., max=1.)
    blue = traitlets.Float(min=0., max=1.)
    alpha = traitlets.Float(min=0., max=1., allow_none=True)

    def __init__(self, red, green, blue, alpha=None):

        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def withAlpha(self, alpha):
        self.alpha = alpha
        return self

    def set_alpha(self, alpha):
        msg = "Color.set_alpha is deprecated. Use Color.withAlpha"
        warnings.warn(msg)
        return self.withAlpha(alpha)

    @classmethod
    def fromAlpha(cls, color, alpha):
        return Color(red=color.red, green=color.green, blue=color.blue,
                     alpha=alpha)

    @classmethod
    def fromBytes(cls, red=255, green=255, blue=255, alpha=None):
        """
        Creates a new Color specified using red, green, blue, and alpha values
        that are in the range of 0 to 255, converting them internally to a range
        of 0.0 to 1.0.

        Parameters
        ----------

        red: int, default 255
            The red component.
        green: int, default 255
            The green component.
        blue: int, default 255
            The blue component.
        alpha: int, default None
            The alpha component.
        """
        if alpha is not None:
            alpha = alpha / 255.
        return Color(red=red / 255., green=green / 255.,
                     blue=blue / 255., alpha=alpha)

    @classmethod
    def fromString(self, color):
        """
        Creates a Color instance from a CSS color value. Shortcut for
        Color.fromCssColorString.

        Parameters
        ----------

        color: str
            The CSS color value in #rgb, #rrggbb, rgb(), rgba(), hsl(), or hsla() format.
        """
        return CssColor(name=color)

    @classmethod
    def fromCssColorString(self, color):
        """
        Creates a Color instance from a CSS color value.

        Parameters
        ----------

        color: str
            The CSS color value in #rgb, #rrggbb, rgb(), rgba(), hsl(), or hsla() format.
        """
        return CssColor(name=color)

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
        # need new
        return 'new Cesium.{rep}'.format(rep=repr(self))

    def copy(self):
        return Color(red=self.red, green=self.green,
                     blue=self.blue, alpha=self.alpha)

    @classmethod
    def maybe(cls, x):
        """ Convert str or tuple to ColorConstant """
        if isinstance(x, Color):
            return x

        if isinstance(x, six.string_types):
            cname = x.upper()
            cname = _SINGLE_COLORS.get(cname, cname)

            if cname in _COLORS:
                return ColorConstant(name=cname)
        elif com.is_listlike(x):
            if len(x) in (3, 4):
                return Color(*x)

        msg = 'Unable to convert to Color instance: {x}'
        raise ValueError(msg.format(x=x))


class CssColor(Color):

    name = traitlets.Unicode()
    alpha = traitlets.Float(min=0., max=1., allow_none=True)

    def __init__(self, name, alpha=None):
        self.name = name
        self.alpha = alpha

    def __repr__(self):
        if self.alpha is None:
            rep = """Color.fromCssColorString("{name}")"""
            return rep.format(name=self.name)
        else:
            rep = """Color.fromCssColorString("{name}").withAlpha({alpha})"""
            return rep.format(name=self.name, alpha=self.alpha)

    @property
    def script(self):
        # no need new
        return 'Cesium.{rep}'.format(rep=repr(self))

    def copy(self):
        return self.__class__(name=self.name, alpha=self.alpha)


class ColorConstant(CssColor):

    def __repr__(self):
        if self.alpha is None:
            rep = """Color.{name}"""
            return rep.format(name=self.name)
        else:
            rep = """Color.{name}.withAlpha({alpha})"""
            return rep.format(name=self.name, alpha=self.alpha)


class ColorMap(_CesiumObject):

    name = traitlets.Unicode()

    def __init__(self, name):
        plt = com._check_package('matplotlib.pyplot')
        self.name = name
        self.cm = plt.get_cmap(name)

    def __call__(self, *args, **kwargs):
        result = self.cm(*args, **kwargs)

        if isinstance(result, tuple):
            # single color
            return Color(*result)
        else:
            return [Color(*c) for c in result]

    def __repr__(self):
        rep = """ColorMap("{name}")"""
        return rep.format(name=self.name)


class ColorFactory(object):

    # mapped to cesiumpy.color

    @property
    def Color(self):
        """ return Color class """
        return Color

    def get_cmap(self, name):
        return ColorMap(name)

    def choice(self):
        """
        Randomly returns a single color.
        """
        name = random.choice(_COLORS)
        return ColorConstant(name=name)

    def sample(self, n):
        """
        Randomly returns list of colors which length is n.
        """
        names = random.sample(_COLORS, n)
        return [ColorConstant(name=name) for name in names]

    def __getattr__(self, name):
        if name in _COLORS:
            # always return new instance to avoid overwrite
            return ColorConstant(name=name)
        else:
            msg = "Unable to find color name: '{name}'"
            raise AttributeError(msg.format(name=name))


# matplotlib compat
_SINGLE_COLORS = {'B': 'BLUE', 'G': 'GREEN', 'R': 'RED',
                  'C': 'CYAN', 'M': 'MAGENTA', 'Y': 'YELLOW',
                  'K': 'BLACK', 'W': 'WHITE'}

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
