cesiumpy
========

Lightweight Python wrapper for `Cesium.js <http://cesiumjs.org/>`_ Mainly intended to be used with ``Jupyter`` Notebook.

Example
=======

.. code-block:: python

  import cesiumpy

  v = cesiumpy.Viewer()
  v.entities.add(cesiumpy.Box(dimensions=(40e4, 30e4, 50e4),
                 material=cesiumpy.color.RED, position=(-120, 40, 0))
  v

![rendered_image](sinhrks.github.com/cesiumpy/doc/source/_static/main.png)
