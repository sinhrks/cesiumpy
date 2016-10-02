#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import cesiumpy
import cesiumpy.util.common as com


class PlottingAccessor(object):

    def __init__(self, widget):
        self.widget = widget

    def _fill_by(self, x, length, key, default=None):
        if not com.is_listlike(x):
            if x is None:
                # fill by other default if specified
                x = default
            x = [x] * length

        # to support array interface
        x = com.validate_listlike(x, key)

        if len(x) != length:
            msg = "{key} length must be {length}: {x}"
            raise ValueError(msg.format(key=key, length=length, x=x))
        return x

    def __call__(self):
        raise NotImplementedError

    def bar(self, x, y, z, size=10e3, color=None, bottom=0.):
        """
        Plot cesiumpy.Cylinder like bar plot

        Parameters
        ----------

        x : list
            List of longitudes
        y : list
            List of latitudes
        z : list
            List of bar heights
        size : list or float, default 10e3
            Radius of cylinder
        color : list or Color
            Cylinder color
        bottom : list or float, default 0
            Bottom heights
        """
        x = com.validate_listlike(x, key='x')

        # for list validation (not allow scalar)
        y = com.validate_listlike(y, key='y')
        # for length validation
        y = self._fill_by(y, len(x), key='y')

        # z must be a list
        z = com.validate_listlike(z, key='z')
        z = self._fill_by(z, len(x), key='y')

        size = self._fill_by(size, len(x), key='size', default=10e3)
        color = self._fill_by(color, len(x), key='color')
        bottom = self._fill_by(bottom, len(x), key='bottom', default=0.)

        it = zip(x, y, z, size, color, bottom)
        for i, (_x, _y, _z, _size, _color, _bottom) in enumerate(it):
            p = cesiumpy.Cylinder(position=(_x, _y, _bottom + _z / 2.),
                                  length=_z,
                                  topRadius=_size, bottomRadius=_size,
                                  material=_color)
            self.widget.entities.add(p)
        return self.widget

    def scatter(self, x, y, z=None, size=None, color=None):
        """
        Plot cesiumpy.Point like scatter plot

        Parameters
        ----------

        x : list
            List of longitudes
        y : list
            List of latitudes
        z : list or float
            Height
        size : list or float
            Pixel size
        color : list or Color
            Point color
        """
        x = com.validate_listlike(x, key='x')

        # for list validation (not allow scalar)
        y = com.validate_listlike(y, key='y')
        # for length validation
        y = self._fill_by(y, len(x), key='y')

        z = self._fill_by(z, len(x), key='z', default=0)
        size = self._fill_by(size, len(x), key='size')
        color = self._fill_by(color, len(x), key='color')

        for i, (_x, _y, _z, _size, _color) in enumerate(zip(x, y, z, size, color)):
            p = cesiumpy.Point(position=(_x, _y, _z), pixelSize=_size,
                               color=_color)
            self.widget.entities.add(p)
        return self.widget

    def pin(self, x, y, z=None, text=None, size=None, color=None):
        """
        Plot cesiumpy.Pin

        Parameters
        ----------

        x : list
            List of longitudes
        y : list
            List of latitudes
        z : list or float
            Heights
        text : list
            List of labels
        size : list or float
            Text size
        color : list or Color
            Text color
        """
        x = com.validate_listlike(x, key='x')

        # for list validation (not allow scalar)
        y = com.validate_listlike(y, key='y')
        y = self._fill_by(y, len(x), key='y')

        z = self._fill_by(z, len(x), key='z', default=0)
        text = self._fill_by(text, len(x), key='text')
        size = self._fill_by(size, len(x), key='size')
        color = self._fill_by(color, len(x), key='color')

        for i, (_text, _x, _y, _z, _size, _color) in enumerate(zip(text, x, y, z, size, color)):
            pin = cesiumpy.Pin(color=_color, size=_size, text=_text)
            p = cesiumpy.Billboard(position=(_x, _y, _z), image=pin)
            self.widget.entities.add(p)
        return self.widget

    def label(self, text, x, y, z=None, size=None, color=None):
        """
        Plot cesiumpy.Label

        Parameters
        ----------

        text : list
            List of labels
        x : list
            List of longitudes
        y : list
            List of latitudes
        z : list or float
            Heights
        size : list or float
            Text size
        color : list or Color
            Text color
        """
        x = com.validate_listlike(x, key='x')

        # for list validation (not allow scalar)
        text = com.validate_listlike(text, key='text')
        text = self._fill_by(text, len(x), key='text')
        y = com.validate_listlike(y, key='y')
        y = self._fill_by(y, len(x), key='y')

        z = self._fill_by(z, len(x), key='z', default=0)
        size = self._fill_by(size, len(x), key='size')
        color = self._fill_by(color, len(x), key='color')

        for i, (_text, _x, _y, _z, _size, _color) in enumerate(zip(text, x, y, z, size, color)):
            p = cesiumpy.Label(position=(_x, _y, _z), text=_text,
                               scale=_size, fillColor=_color)
            self.widget.entities.add(p)
        return self.widget

    def contour(self, x, y, z):
        """
        Plot contours using cesiumpy.Polyline

        Parameters
        ----------

        X : np.ndarray
        Y : np.ndarray
        Y : np.ndarray

        *X* and *Y* must both be 2-D with the same shape as *Z*, or they
        must both be 1-D such that ``len(X)`` is the number of columns in
        *Z* and ``len(Y)`` is the number of rows in *Z*.
        """

        plt = com._check_package('matplotlib.pyplot')
        contours = plt.contour(x, y, z)

        for segs, c in zip(contours.allsegs, contours.tcolors):
            c = cesiumpy.color.Color(*c[0])
            for seg in segs:
                pos = seg.flatten().tolist()
                p = cesiumpy.Polyline(positions=pos, material=c)
                self.widget.entities.add(p)
        plt.close()
        return self.widget
