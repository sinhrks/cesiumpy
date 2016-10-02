#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import traitlets

import cesiumpy
from cesiumpy.base import _CesiumObject
import cesiumpy.entities.cartesian as cartesian
import cesiumpy.util.common as com
from cesiumpy.util.trait import MaybeTrait


class _CesiumProvider(_CesiumObject):

    _props = ['url']

    def __repr__(self):
        if self.url is None:
            return super(_CesiumProvider, self).__repr__()
        else:
            rep = """{klass}(url="{url}")"""
            return rep.format(klass=self.__class__.__name__, url=self.url)

    @property
    def script(self):
        props = super(_CesiumProvider, self).script
        rep = """new {klass}({props})"""
        return rep.format(klass=self._klass, props=props)


# --------------------------------------------------
# Terrain Provider
# --------------------------------------------------


class TerrainProvider(_CesiumProvider):

    _props = ['url', 'proxy', 'ellipsoid', 'credit']

    url = traitlets.Unicode()
    credit = traitlets.Unicode(allow_none=True)

    def __init__(self, url=None, proxy=None, tilingScheme=None,
                 ellipsoid=None, credit=None):
        self.url = url
        self.proxy = com.notimplemented(proxy)
        self.tilingScheme = com.notimplemented(tilingScheme)
        self.ellipsoid = com.notimplemented(ellipsoid)
        self.credit = credit


class ArcGisImageServerTerrainProvider(TerrainProvider):
    """
    ArcGisImageServerTerrainProvider

    Parameters
    ----------

    url : str
        The URL of the ArcGIS ImageServer service.
    token : str
        The authorization token to use to connect to the service.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    tilingScheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme specifying how the terrain is broken into tiles. If this parameter is not provided, a GeographicTilingScheme is used.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tilingScheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    credit : Credit or str
        The credit, which will is displayed on the canvas.
    """

    _props = ['url', 'token', 'proxy', 'tilingScheme', 'ellipsoid', 'credit']

    token = traitlets.Unicode(allow_none=True)

    def __init__(self, url, token, proxy=None, tilingScheme=None,
                 ellipsoid=None, credit=None):
        super(ArcGisImageServerTerrainProvider, self).__init__(url=url, proxy=proxy, tilingScheme=tilingScheme,
                                                               ellipsoid=ellipsoid, credit=credit)
        self.token = token


class CesiumTerrainProvider(TerrainProvider):
    """
    CesiumTerrainProvider

    Parameters
    ----------

    url : str
        The URL of the Cesium terrain server.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    requestVertexNormals : bool, default False
        Flag that indicates if the client should request additional lighting information from the server, in the form of per vertex normals if available.
    requestWaterMask : bool, default False
        Flag that indicates if the client should request per tile water masks from the server, if available.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    """

    _props = ['url', 'proxy', 'requestVertexNormals', 'requestWaterMask', 'ellipsoid', 'credit']

    requestVertexNormals = traitlets.Bool(allow_none=True)
    requestWaterMask = traitlets.Bool(allow_none=True)

    def __init__(self, url, proxy=None, requestVertexNormals=None,
                 requestWaterMask=None, ellipsoid=None, credit=None):
        super(CesiumTerrainProvider, self).__init__(url=url, proxy=proxy,
                                                    ellipsoid=ellipsoid, credit=credit)
        self.requestVertexNormals = requestVertexNormals
        self.requestWaterMask = requestWaterMask


class EllipsoidTerrainProvider(TerrainProvider):
    """
    EllipsoidTerrainProvider

    Parameters
    ----------

    tilingScheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme specifying how the ellipsoidal surface is broken into tiles. If this parameter is not provided, a GeographicTilingScheme is used.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tilingScheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    """

    url = traitlets.Unicode(allow_none=True)

    def __init__(self, tilingScheme=None, ellipsoid=None):

        super(EllipsoidTerrainProvider, self).__init__(tilingScheme=tilingScheme,
                                                       ellipsoid=ellipsoid)


class VRTheWorldTerrainProvider(TerrainProvider):
    """
    VRTheWorldTerrainProvider

    Parameters
    ----------
    url : str
        The URL of the VR-TheWorld TileMap.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    ellipsoid : Ellipsoid, default Ellipsoid.WGS84
        The ellipsoid. If this parameter is not specified, the WGS84 ellipsoid is used.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    """
    def __init__(self, url, proxy=None, ellipsoid=None, credit=None):

        super(VRTheWorldTerrainProvider, self).__init__(url=url, proxy=proxy,
                                                        ellipsoid=ellipsoid,
                                                        credit=credit)


# --------------------------------------------------
# Imagery Provider
# --------------------------------------------------


class ImageryProvider(_CesiumProvider):

    _props = ['url', 'fileExtension', 'rectangle', 'tillingScheme', 'ellipsoid',
              'tileWidth', 'tileHeight', 'tileDiscardPolicy',
              'minimumLevel', 'maximumLevel',
              'credit', 'proxy', 'subdomains']

    url = traitlets.Unicode(allow_none=True)
    fileExtension = traitlets.Unicode(allow_none=True)
    rectangle = MaybeTrait(klass=cartesian.Rectangle, allow_none=True)

    tileWidth = traitlets.Float(allow_none=True)
    tileHeight = traitlets.Float(allow_none=True)

    minimumLevel = traitlets.Float(allow_none=True)
    maximumLevel = traitlets.Float(allow_none=True)

    credit = traitlets.Unicode(allow_none=True)

    def __init__(self, url=None, fileExtension=None, rectangle=None, tillingScheme=None,
                 ellipsoid=None, tileWidth=None, tileHeight=None, tileDiscardPolicy=None,
                 minimumLevel=None, maximumLevel=None, credit=None, proxy=None, subdomains=None):

        self.url = url
        self.fileExtension = fileExtension
        self.rectangle = rectangle

        self.tillingScheme = com.notimplemented(tillingScheme)
        self.ellipsoid = com.notimplemented(ellipsoid)

        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.tileDiscardPolicy = com.notimplemented(tileDiscardPolicy)

        self.minimumLevel = minimumLevel
        self.maximumLevel = maximumLevel

        self.credit = credit

        self.proxy = com.notimplemented(proxy)
        self.subdomains = com.notimplemented(subdomains)


class ArcGisMapServerImageryProvider(ImageryProvider):
    """
    ArcGisImageServerTerrainProvider

    Parameters
    ----------

    url : str
        The URL of the ArcGIS MapServer service.
    token : str
        The ArcGIS token used to authenticate with the ArcGIS MapServer service.
    usePreCachedTilesIfAvailable : bool, default True
        If true, the server's pre-cached tiles are used if they are available. If false, any pre-cached tiles are ignored and the 'export' service is used.
    layers : str
        A comma-separated list of the layers to show, or undefined if all layers should be shown.
    enablePickFeatures : bool, default True
        If true, ArcGisMapServerImageryProvider#pickFeatures will invoke the Identify service on the MapServer and return the features included in the response. If false, ArcGisMapServerImageryProvider#pickFeatures will immediately return undefined (indicating no pickable features) without communicating with the server. Set this property to false if you don't want this provider's features to be pickable.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle of the layer. This parameter is ignored when accessing a tiled layer.
    tilingScheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme to use to divide the world into tiles. This parameter is ignored when accessing a tiled server.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tilingScheme is specified and used, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    tileWidth : int, default 256
        The width of each tile in pixels. This parameter is ignored when accessing a tiled server.
    tileHeight : int, default 256
        The height of each tile in pixels. This parameter is ignored when accessing a tiled server.
    tileDiscardPolicy : TileDiscardPolicy
        The policy that determines if a tile is invalid and should be discarded. If this value is not specified, a default DiscardMissingTileImagePolicy is used for tiled map servers, and a NeverTileDiscardPolicy is used for non-tiled map servers. In the former case, we request tile 0,0 at the maximum tile level and check pixels (0,0), (200,20), (20,200), (80,110), and (160, 130). If all of these pixels are transparent, the discard check is disabled and no tiles are discarded. If any of them have a non-transparent color, any tile that has the same values in these pixel locations is discarded. The end result of these defaults should be correct tile discarding for a standard ArcGIS Server. To ensure that no tiles are discarded, construct and pass a NeverTileDiscardPolicy for this parameter.
    maximumLevel : int
        The maximum tile level to request, or undefined if there is no maximum. This parameter is ignored when accessing a tiled server.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    """

    _props = ['url', 'token', 'usePreCachedTilesIfAvailable', 'layers',
              'enablePickFeatures', 'rectangle', 'tillingScheme', 'ellipsoid',
              'tileWidth', 'tileHeight', 'tileDiscardPolicy', 'minimumLevel',
              'proxy']

    token = traitlets.Unicode(allow_none=True)
    usePreCachedTilesIfAvailable = traitlets.Bool(allow_none=True)
    layers = traitlets.Unicode(allow_none=True)
    enablePickFeatures = traitlets.Bool(allow_none=True)

    def __init__(self, url, token=None, usePreCachedTilesIfAvailable=None,
                 layers=None, enablePickFeatures=None, rectangle=None, tillingScheme=None,
                 ellipsoid=None, tileWidth=None, tileHeight=None, tileDiscardPolicy=None,
                 minimumLevel=None, proxy=None):

        super(ArcGisMapServerImageryProvider, self).__init__(url=url, rectangle=rectangle,
                                                             tillingScheme=tillingScheme,
                                                             ellipsoid=ellipsoid,
                                                             tileWidth=tileWidth,
                                                             tileHeight=tileHeight,
                                                             tileDiscardPolicy=tileDiscardPolicy,
                                                             minimumLevel=minimumLevel, proxy=proxy)

        self.token = token
        self.usePreCachedTilesIfAvailable = usePreCachedTilesIfAvailable
        self.layers = layers
        self.enablePickFeatures = enablePickFeatures


class BingMapsImageryProvider(ImageryProvider):
    """
    BingMapsImageryProvider

    Parameters
    ----------

    url : str
        The url of the Bing Maps server hosting the imagery.
    key : str
        The Bing Maps key for your application, which can be created at https://www.bingmapsportal.com/. If this parameter is not provided, BingMapsApi.defaultKey is used. If BingMapsApi.defaultKey is undefined as well, a message is written to the console reminding you that you must create and supply a Bing Maps key as soon as possible. Please do not deploy an application that uses Bing Maps imagery without creating a separate key for your application.
    tileProtocol : str
        The protocol to use when loading tiles, e.g. 'http:' or 'https:'. By default, tiles are loaded using the same protocol as the page.
    mapStyle : str, default BingMapsStyle.AERIAL
        The type of Bing Maps imagery to load.
    culture : str, default ''
        The culture to use when requesting Bing Maps imagery. Not all cultures are supported. See http://msdn.microsoft.com/en-us/library/hh441729.aspx for information on the supported cultures.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    tileDiscardPolicy : TileDiscardPolicy
        The policy that determines if a tile is invalid and should be discarded. If this value is not specified, a default DiscardMissingTileImagePolicy is used which requests tile 0,0 at the maximum tile level and checks pixels (0,0), (120,140), (130,160), (200,50), and (200,200). If all of these pixels are transparent, the discard check is disabled and no tiles are discarded. If any of them have a non-transparent color, any tile that has the same values in these pixel locations is discarded. The end result of these defaults should be correct tile discarding for a standard Bing Maps server. To ensure that no tiles are discarded, construct and pass a NeverTileDiscardPolicy for this parameter.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    """

    _props = ['url', 'key', 'tileProtocol', 'mapStyle', 'culture',
              'ellipsoid', 'tileDiscardPolicy', 'proxy']

    key = traitlets.Unicode()
    tileProtocol = traitlets.Unicode()
    mapStyle = traitlets.Unicode(allow_none=True)
    culture = traitlets.Unicode(allow_none=True)

    def __init__(self, url, key, tileProtocol, mapStyle=None, culture=None,
                 ellipsoid=None, tileDiscardPolicy=None, proxy=None):

        super(BingMapsImageryProvider, self).__init__(url=url, ellipsoid=ellipsoid,
                                                      tileDiscardPolicy=tileDiscardPolicy,
                                                      proxy=proxy)

        self.key = key
        self.tileProtocol = key
        self.mapStyle = mapStyle
        self.culture = culture


class GoogleEarthImageryProvider(ImageryProvider):
    """
    GoogleEarthImageryProvider

    Parameters
    ----------

    url : str
        The url of the Google Earth server hosting the imagery.
    channel : int
        The channel (id) to be used when requesting data from the server. The channel number can be found by looking at the json file located at: earth.localdomain/default_map/query?request=Json&vars=geeServerDefs The /default_map path may differ depending on your Google Earth Enterprise server configuration. Look for the "id" that is associated with a "ImageryMaps" requestType. There may be more than one id available. Example: { layers: [ { id: 1002, requestType: "ImageryMaps" }, { id: 1007, requestType: "VectorMapsRaster" } ] }
    path : str, default "/default_map"
        The path of the Google Earth server hosting the imagery.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    tileDiscardPolicy : TileDiscardPolicy
        The policy that determines if a tile is invalid and should be discarded. To ensure that no tiles are discarded, construct and pass a NeverTileDiscardPolicy for this parameter.
    maximumLevel : int
        The maximum level-of-detail supported by the Google Earth Enterprise server, or undefined if there is no limit.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    """

    _props = ['url', 'channel', 'path', 'ellipsoid', 'tileDiscardPolicy',
              'maximumLevel', 'proxy']

    channel = traitlets.Float()
    path = traitlets.Unicode(allow_none=True)

    def __init__(self, url, channel, path=None, ellipsoid=None,
                 tileDiscardPolicy=None, maximumLevel=None, proxy=None):

        super(GoogleEarthImageryProvider, self).__init__(url=url,
                                                         ellipsoid=ellipsoid,
                                                         tileDiscardPolicy=tileDiscardPolicy,
                                                         maximumLevel=maximumLevel, proxy=proxy)

        self.channel = channel
        self.path = path


class GridImageryProvider(ImageryProvider):

    def __init__(self):
        # this accepts other kw than options
        raise NotImplementedError


class MapboxImageryProvider(ImageryProvider):
    """
    MapboxImageryProvider

    Parameters
    ----------

    url : str, default '//api.mapbox.com/v4/'
        The Mapbox server url.
    mapId : str
        The Mapbox Map ID.
    accessToken : str
        The public access token for the imagery.
    format : str, default 'png'
        The format of the image request.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle, in radians, covered by the image.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    minimumLevel : int, default 0
        The minimum level-of-detail supported by the imagery provider. Take care when specifying this that the number of tiles at the minimum level is small, such as four or less. A larger number is likely to result in rendering problems.
    maximumLevel : int, default 0
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL.
    """

    _props = ['url', 'mapId', 'accessToken', 'format', 'rectangle', 'ellipsoid',
              'minimumLevel', 'maximumLevel', 'credit', 'proxy']

    url = traitlets.Unicode()
    mapId = traitlets.Unicode()
    accessToken = traitlets.Unicode()
    format = traitlets.Unicode(allow_none=True)

    def __init__(self, url, mapId, accessToken, format=None,
                 rectangle=None, ellipsoid=None, minimumLevel=None,
                 maximumLevel=None, credit=None, proxy=None):

        super(MapboxImageryProvider, self).__init__(url=url, rectangle=rectangle, ellipsoid=ellipsoid,
                                                    minimumLevel=minimumLevel, maximumLevel=maximumLevel,
                                                    credit=credit, proxy=proxy)

        self.mapId = mapId
        self.accessToken = accessToken
        self.format = format


class OpenStreetMapImageryProvider(ImageryProvider):
    """
    OpenStreetMapImageryProvider

    Parameters
    ----------

    url : str, default '//a.tile.openstreetmap.org'
        The OpenStreetMap server url.
    fileExtension : str, default 'png'
        The file extension for images on the server.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle of the layer.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    minimumLevel : int, default 0
        The minimum level-of-detail supported by the imagery provider.
    maximumLevel : int
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit.
    credit : Credit or str, default 'MapQuest, Open Street Map and contributors, CC-BY-SA'
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL.
    """

    def __init__(self, url=None, fileExtension=None, rectangle=None, ellipsoid=None,
                 minimumLevel=None, maximumLevel=None, credit=None, proxy=None):

        super(OpenStreetMapImageryProvider, self).__init__(url=url,
                                                           fileExtension=fileExtension,
                                                           rectangle=rectangle,
                                                           ellipsoid=ellipsoid,
                                                           minimumLevel=minimumLevel,
                                                           maximumLevel=maximumLevel,
                                                           credit=credit, proxy=proxy)


class SingleTileImageryProvider(ImageryProvider):
    """
    SingleTileImageryProvider

    Parameters
    ----------

    url : str
        The url for the tile.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle, in radians, covered by the image.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    """

    def __init__(self, url, rectangle=None, ellipsoid=None, credit=None, proxy=None):

        from cesiumpy.entities.material import TemporaryImage
        if isinstance(url, TemporaryImage):
            url = url.script

        super(SingleTileImageryProvider, self).__init__(url=url, rectangle=rectangle,
                                                        ellipsoid=ellipsoid,
                                                        credit=credit, proxy=proxy)


class TileCoordinatesImageryProvider(ImageryProvider):
    """
    TileCoordinatesImageryProvider

    Parameters
    ----------

    color : cesiumpy.color.Color, default YELLOW
        The color to draw the tile box and label.
    tilingScheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme for which to draw tiles.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tilingScheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    tileWidth : int, default 256
        The width of the tile for level-of-detail selection purposes.
    tileHeight : int, default 256
        The height of the tile for level-of-detail selection purposes.
    """

    _props = ['color', 'tillingScheme', 'ellipsoid', 'tileWidth', 'tileHeight']

    def __init__(self, color=None, tillingScheme=None, ellipsoid=None,
                 tileWidth=None, tileHeight=None):

        super(TileCoordinatesImageryProvider, self).__init__(tillingScheme=tillingScheme, ellipsoid=ellipsoid,
                                                             tileWidth=tileWidth, tileHeight=tileHeight)

        if color is not None:
            color = cesiumpy.color._maybe_color(color)
            if not isinstance(color, cesiumpy.color.Color):
                msg = 'color must be a Color instance: {0}'
                raise ValueError(msg.format(type(color)))
        self.color = color


class TileMapServiceImageryProvider(ImageryProvider):
    """
    TileMapServiceImageryProvider

    Parameters
    ----------

    url : str, default '.'
        Path to image tiles on server.
    fileExtension : default 'png'
        The file extension for images on the server.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle, in radians, covered by the image.
    tilingScheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme specifying how the ellipsoidal surface is broken into tiles. If this parameter is not provided, a WebMercatorTilingScheme is used.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tilingScheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    tileWidth : int, default 256
        Pixel width of image tiles.
    tileHeight : int, default 256
        Pixel height of image tiles.
    minimumLevel : int, default 0
        The minimum level-of-detail supported by the imagery provider. Take care when specifying this that the number of tiles at the minimum level is small, such as four or less. A larger number is likely to result in rendering problems.
    maximumLevel : int
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit.
    credit : Credit or str, default ''
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL.
    """

    def __init__(self, url=None, fileExtension=None, rectangle=None, tillingScheme=None,
                 ellipsoid=None, tileWidth=None, tileHeight=None,
                 minimumLevel=None, maximumLevel=None, credit=None, proxy=None):

        super(TileMapServiceImageryProvider, self).__init__(url=url,
                                                            fileExtension=fileExtension,
                                                            rectangle=rectangle,
                                                            tillingScheme=tillingScheme,
                                                            ellipsoid=ellipsoid,
                                                            tileWidth=tileWidth,
                                                            tileHeight=tileHeight,
                                                            minimumLevel=minimumLevel,
                                                            maximumLevel=maximumLevel,
                                                            credit=credit, proxy=proxy)


class UrlTemplateImageryProvider(ImageryProvider):

    def __init__(self):
        raise NotImplementedError


class WebMapServiceImageryProvider(ImageryProvider):
    """
    WebMapServiceImageryProvider

    Parameters
    ----------

    url : str
        The URL of the WMS service. The URL supports the same keywords as the UrlTemplateImageryProvider.
    layers : str
        The layers to include, separated by commas.
    parameters : Object, default WebMapServiceImageryProvider.DefaultParameters
        Additional parameters to pass to the WMS server in the GetMap URL.
    getFeatureInfoParameters : Object, default WebMapServiceImageryProvider.GetFeatureInfoDefaultParameters
        Additional parameters to pass to the WMS server in the GetFeatureInfo URL.
    enablePickFeatures : bool, default True
        If true, WebMapServiceImageryProvider#pickFeatures will invoke the GetFeatureInfo operation on the WMS server and return the features included in the response. If false, WebMapServiceImageryProvider#pickFeatures will immediately return undefined (indicating no pickable features) without communicating with the server. Set this property to false if you know your WMS server does not support GetFeatureInfo or if you don't want this provider's features to be pickable.
    getFeatureInfoFormats : list of GetFeatureInfoFormat, default WebMapServiceImageryProvider.DefaultGetFeatureInfoFormats
        The formats in which to try WMS GetFeatureInfo requests.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle of the layer.
    tilingScheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme to use to divide the world into tiles.
    ellipsoid : Ellipsoid
        The ellipsoid. If the tilingScheme is specified, this parameter is ignored and the tiling scheme's ellipsoid is used instead. If neither parameter is specified, the WGS84 ellipsoid is used.
    tileWidth : int, default 256
        The width of each tile in pixels.
    tileHeight : int, default 256
        The height of each tile in pixels.
    minimumLevel : int, default 0
        The minimum level-of-detail supported by the imagery provider. Take care when specifying this that the number of tiles at the minimum level is small, such as four or less. A larger number is likely to result in rendering problems.
    maximumLevel : int
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit. If not specified, there is no limit.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL, if needed.
    subdomains : str or list of str, default 'abc'
    """

    _props = ['url', 'layers', 'parameters', 'getFeatureInfoParameters',
              'enablePickFeatures', 'getFeatureInfoFormats', 'rectangle',
              'tillingScheme', 'ellipsoid', 'tileWidth', 'tileHeight',
              'tileDiscardPolicy', 'minimumLevel', 'maximumLevel',
              'credit', 'proxy', 'subdomains']

    layers = traitlets.Unicode()
    enablePickFeatures = traitlets.Bool(allow_none=True)

    def __init__(self, url, layers, parameters=None, getFeatureInfoParameters=None,
                 enablePickFeatures=None, getFeatureInfoFormats=None,
                 rectangle=None, tillingScheme=None, ellipsoid=None, tileWidth=None,
                 tileHeight=None, tileDiscardPolicy=None, minimumLevel=None,
                 maximumLevel=None, credit=None, proxy=None, subdomains=None):

        super(WebMapServiceImageryProvider, self).__init__(url=url, rectangle=rectangle,
                                                           tillingScheme=tillingScheme,
                                                           ellipsoid=ellipsoid,
                                                           tileWidth=tileWidth,
                                                           tileHeight=tileHeight,
                                                           tileDiscardPolicy=tileDiscardPolicy,
                                                           minimumLevel=minimumLevel,
                                                           maximumLevel=maximumLevel,
                                                           credit=credit, proxy=proxy,
                                                           subdomains=subdomains)

        self.layers = layers

        self.parameters = com.notimplemented(parameters)
        self.getFeatureInfoParameters = com.notimplemented(getFeatureInfoParameters)

        self.enablePickFeatures = enablePickFeatures

        self.getFeatureInfoFormats = com.notimplemented(getFeatureInfoFormats)


class WebMapTileServiceImageryProvider(ImageryProvider):
    """
    WebMapTileServiceImageryProvider

    Parameters
    ----------

    url : str
        The base URL for the WMTS GetTile operation (for KVP-encoded requests) or the tile-URL template (for RESTful requests). The tile-URL template should contain the following variables: {style}, {TileMatrixSet}, {TileMatrix}, {TileRow}, {TileCol}. The first two are optional if actual values are hardcoded or not required by the server. The {s} keyword may be used to specify subdomains.
    layer : str
        The layer name for WMTS requests.
    style : str
        The style name for WMTS requests.
    format : str, default 'image/jpeg'
        The MIME type for images to retrieve from the server.
    tileMatrixSetID : str
        The identifier of the TileMatrixSet to use for WMTS requests.
    tileMatrixLabels : list
        optional A list of identifiers in the TileMatrix to use for WMTS requests, one per TileMatrix level.
    rectangle : Rectangle, default Rectangle.MAX_VALUE
        The rectangle covered by the layer.
    tilingScheme : TilingScheme, default new GeographicTilingScheme()
        The tiling scheme corresponding to the organization of the tiles in the TileMatrixSet.
    ellipsoid : Ellipsoid
        The ellipsoid. If not specified, the WGS84 ellipsoid is used.
    tileWidth : int, default 256
        optional The tile width in pixels.
    tileHeight : int, default 256
        The tile height in pixels.
    minimumLevel : int, default 0
        The minimum level-of-detail supported by the imagery provider.
    maximumLevel : int
        The maximum level-of-detail supported by the imagery provider, or undefined if there is no limit.
    credit : Credit or str
        A credit for the data source, which is displayed on the canvas.
    proxy : Proxy
        A proxy to use for requests. This object is expected to have a getURL function which returns the proxied URL.
    subdomains : str or list of str, default 'abc'
        The subdomains to use for the {s} placeholder in the URL template. If this parameter is a single string, each character in the string is a subdomain. If it is an array, each element in the array is a subdomain.
    """

    _props = ['url', 'layer', 'style', 'format', 'tileMatrixLabels', 'tileMatrixLabels',
              'rectangle', 'tillingScheme', 'ellipsoid', 'tileWidth', 'tileHeight',
              'tileDiscardPolicy', 'minimumLevel', 'maximumLevel', 'credit', 'proxy',
              'subdomains']

    layer = traitlets.Unicode()
    style = traitlets.Unicode()
    format = traitlets.Unicode(allow_none=True)
    tileMatrixSetID = traitlets.Unicode(allow_none=True)

    def __init__(self, url, layer, style, format=None, tileMatrixSetID=None,
                 tileMatrixLabels=None, rectangle=None, tillingScheme=None,
                 ellipsoid=None, tileWidth=None, tileHeight=None, tileDiscardPolicy=None,
                 minimumLevel=None, maximumLevel=None, credit=None, proxy=None, subdomains=None):

        super(WebMapTileServiceImageryProvider, self).__init__(url=url, rectangle=rectangle,
                                                               tillingScheme=tillingScheme,
                                                               ellipsoid=ellipsoid,
                                                               tileWidth=tileWidth,
                                                               tileHeight=tileHeight,
                                                               tileDiscardPolicy=tileDiscardPolicy,
                                                               minimumLevel=minimumLevel,
                                                               maximumLevel=maximumLevel,
                                                               credit=credit, proxy=proxy,
                                                               subdomains=subdomains)
        self.layer = layer
        self.style = style
        self.format = format
        self.tileMatrixSetID = tileMatrixSetID

        self.tileMatrixLabels = com.notimplemented(tileMatrixLabels)
