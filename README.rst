cesiumpy
========

.. image:: https://img.shields.io/pypi/v/cesiumpy.svg
    :target: https://pypi.python.org/pypi/cesiumpy/
.. image:: https://readthedocs.org/projects/cesiumpy/badge/?version=latest
    :target: http://cesiumpy.readthedocs.org/en/latest/
    :alt: Latest Docs
.. image:: https://travis-ci.org/sinhrks/cesiumpy.svg?branch=master
    :target: https://travis-ci.org/sinhrks/cesiumpy
.. image:: https://coveralls.io/repos/sinhrks/cesiumpy/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/sinhrks/cesiumpy?branch=master


Lightweight Python wrapper for `Cesium.js <http://cesiumjs.org/>`_. Mainly intended to be used with ``Jupyter Notebook``.

Installation
------------

Use ``pip``.

.. code-block:: sh

  pip install cesiumpy

Example
-------

Running following script on ``Jupyter`` Notebook will show an embedded interactive 3D map.

.. code-block:: python

  >>> import cesiumpy

  >>> v = cesiumpy.Viewer()
  >>> v.entities.add(cesiumpy.Box(dimensions=(40e4, 30e4, 50e4),
  ...                             material=cesiumpy.color.RED, position=(-120, 40, 0))
  >>> v

.. image:: https://raw.githubusercontent.com/sinhrks/cesiumpy/master/doc/source/_static/viewer01.png

Documentation
-------------

- http://cesiumpy.readthedocs.org/en/latest/

Bundled Datasets
----------------

- World countries: https://github.com/mledoze/countries (ODbL)

Dependencies
------------

- ``geopy``, ``traitlets``, ``six`` and ``enum34`` (Python 3.3 or earlier)
- (Optional) ``scipy`` and ``shapely``
