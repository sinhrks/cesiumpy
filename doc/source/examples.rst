Examples
========

This section lists some examples using ``cesiumpy`` and other packages. You
can find ``Jupyter Notebook`` of these exampless under ``GitHub`` repository
(maps are not rendered on ``GitHub``. Download an run them on local).

- https://github.com/sinhrks/cesiumpy/tree/master/examples

Use with pandas
---------------

Following example shows retrieving ``US National Parks`` data from Wikipedia,
then plot number of visitors on the map.

First, load data from Wikipedia using ``pd.read_html`` functionality. The data
contains latitude and longtitude as text, thus some preprocessing is required.

.. code-block:: python

  >>> import pandas as pd
  >>> url = "https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States"
  >>> df = pd.read_html(url, header=0)[0]

  >>> locations = df['Location'].str.extract(u'(\D+) (\d+°\d+′[NS]) (\d+°\d+′[WE]).*')
  >>> locations.columns = ['State', 'lat', 'lon']
  >>> locations['lat'] = locations['lat'].str.replace(u'°', '.')
  >>> locations['lon'] = locations['lon'].str.replace(u'°', '.')
  >>> locations.loc[locations['lat'].str.endswith('S'), 'lat'] = '-' + locations['lat']
  >>> locations.loc[locations['lon'].str.endswith('W'), 'lon'] = '-' + locations['lon']

  >>> locations['lat'] = locations['lat'].str.slice_replace(start=-2)
  >>> locations['lon'] = locations['lon'].str.slice_replace(start=-2)
  >>> locations[['lat', 'lon']] = locations[['lat', 'lon']].astype(float)

  >>> locations.head()
              State    lat     lon
  0           Maine  44.21  -68.13
  1  American Samoa -14.15 -170.41
  2            Utah  38.41 -109.34
  3    South Dakota  43.45 -102.30
  4           Texas  29.15 -103.15

  >>> df = pd.concat([df, locations], axis=1)

Once prepared the data, iterate over rows and plot its values. The below script adds
``cesiumpy.Cylinder`` which height is corresponding to the number of visitors.

.. code-block:: python

  >>> import cesiumpy

  >>> options = dict(animation=True, baseLayerPicker=False, fullscreenButton=False,
  ...                geocoder=False, homeButton=False, infoBox=False, sceneModePicker=True,
  ...                selectionIndicator=False, navigationHelpButton=False,
  ...                timeline=False, navigationInstructionsInitiallyVisible=False)

  >>> v = cesiumpy.Viewer(**options)

  >>> for i, row in df.iterrows():
  ...     l = row['Recreation Visitors (2014)[5]']
  ...     cyl = cesiumpy.Cylinder(position=[row['lon'], row['lat'], l / 2.], length=l,
  ...                             topRadius=10e4, bottomRadius=10e4, material='aqua', alpha=0.5)
  ...     v.entities.add(cyl)

  >>> v

.. image:: ./_static/pandas01.png


Use with shapely / geopandas
----------------------------

Following example shows how to handle ``geojson`` files using ``cesiumpy``.

First, read ``geojson`` file of US, California using ``geopandas`` function.
The content will be ``shapely`` instance.

.. code-block:: python

  >>> import geopandas as gpd

  >>> df = gpd.read_file('ca.json')
  >>> df.head()
    fips                                           geometry      id        name
  0   06  POLYGON ((-123.233256 42.006186, -122.378853 4...  USA-CA  California

  >>> g = df.loc[0, "geometry"]
  >>> type(g)
  shapely.geometry.polygon.Polygon


We can use this ``shapely`` instance to specify the shape of ``cesiumpy`` instances.
The below script adds ``cesiumpy.Wall`` which has the shape of California.

.. code-block:: python

  >>> import cesiumpy

  >>> options = dict(animation=True, baseLayerPicker=False, fullscreenButton=False,
  ...                geocoder=False, homeButton=False, infoBox=False, sceneModePicker=True,
  ...                selectionIndicator=False, navigationHelpButton=False,
  ...                timeline=False, navigationInstructionsInitiallyVisible=False)

  >>> v = cesiumpy.Viewer(**options)
  >>> v.entities.add(cesiumpy.Wall(positions=g,
  ...                              maximumHeights=10e5, minimumHeights=0,
  ...                              material=cesiumpy.color.RED))
  >>> v

.. image:: ./_static/geopandas01.png