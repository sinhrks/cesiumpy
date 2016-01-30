Read External Files
===================

``cesiumpy`` can read following file formats using ``io`` module. The results
are automatically converted to ``cesiumpy`` entities and can be added to
map directly.

- GeoJSON
- Shapefile

GeoJSON
-------

This example reads GeoJSON file of Japanese land area. ``cesiumpy.io.read_geojson``
returns a ``list`` of ``cesiumpy.Polygon``.

The file is provided by `mledoze/countries <https://github.com/mledoze/countries>`_ repositry.

.. code-block:: python

  >>> res = cesiumpy.io.read_geojson('jpn.geo.json')
  >>> type(res)
  list

You can add the ``list`` as entities.

.. code-block:: python

  >>> viewer = cesiumpy.Viewer()
  >>> viewer.entities.add(res)
  >>> viewer

.. image:: ./_static/io_geojson01.png

If you want to change some properties, passing keyword arguments via ``entities.add`` methods is easy. Of cource it is also OK to change properties of each entity one by one.

.. code-block:: python

  >>> viewer = cesiumpy.Viewer()
  >>> viewer.entities.add(res, extrudedHeight=1e6, material='aqua')
  >>> viewer

.. image:: ./_static/io_geojson02.png

Shapefile
---------

This example reads Shapefile of Japanese coastal lines. ``cesiumpy.io.read_shape``
returns a ``list`` of ``cesiumpy.Polyline``.

The file is provided by `地球地図日本 <http://www.gsi.go.jp/kankyochiri/gm_jpn.html>`_ website.

- 出典 (Source)：国土地理院ウェブサイト　

.. code-block:: python

  >>> res = cesiumpy.io.read_shape('coastl_jpn.shp')
  >>> type(res)
  list

Then, you can add the result to the map.

.. code-block:: python

  >>> viewer = cesiumpy.Viewer()
  >>> viewer.entities.add(res, material='red')
  >>> viewer

.. image:: ./_static/io_shape01.png

Bundled Data
------------

``cesiumpy`` bundles GeoJSON data provided by `mledoze/countries <https://github.com/mledoze/countries>`_ repositry. You can load them via ``cesiumpy.countries.get`` method passing country code or its name.

Please refer to `countries.json <https://github.com/mledoze/countries/blob/master/countries.json>`_ file
to check available country codes ("cca2" or "cca3") and names ("official name").

.. code-block:: python

  >>> usa = cesiumpy.countries.get('USA')
  >>> viewer = cesiumpy.Viewer()
  >>> viewer.entities.add(usa, material='red')
  >>> viewer

.. image:: ./_static/io_bundle01.png

