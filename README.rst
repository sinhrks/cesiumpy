cesiumpy
========

Lightweight Python wrapper for `Cesium.js <http://cesiumjs.org/>`_ Mainly intended to be used with ``Jupyter`` Notebook.

Example
=======

.. code-block:: python

  import cesiumpy
  options = dict(animation=True, baseLayerPicker=False, fullscreenButton=False,
                 geocoder=False, homeButton=False, infoBox=False, sceneModePicker=True,
                 selectionIndicator=False, navigationHelpButton=False,
                 timeline=False, navigationInstructionsInitiallyVisible=False)

  v = cesiumpy.Viewer(**options)
  v.add(cesiumpy.Box(dimensions=(40e4, 30e4, 50e4),
                     material=cesiumpy.color.RED, position=[-120, 40, 0]))
  v

.. image:: https://raw.githubusercontent.com/sinhrks/cesiumpy/master/doc/source/_static/main.png
