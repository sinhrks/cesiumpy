Entities
========

This section describes the basic usage of ``cesiumpy``. ``cesiumpy`` is the lightweight
wrapper for `Cesium.js <http://cesiumjs.org/>`_.

Cartesian
---------

`Cesium.js <http://cesiumjs.org/>`_ handles coordinates using ``Cartesian`` class. ``Cartesian`` may represent following 2 types of coordinates

- Pair of numerics, like ``x``, ``y``, ``z``
- Geolocation (degrees), like ``longitude``, ``latitude``, ``height``

.. code-block:: python

  >>> import cesiumpy

  >>> cesiumpy.Cartesian2(10, 20)
  Cartesian2(10, 20)

  >>> cesiumpy.Cartesian3(10, 20, 30)
  Cartesian3(10, 20, 30)

  >>> cesiumpy.Cartesian3.fromDegrees(-110, 40, 0)
  Cartesian3.fromDegrees(-110, 40, 0)

Basically you don't have to use the ``Cartesian`` classes because ``cesiumpy`` automatically converts python's ``list`` and ``tuple`` to ``Cartesian`` based on it's dimension.

Point
-----

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/PointGraphics.html?

.. code-block:: python

  >>> p = cesiumpy.Point(position=[-110, 40, 0])
  >>> p
  Point(-110, 40, 0)

  >>> p.script
  u'{position : Cesium.Cartesian3.fromDegrees(-110, 40, 0), point : {color : Cesium.Color.WHITE, pixelSize : 10}}'

You can specify the color using constants defined in ``cesiumpy.color``, or ``str`` specifying the color name.

.. code-block:: python

  >>> p = cesiumpy.Point(position=[-110, 40, 0], color=cesiumpy.color.RED)
  >>> p.script
  u'{position : Cesium.Cartesian3.fromDegrees(-110, 40, 0), point : {color : Cesium.Color.RED, pixelSize : 10}}'

  >>> p = cesiumpy.Point(position=[-110, 40, 0], color='blue')
  >>> p.script
  u'{position : Cesium.Cartesian3.fromDegrees(-110, 40, 0), point : {color : Cesium.Color.BLUE, pixelSize : 10}}'

Label
-----

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/LabelGraphics.html?

.. code-block:: python

  >>> l = cesiumpy.Label(position=[-110, 40, 0], text='xxx')
  >>> l
  Label(-110, 40, 0)

  >>> l.script
  u'{position : Cesium.Cartesian3.fromDegrees(-110, 40, 0), label : {text : "xxx"}}'

Box
---

.. code-block:: python

  >>> b = cesiumpy.Box(position=[-110, 40, 0], dimensions=(40e4, 30e4, 50e4))
  >>> b
  Box(-110, 40, 0)

  >>> b.script
  u'{position : Cesium.Cartesian3.fromDegrees(-110, 40, 0), box : {dimensions : new Cesium.Cartesian3(400000.0, 300000.0, 500000.0)}}'


Ellipse
-------


Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/EllipseGraphics.html?

.. code-block:: python

  >>> e = cesiumpy.Ellipse(position=[-110, 40, 0], semiMinorAxis=25e4,
  ...                      semiMajorAxis=40e4)
  >>> e
  Ellipse(-110, 40, 0)

  >>> e.script
  u'{position : Cesium.Cartesian3.fromDegrees(-110, 40, 0), ellipse : {semiMinorAxis : 250000.0, semiMajorAxis : 400000.0}}'


Cylinder
--------

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/CylinderGraphics.html?

.. code-block:: python

  >>> c = cesiumpy.Cylinder(position=[-110, 40, 100], length=100e4,
  ...                       topRadius=10e4, bottomRadius=10e4)
  >>> c
  Cylinder(-110, 40, 100)

  >>> c.script
  u'{position : Cesium.Cartesian3.fromDegrees(-110, 40, 100), cylinder : {length : 1000000.0, topRadius : 100000.0, bottomRadius : 100000.0}}'

Polygon
-------

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/PolygonGraphics.html?

.. code-block:: python

  >>> p = cesiumpy.Polygon(hierarchy=[-90, 40, -95, 40, -95, 45, -90, 40])
  >>> p
  Polygon([-90, 40, -95, 40, -95, 45, -90, 40])

  >>> p.script
  u'{polygon : {hierarchy : Cesium.Cartesian3.fromDegreesArray([-90, 40, -95, 40, -95, 45, -90, 40])}}'


Rectangle
---------

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/RectangleGraphics.html?

.. code-block:: python

  >>> r = cesiumpy.Rectangle(coordinates=(-85, 40, -80, 45))
  >>> r
  Rectangle(west=-85, south=40, east=-80, north=45)

  >>> r.script
  u'{rectangle : {coordinates : Cesium.Rectangle.fromDegrees(-85, 40, -80, 45)}}'


Ellipsoid
---------

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/EllipsoidGraphics.html?

.. code-block:: python

  >>> e = cesiumpy.Ellipsoid(position=(-70, 40, 0), radii=(20e4, 20e4, 30e4))
  >>> e
  Ellipsoid(-70, 40, 0)

  >>> e.script
  u'{position : Cesium.Cartesian3.fromDegrees(-70, 40, 0), ellipsoid : {radii : new Cesium.Cartesian3(200000.0, 200000.0, 300000.0)}}'


Wall
----

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/WallGraphics.html?

.. code-block:: python

  >>> w = cesiumpy.Wall(positions=[-60, 40, -65, 40, -65, 45, -60, 45],
  ...                   maximumHeights=10e4, minimumHeights=0)
  >>> w
  Wall([-60, 40, -65, 40, -65, 45, -60, 45])

  >>> w.script
  u'{wall : {positions : Cesium.Cartesian3.fromDegreesArray([-60, 40, -65, 40, -65, 45, -60, 45]), maximumHeights : [100000.0, 100000.0, 100000.0, 100000.0], minimumHeights : [0, 0, 0, 0]}}'


Corridor
--------

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/CorridorGraphics.html?

.. code-block:: python

  >>> c = cesiumpy.Corridor(positions=[-120, 30, -90, 35, -60, 30], width=2e5)
  >>> c
  Corridor([-120, 30, -90, 35, -60, 30])

  >>> c.script
  u'{corridor : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 30, -90, 35, -60, 30]), width : 200000.0}}'

Polyline
--------

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/PolylineGraphics.html?

.. code-block:: python

  p = cesiumpy.Polyline(positions=[-120, 25, -90, 30, -60, 25], width=0.5)
  >>> p
  Polyline([-120, 25, -90, 30, -60, 25])

  >>> p.script
  u'{polyline : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 25, -90, 30, -60, 25]), width : 0.5}}'


PolylineVolume
--------------

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/PolylineVolumeGraphics.html?

.. code-block:: python

  >>> p = cesiumpy.PolylineVolume(positions=[-120, 20, -90, 25, -60, 20],
  ...                             shape=[-5e4, -5e4, 5e4, -5e4, 5e4, 5e4, -5e4, 5e4])
  >>> p
  PolylineVolume([-120, 20, -90, 25, -60, 20])

  >>> p.script
  u'{polylineVolume : {positions : Cesium.Cartesian3.fromDegreesArray([-120, 20, -90, 25, -60, 20]), shape : [new Cesium.Cartesian2(-50000.0, -50000.0), new Cesium.Cartesian2(50000.0, -50000.0), new Cesium.Cartesian2(50000.0, 50000.0), new Cesium.Cartesian2(-50000.0, 50000.0)]}}'

Billboard
---------

Refer to the following document to see the details of each options.

- https://cesiumjs.org/Cesium/Build/Documentation/BillboardGraphics.html?

.. code-block:: python

  >>> p = cesiumpy.PinBuilder()
  >>> b = cesiumpy.Billboard(position=(-110, 40, 0), image=p)
  >>> b
  Billboard(-110, 40, 0)

  >>> b.script
  u'{position : Cesium.Cartesian3.fromDegrees(-110, 40, 0), billboard : {image : new Cesium.PinBuilder().fromColor(Cesium.Color.ROYALBLUE, 48)}}'
