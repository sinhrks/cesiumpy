/*global define*/
define([
        '../Core/BoundingSphere',
        '../Core/BoxOutlineGeometry',
        '../Core/Cartesian2',
        '../Core/Cartesian3',
        '../Core/Cartesian4',
        '../Core/Color',
        '../Core/ColorGeometryInstanceAttribute',
        '../Core/defaultValue',
        '../Core/defined',
        '../Core/defineProperties',
        '../Core/destroyObject',
        '../Core/DeveloperError',
        '../Core/Event',
        '../Core/FeatureDetection',
        '../Core/GeometryInstance',
        '../Core/GeometryPipeline',
        '../Core/IndexDatatype',
        '../Core/Intersect',
        '../Core/Math',
        '../Core/Matrix4',
        '../Core/OrientedBoundingBox',
        '../Core/PrimitiveType',
        '../Core/Rectangle',
        '../Core/SphereOutlineGeometry',
        '../Core/Visibility',
        '../Core/WebMercatorProjection',
        '../Renderer/Buffer',
        '../Renderer/BufferUsage',
        '../Renderer/ContextLimits',
        '../Renderer/DrawCommand',
        '../Renderer/RenderState',
        '../Renderer/VertexArray',
        '../Scene/BlendingState',
        '../Scene/DepthFunction',
        '../Scene/Pass',
        '../Scene/PerInstanceColorAppearance',
        '../Scene/Primitive',
        '../ThirdParty/when',
        './GlobeSurfaceTile',
        './ImageryLayer',
        './ImageryState',
        './QuadtreeTileLoadState',
        './SceneMode'
    ], function(
        BoundingSphere,
        BoxOutlineGeometry,
        Cartesian2,
        Cartesian3,
        Cartesian4,
        Color,
        ColorGeometryInstanceAttribute,
        defaultValue,
        defined,
        defineProperties,
        destroyObject,
        DeveloperError,
        Event,
        FeatureDetection,
        GeometryInstance,
        GeometryPipeline,
        IndexDatatype,
        Intersect,
        CesiumMath,
        Matrix4,
        OrientedBoundingBox,
        PrimitiveType,
        Rectangle,
        SphereOutlineGeometry,
        Visibility,
        WebMercatorProjection,
        Buffer,
        BufferUsage,
        ContextLimits,
        DrawCommand,
        RenderState,
        VertexArray,
        BlendingState,
        DepthFunction,
        Pass,
        PerInstanceColorAppearance,
        Primitive,
        when,
        GlobeSurfaceTile,
        ImageryLayer,
        ImageryState,
        QuadtreeTileLoadState,
        SceneMode) {
    "use strict";

    /**
     * Provides quadtree tiles representing the surface of the globe.  This type is intended to be used
     * with {@link QuadtreePrimitive}.
     *
     * @alias GlobeSurfaceTileProvider
     * @constructor
     *
     * @param {TerrainProvider} options.terrainProvider The terrain provider that describes the surface geometry.
     * @param {ImageryLayerCollection} option.imageryLayers The collection of imagery layers describing the shading of the surface.
     * @param {GlobeSurfaceShaderSet} options.surfaceShaderSet The set of shaders used to render the surface.
     *
     * @private
     */
    function GlobeSurfaceTileProvider(options) {
        //>>includeStart('debug', pragmas.debug);
        if (!defined(options)) {
            throw new DeveloperError('options is required.');
        }
        if (!defined(options.terrainProvider)) {
            throw new DeveloperError('options.terrainProvider is required.');
        } else if (!defined(options.imageryLayers)) {
            throw new DeveloperError('options.imageryLayers is required.');
        } else if (!defined(options.surfaceShaderSet)) {
            throw new DeveloperError('options.surfaceShaderSet is required.');
        }
        //>>includeEnd('debug');

        this.lightingFadeOutDistance = 6500000.0;
        this.lightingFadeInDistance = 9000000.0;
        this.hasWaterMask = false;
        this.oceanNormalMap = undefined;
        this.zoomedOutOceanSpecularIntensity = 0.5;
        this.enableLighting = false;

        this._quadtree = undefined;
        this._terrainProvider = options.terrainProvider;
        this._imageryLayers = options.imageryLayers;
        this._surfaceShaderSet = options.surfaceShaderSet;

        this._renderState = undefined;
        this._blendRenderState = undefined;
        this._pickRenderState = undefined;

        this._errorEvent = new Event();

        this._imageryLayers.layerAdded.addEventListener(GlobeSurfaceTileProvider.prototype._onLayerAdded, this);
        this._imageryLayers.layerRemoved.addEventListener(GlobeSurfaceTileProvider.prototype._onLayerRemoved, this);
        this._imageryLayers.layerMoved.addEventListener(GlobeSurfaceTileProvider.prototype._onLayerMoved, this);
        this._imageryLayers.layerShownOrHidden.addEventListener(GlobeSurfaceTileProvider.prototype._onLayerShownOrHidden, this);

        this._layerOrderChanged = false;

        this._tilesToRenderByTextureCount = [];
        this._drawCommands = [];
        this._uniformMaps = [];
        this._pickCommands = [];
        this._usedDrawCommands = 0;
        this._usedPickCommands = 0;

        this._debug = {
            wireframe : false,
            boundingSphereTile : undefined
        };

        this._baseColor = undefined;
        this._firstPassInitialColor = undefined;
        this.baseColor = new Color(0.0, 0.0, 0.5, 1.0);
    }

    defineProperties(GlobeSurfaceTileProvider.prototype, {
        /**
         * Gets or sets the color of the globe when no imagery is available.
         * @memberof GlobeSurfaceTileProvider.prototype
         * @type {Color}
         */
        baseColor : {
            get : function() {
                return this._baseColor;
            },
            set : function(value) {
                //>>includeStart('debug', pragmas.debug);
                if (!defined(value)) {
                    throw new DeveloperError('value is required.');
                }
                //>>includeEnd('debug');

                this._baseColor = value;
                this._firstPassInitialColor = Cartesian4.fromColor(value, this._firstPassInitialColor);
            }
        },
        /**
         * Gets or sets the {@link QuadtreePrimitive} for which this provider is
         * providing tiles.  This property may be undefined if the provider is not yet associated
         * with a {@link QuadtreePrimitive}.
         * @memberof GlobeSurfaceTileProvider.prototype
         * @type {QuadtreePrimitive}
         */
        quadtree : {
            get : function() {
                return this._quadtree;
            },
            set : function(value) {
                //>>includeStart('debug', pragmas.debug);
                if (!defined(value)) {
                    throw new DeveloperError('value is required.');
                }
                //>>includeEnd('debug');

                this._quadtree = value;
            }
        },

        /**
         * Gets a value indicating whether or not the provider is ready for use.
         * @memberof GlobeSurfaceTileProvider.prototype
         * @type {Boolean}
         */
        ready : {
            get : function() {
                return this._terrainProvider.ready && (this._imageryLayers.length === 0 || this._imageryLayers.get(0).imageryProvider.ready);
            }
        },

        /**
         * Gets the tiling scheme used by the provider.  This property should
         * not be accessed before {@link GlobeSurfaceTileProvider#ready} returns true.
         * @memberof GlobeSurfaceTileProvider.prototype
         * @type {TilingScheme}
         */
        tilingScheme : {
            get : function() {
                return this._terrainProvider.tilingScheme;
            }
        },

        /**
         * Gets an event that is raised when the geometry provider encounters an asynchronous error.  By subscribing
         * to the event, you will be notified of the error and can potentially recover from it.  Event listeners
         * are passed an instance of {@link TileProviderError}.
         * @memberof GlobeSurfaceTileProvider.prototype
         * @type {Event}
         */
        errorEvent : {
            get : function() {
                return this._errorEvent;
            }
        },

        /**
         * Gets or sets the terrain provider that describes the surface geometry.
         * @memberof GlobeSurfaceTileProvider.prototype
         * @type {TerrainProvider}
         */
        terrainProvider : {
            get : function() {
                return this._terrainProvider;
            },
            set : function(terrainProvider) {
                if (this._terrainProvider === terrainProvider) {
                    return;
                }

                //>>includeStart('debug', pragmas.debug);
                if (!defined(terrainProvider)) {
                    throw new DeveloperError('terrainProvider is required.');
                }
                //>>includeEnd('debug');

                this._terrainProvider = terrainProvider;

                if (defined(this._quadtree)) {
                    this._quadtree.invalidateAllTiles();
                }
            }
        }
    });

    function sortTileImageryByLayerIndex(a, b) {
        var aImagery = a.loadingImagery;
        if (!defined(aImagery)) {
            aImagery = a.readyImagery;
        }

        var bImagery = b.loadingImagery;
        if (!defined(bImagery)) {
            bImagery = b.readyImagery;
        }

        return aImagery.imageryLayer._layerIndex - bImagery.imageryLayer._layerIndex;
    }

    /**
     * Called at the beginning of the update cycle for each render frame, before {@link QuadtreeTileProvider#showTileThisFrame}
     * or any other functions.
     *
     * @param {FrameState} frameState The frame state.
     */
    GlobeSurfaceTileProvider.prototype.beginUpdate = function(frameState) {
        this._imageryLayers._update();

        if (this._layerOrderChanged) {
            this._layerOrderChanged = false;

            // Sort the TileImagery instances in each tile by the layer index.
            this._quadtree.forEachLoadedTile(function(tile) {
                tile.data.imagery.sort(sortTileImageryByLayerIndex);
            });
        }

        var i;
        var len;

        var tilesToRenderByTextureCount = this._tilesToRenderByTextureCount;
        for (i = 0, len = tilesToRenderByTextureCount.length; i < len; ++i) {
            var tiles = tilesToRenderByTextureCount[i];
            if (defined(tiles)) {
                tiles.length = 0;
            }
        }

        this._usedDrawCommands = 0;

        // Add credits for terrain and imagery providers.
        var creditDisplay = frameState.creditDisplay;

        if (this._terrainProvider.ready && defined(this._terrainProvider.credit)) {
            creditDisplay.addCredit(this._terrainProvider.credit);
        }

        var imageryLayers = this._imageryLayers;
        for (i = 0, len = imageryLayers.length; i < len; ++i) {
            var imageryProvider = imageryLayers.get(i).imageryProvider;
            if (imageryProvider.ready && defined(imageryProvider.credit)) {
                creditDisplay.addCredit(imageryProvider.credit);
            }
        }
    };

    /**
     * Called at the end of the update cycle for each render frame, after {@link QuadtreeTileProvider#showTileThisFrame}
     * and any other functions.
     *
     * @param {FrameState} frameState The frame state.
     */
    GlobeSurfaceTileProvider.prototype.endUpdate = function(frameState) {
        if (!defined(this._renderState)) {
            this._renderState = RenderState.fromCache({ // Write color and depth
                cull : {
                    enabled : true
                },
                depthTest : {
                    enabled : true,
                    func : DepthFunction.LESS
                }
            });

            this._blendRenderState = RenderState.fromCache({ // Write color and depth
                cull : {
                    enabled : true
                },
                depthTest : {
                    enabled : true,
                    func : DepthFunction.LESS_OR_EQUAL
                },
                blending : BlendingState.ALPHA_BLEND
            });
        }

        // Add the tile render commands to the command list, sorted by texture count.
        var tilesToRenderByTextureCount = this._tilesToRenderByTextureCount;
        for (var textureCountIndex = 0, textureCountLength = tilesToRenderByTextureCount.length; textureCountIndex < textureCountLength; ++textureCountIndex) {
            var tilesToRender = tilesToRenderByTextureCount[textureCountIndex];
            if (!defined(tilesToRender)) {
                continue;
            }

            for (var tileIndex = 0, tileLength = tilesToRender.length; tileIndex < tileLength; ++tileIndex) {
                addDrawCommandsForTile(this, tilesToRender[tileIndex], frameState);
            }
        }
    };

    /**
     * Adds draw commands for tiles rendered in the previous frame for a pick pass.
     *
     * @param {FrameState} frameState The frame state.
     */
    GlobeSurfaceTileProvider.prototype.updateForPick = function(frameState) {
        if (!defined(this._pickRenderState)) {
            this._pickRenderState = RenderState.fromCache({
                colorMask : {
                    red : false,
                    green : false,
                    blue : false,
                    alpha : false
                },
                depthTest : {
                    enabled : true
                }
            });
        }

        this._usedPickCommands = 0;
        var drawCommands = this._drawCommands;

        // Add the tile pick commands from the tiles drawn last frame.
        for (var i = 0, length = this._usedDrawCommands; i < length; ++i) {
            addPickCommandsForTile(this, drawCommands[i], frameState);
        }
    };

    /**
     * Gets the maximum geometric error allowed in a tile at a given level, in meters.  This function should not be
     * called before {@link GlobeSurfaceTileProvider#ready} returns true.
     *
     * @param {Number} level The tile level for which to get the maximum geometric error.
     * @returns {Number} The maximum geometric error in meters.
     */
    GlobeSurfaceTileProvider.prototype.getLevelMaximumGeometricError = function(level) {
        return this._terrainProvider.getLevelMaximumGeometricError(level);
    };

    /**
     * Loads, or continues loading, a given tile.  This function will continue to be called
     * until {@link QuadtreeTile#state} is no longer {@link QuadtreeTileLoadState#LOADING}.  This function should
     * not be called before {@link GlobeSurfaceTileProvider#ready} returns true.
     *
     * @param {FrameState} frameState The frame state.
     * @param {QuadtreeTile} tile The tile to load.
     *
     * @exception {DeveloperError} <code>loadTile</code> must not be called before the tile provider is ready.
     */
    GlobeSurfaceTileProvider.prototype.loadTile = function(frameState, tile) {
        GlobeSurfaceTile.processStateMachine(tile, frameState, this._terrainProvider, this._imageryLayers);
    };

    var boundingSphereScratch = new BoundingSphere();

    /**
     * Determines the visibility of a given tile.  The tile may be fully visible, partially visible, or not
     * visible at all.  Tiles that are renderable and are at least partially visible will be shown by a call
     * to {@link GlobeSurfaceTileProvider#showTileThisFrame}.
     *
     * @param {QuadtreeTile} tile The tile instance.
     * @param {FrameState} frameState The state information about the current frame.
     * @param {QuadtreeOccluders} occluders The objects that may occlude this tile.
     *
     * @returns {Visibility} The visibility of the tile.
     */
    GlobeSurfaceTileProvider.prototype.computeTileVisibility = function(tile, frameState, occluders) {
        var distance = this.computeDistanceToTile(tile, frameState);
        tile._distance = distance;

        if (frameState.fog.enabled) {
            if (CesiumMath.fog(distance, frameState.fog.density) >= 1.0) {
                // Tile is completely in fog so return that it is not visible.
                return Visibility.NONE;
            }
        }

        var surfaceTile = tile.data;
        var cullingVolume = frameState.cullingVolume;
        var boundingVolume = defaultValue(surfaceTile.orientedBoundingBox, surfaceTile.boundingSphere3D);

        if (frameState.mode !== SceneMode.SCENE3D) {
            boundingVolume = boundingSphereScratch;
            BoundingSphere.fromRectangleWithHeights2D(tile.rectangle, frameState.mapProjection, surfaceTile.minimumHeight, surfaceTile.maximumHeight, boundingVolume);
            Cartesian3.fromElements(boundingVolume.center.z, boundingVolume.center.x, boundingVolume.center.y, boundingVolume.center);

            if (frameState.mode === SceneMode.MORPHING) {
                boundingVolume = BoundingSphere.union(surfaceTile.boundingSphere3D, boundingVolume, boundingVolume);
            }
        }

        var intersection = cullingVolume.computeVisibility(boundingVolume);
        if (intersection === Intersect.OUTSIDE) {
            return Visibility.NONE;
        }

        if (frameState.mode === SceneMode.SCENE3D) {
            var occludeePointInScaledSpace = surfaceTile.occludeePointInScaledSpace;
            if (!defined(occludeePointInScaledSpace)) {
                return intersection;
            }

            if (occluders.ellipsoid.isScaledSpacePointVisible(occludeePointInScaledSpace)) {
                return intersection;
            }

            return Visibility.NONE;
        }

        return intersection;
    };

    var modifiedModelViewScratch = new Matrix4();
    var tileRectangleScratch = new Cartesian4();
    var rtcScratch = new Cartesian3();
    var centerEyeScratch = new Cartesian3();
    var southwestScratch = new Cartesian3();
    var northeastScratch = new Cartesian3();

    /**
     * Shows a specified tile in this frame.  The provider can cause the tile to be shown by adding
     * render commands to the commandList, or use any other method as appropriate.  The tile is not
     * expected to be visible next frame as well, unless this method is called next frame, too.
     *
     * @param {Object} tile The tile instance.
     * @param {FrameState} frameState The state information of the current rendering frame.
     */
    GlobeSurfaceTileProvider.prototype.showTileThisFrame = function(tile, frameState) {
        var readyTextureCount = 0;
        var tileImageryCollection = tile.data.imagery;
        for (var i = 0, len = tileImageryCollection.length; i < len; ++i) {
            var tileImagery = tileImageryCollection[i];
            if (defined(tileImagery.readyImagery) && tileImagery.readyImagery.imageryLayer.alpha !== 0.0) {
                ++readyTextureCount;
            }
        }

        var tileSet = this._tilesToRenderByTextureCount[readyTextureCount];
        if (!defined(tileSet)) {
            tileSet = [];
            this._tilesToRenderByTextureCount[readyTextureCount] = tileSet;
        }

        tileSet.push(tile);

        var debug = this._debug;
        ++debug.tilesRendered;
        debug.texturesRendered += readyTextureCount;
    };

    var southwestCornerScratch = new Cartesian3();
    var northeastCornerScratch = new Cartesian3();
    var negativeUnitY = new Cartesian3(0.0, -1.0, 0.0);
    var negativeUnitZ = new Cartesian3(0.0, 0.0, -1.0);
    var vectorScratch = new Cartesian3();

    /**
     * Gets the distance from the camera to the closest point on the tile.  This is used for level-of-detail selection.
     *
     * @param {QuadtreeTile} tile The tile instance.
     * @param {FrameState} frameState The state information of the current rendering frame.
     * @param {Cartesian3} cameraCartesianPosition The position of the camera in world coordinates.
     * @param {Cartographic} cameraCartographicPosition The position of the camera in cartographic / geodetic coordinates.
     *
     * @returns {Number} The distance from the camera to the closest point on the tile, in meters.
     */
    GlobeSurfaceTileProvider.prototype.computeDistanceToTile = function(tile, frameState) {
        var surfaceTile = tile.data;
        var camera = frameState.camera;
        var cameraCartesianPosition = camera.positionWC;
        var cameraCartographicPosition = camera.positionCartographic;

        var result = 0.0;
        if (!Rectangle.contains(tile.rectangle, cameraCartographicPosition)) {
            var southwestCornerCartesian = surfaceTile.southwestCornerCartesian;
            var northeastCornerCartesian = surfaceTile.northeastCornerCartesian;
            var westNormal = surfaceTile.westNormal;
            var southNormal = surfaceTile.southNormal;
            var eastNormal = surfaceTile.eastNormal;
            var northNormal = surfaceTile.northNormal;

            if (frameState.mode !== SceneMode.SCENE3D) {
                southwestCornerCartesian = frameState.mapProjection.project(Rectangle.southwest(tile.rectangle), southwestCornerScratch);
                southwestCornerCartesian.z = southwestCornerCartesian.y;
                southwestCornerCartesian.y = southwestCornerCartesian.x;
                southwestCornerCartesian.x = 0.0;
                northeastCornerCartesian = frameState.mapProjection.project(Rectangle.northeast(tile.rectangle), northeastCornerScratch);
                northeastCornerCartesian.z = northeastCornerCartesian.y;
                northeastCornerCartesian.y = northeastCornerCartesian.x;
                northeastCornerCartesian.x = 0.0;
                westNormal = negativeUnitY;
                eastNormal = Cartesian3.UNIT_Y;
                southNormal = negativeUnitZ;
                northNormal = Cartesian3.UNIT_Z;
            }

            var vectorFromSouthwestCorner = Cartesian3.subtract(cameraCartesianPosition, southwestCornerCartesian, vectorScratch);
            var distanceToWestPlane = Cartesian3.dot(vectorFromSouthwestCorner, westNormal);
            var distanceToSouthPlane = Cartesian3.dot(vectorFromSouthwestCorner, southNormal);

            var vectorFromNortheastCorner = Cartesian3.subtract(cameraCartesianPosition, northeastCornerCartesian, vectorScratch);
            var distanceToEastPlane = Cartesian3.dot(vectorFromNortheastCorner, eastNormal);
            var distanceToNorthPlane = Cartesian3.dot(vectorFromNortheastCorner, northNormal);

            if (distanceToWestPlane > 0.0) {
                result += distanceToWestPlane * distanceToWestPlane;
            } else if (distanceToEastPlane > 0.0) {
                result += distanceToEastPlane * distanceToEastPlane;
            }

            if (distanceToSouthPlane > 0.0) {
                result += distanceToSouthPlane * distanceToSouthPlane;
            } else if (distanceToNorthPlane > 0.0) {
                result += distanceToNorthPlane * distanceToNorthPlane;
            }
        }

        var cameraHeight;
        if (frameState.mode === SceneMode.SCENE3D) {
            cameraHeight = cameraCartographicPosition.height;
        } else {
            cameraHeight = cameraCartesianPosition.x;
        }

        var maximumHeight = frameState.mode === SceneMode.SCENE3D ? surfaceTile.maximumHeight : 0.0;
        var distanceFromTop = cameraHeight - maximumHeight;
        if (distanceFromTop > 0.0) {
            result += distanceFromTop * distanceFromTop;
        }

        return Math.sqrt(result);
    };

    /**
     * Returns true if this object was destroyed; otherwise, false.
     * <br /><br />
     * If this object was destroyed, it should not be used; calling any function other than
     * <code>isDestroyed</code> will result in a {@link DeveloperError} exception.
     *
     * @returns {Boolean} True if this object was destroyed; otherwise, false.
     *
     * @see GlobeSurfaceTileProvider#destroy
     */
    GlobeSurfaceTileProvider.prototype.isDestroyed = function() {
        return false;
    };

    /**
     * Destroys the WebGL resources held by this object.  Destroying an object allows for deterministic
     * release of WebGL resources, instead of relying on the garbage collector to destroy this object.
     * <br /><br />
     * Once an object is destroyed, it should not be used; calling any function other than
     * <code>isDestroyed</code> will result in a {@link DeveloperError} exception.  Therefore,
     * assign the return value (<code>undefined</code>) to the object as done in the example.
     *
     * @returns {undefined}
     *
     * @exception {DeveloperError} This object was destroyed, i.e., destroy() was called.
     *
     *
     * @example
     * provider = provider && provider();
     * 
     * @see GlobeSurfaceTileProvider#isDestroyed
     */
    GlobeSurfaceTileProvider.prototype.destroy = function() {
        this._tileProvider = this._tileProvider && this._tileProvider.destroy();
        return destroyObject(this);
    };

    GlobeSurfaceTileProvider.prototype._onLayerAdded = function(layer, index) {
        if (layer.show) {
            var terrainProvider = this._terrainProvider;

            // create TileImagerys for this layer for all previously loaded tiles
            this._quadtree.forEachLoadedTile(function(tile) {
                if (layer._createTileImagerySkeletons(tile, terrainProvider)) {
                    tile.state = QuadtreeTileLoadState.LOADING;
                }
            });

            this._layerOrderChanged = true;
        }
    };

    GlobeSurfaceTileProvider.prototype._onLayerRemoved = function(layer, index) {
        // destroy TileImagerys for this layer for all previously loaded tiles
        this._quadtree.forEachLoadedTile(function(tile) {
            var tileImageryCollection = tile.data.imagery;

            var startIndex = -1;
            var numDestroyed = 0;
            for (var i = 0, len = tileImageryCollection.length; i < len; ++i) {
                var tileImagery = tileImageryCollection[i];
                var imagery = tileImagery.loadingImagery;
                if (!defined(imagery)) {
                    imagery = tileImagery.readyImagery;
                }
                if (imagery.imageryLayer === layer) {
                    if (startIndex === -1) {
                        startIndex = i;
                    }

                    tileImagery.freeResources();
                    ++numDestroyed;
                } else if (startIndex !== -1) {
                    // iterated past the section of TileImagerys belonging to this layer, no need to continue.
                    break;
                }
            }

            if (startIndex !== -1) {
                tileImageryCollection.splice(startIndex, numDestroyed);
            }
        });
    };

    GlobeSurfaceTileProvider.prototype._onLayerMoved = function(layer, newIndex, oldIndex) {
        this._layerOrderChanged = true;
    };

    GlobeSurfaceTileProvider.prototype._onLayerShownOrHidden = function(layer, index, show) {
        if (show) {
            this._onLayerAdded(layer, index);
        } else {
            this._onLayerRemoved(layer, index);
        }
    };

    function createTileUniformMap() {
        var uniformMap = {
            u_initialColor : function() {
                return this.initialColor;
            },
            u_zoomedOutOceanSpecularIntensity : function() {
                return this.zoomedOutOceanSpecularIntensity;
            },
            u_oceanNormalMap : function() {
                return this.oceanNormalMap;
            },
            u_lightingFadeDistance : function() {
                return this.lightingFadeDistance;
            },
            u_center3D : function() {
                return this.center3D;
            },
            u_tileRectangle : function() {
                return this.tileRectangle;
            },
            u_modifiedModelView : function() {
                return this.modifiedModelView;
            },
            u_dayTextures : function() {
                return this.dayTextures;
            },
            u_dayTextureTranslationAndScale : function() {
                return this.dayTextureTranslationAndScale;
            },
            u_dayTextureTexCoordsRectangle : function() {
                return this.dayTextureTexCoordsRectangle;
            },
            u_dayTextureAlpha : function() {
                return this.dayTextureAlpha;
            },
            u_dayTextureBrightness : function() {
                return this.dayTextureBrightness;
            },
            u_dayTextureContrast : function() {
                return this.dayTextureContrast;
            },
            u_dayTextureHue : function() {
                return this.dayTextureHue;
            },
            u_dayTextureSaturation : function() {
                return this.dayTextureSaturation;
            },
            u_dayTextureOneOverGamma : function() {
                return this.dayTextureOneOverGamma;
            },
            u_dayIntensity : function() {
                return this.dayIntensity;
            },
            u_southAndNorthLatitude : function() {
                return this.southAndNorthLatitude;
            },
            u_southMercatorYAndOneOverHeight : function() {
                return this.southMercatorYAndOneOverHeight;
            },
            u_waterMask : function() {
                return this.waterMask;
            },
            u_waterMaskTranslationAndScale : function() {
                return this.waterMaskTranslationAndScale;
            },
            u_minMaxHeight : function() {
                return this.minMaxHeight;
            },
            u_scaleAndBias : function() {
                return this.scaleAndBias;
            },


            initialColor : new Cartesian4(0.0, 0.0, 0.5, 1.0),
            zoomedOutOceanSpecularIntensity : 0.5,
            oceanNormalMap : undefined,
            lightingFadeDistance : new Cartesian2(6500000.0, 9000000.0),

            center3D : undefined,
            modifiedModelView : new Matrix4(),
            tileRectangle : new Cartesian4(),

            dayTextures : [],
            dayTextureTranslationAndScale : [],
            dayTextureTexCoordsRectangle : [],
            dayTextureAlpha : [],
            dayTextureBrightness : [],
            dayTextureContrast : [],
            dayTextureHue : [],
            dayTextureSaturation : [],
            dayTextureOneOverGamma : [],
            dayIntensity : 0.0,

            southAndNorthLatitude : new Cartesian2(),
            southMercatorYAndOneOverHeight : new Cartesian2(),

            waterMask : undefined,
            waterMaskTranslationAndScale : new Cartesian4(),

            minMaxHeight : new Cartesian2(),
            scaleAndBias : new Matrix4()
        };

        return uniformMap;
    }

    function createWireframeVertexArrayIfNecessary(context, provider, tile) {
        var surfaceTile = tile.data;

        if (defined(surfaceTile.wireframeVertexArray)) {
            return;
        }

        if (defined(surfaceTile.meshForWireframePromise)) {
            return;
        }

        surfaceTile.meshForWireframePromise = surfaceTile.terrainData.createMesh(provider._terrainProvider.tilingScheme, tile.x, tile.y, tile.level);
        if (!defined(surfaceTile.meshForWireframePromise)) {
            // deferrred
            return;
        }

        var vertexArray = surfaceTile.vertexArray;

        when(surfaceTile.meshForWireframePromise, function(mesh) {
            if (surfaceTile.vertexArray === vertexArray) {
                surfaceTile.wireframeVertexArray = createWireframeVertexArray(context, surfaceTile.vertexArray, mesh);
            }
            surfaceTile.meshForWireframePromise = undefined;
        });
    }

    /**
     * Creates a vertex array for wireframe rendering of a terrain tile.
     *
     * @private
     *
     * @param {Context} context The context in which to create the vertex array.
     * @param {VertexArray} vertexArray The existing, non-wireframe vertex array.  The new vertex array
     *                      will share vertex buffers with this existing one.
     * @param {TerrainMesh} terrainMesh The terrain mesh containing non-wireframe indices.
     * @returns {VertexArray} The vertex array for wireframe rendering.
     */
    function createWireframeVertexArray(context, vertexArray, terrainMesh) {
        var geometry = {
            indices : terrainMesh.indices,
            primitiveType : PrimitiveType.TRIANGLES
        };

        GeometryPipeline.toWireframe(geometry);

        var wireframeIndices = geometry.indices;
        var wireframeIndexBuffer = Buffer.createIndexBuffer({
            context : context,
            typedArray : wireframeIndices,
            usage : BufferUsage.STATIC_DRAW,
            indexDatatype : IndexDatatype.UNSIGNED_SHORT
        });
        return new VertexArray({
            context : context,
            attributes : vertexArray._attributes,
            indexBuffer : wireframeIndexBuffer
        });
    }

    var getDebugOrientedBoundingBox;
    var getDebugBoundingSphere;
    var debugDestroyPrimitive;

    (function() {
        var instanceOBB = new GeometryInstance({
            geometry: BoxOutlineGeometry.fromDimensions({ dimensions: new Cartesian3(2.0, 2.0, 2.0) })
        });
        var instanceSphere = new GeometryInstance({
            geometry: new SphereOutlineGeometry({ radius: 1.0 })
        });
        var modelMatrix = new Matrix4();
        var previousVolume;
        var primitive;

        function createDebugPrimitive(instance) {
            return new Primitive({
                geometryInstances : instance,
                appearance : new PerInstanceColorAppearance({
                    translucent : false,
                    flat : true
                }),
                asynchronous : false
            });
        }

        getDebugOrientedBoundingBox = function(obb, color) {
            if (obb === previousVolume) {
                return primitive;
            }
            debugDestroyPrimitive();

            previousVolume = obb;
            modelMatrix = Matrix4.fromRotationTranslation(obb.halfAxes, obb.center, modelMatrix);

            instanceOBB.modelMatrix = modelMatrix;
            instanceOBB.attributes.color = ColorGeometryInstanceAttribute.fromColor(color);

            primitive = createDebugPrimitive(instanceOBB);
            return primitive;
        };

        getDebugBoundingSphere = function(sphere, color) {
            if (sphere === previousVolume) {
                return primitive;
            }
            debugDestroyPrimitive();

            previousVolume = sphere;
            modelMatrix = Matrix4.fromTranslation(sphere.center, modelMatrix);
            modelMatrix = Matrix4.multiplyByUniformScale(modelMatrix, sphere.radius, modelMatrix);

            instanceSphere.modelMatrix = modelMatrix;
            instanceSphere.attributes.color = ColorGeometryInstanceAttribute.fromColor(color);

            primitive = createDebugPrimitive(instanceSphere);
            return primitive;
        };

        debugDestroyPrimitive = function() {
            if (defined(primitive)) {
                primitive.destroy();
                primitive = undefined;
                previousVolume = undefined;
            }
        };
    })();

    var otherPassesInitialColor = new Cartesian4(0.0, 0.0, 0.0, 0.0);

    function addDrawCommandsForTile(tileProvider, tile, frameState) {
        var surfaceTile = tile.data;

        var viewMatrix = frameState.camera.viewMatrix;

        var maxTextures = ContextLimits.maximumTextureImageUnits;

        var waterMaskTexture = surfaceTile.waterMaskTexture;
        var showReflectiveOcean = tileProvider.hasWaterMask && defined(waterMaskTexture);
        var oceanNormalMap = tileProvider.oceanNormalMap;
        var showOceanWaves = showReflectiveOcean && defined(oceanNormalMap);
        var hasVertexNormals = tileProvider.terrainProvider.ready && tileProvider.terrainProvider.hasVertexNormals;
        var enableFog = frameState.fog.enabled;

        if (showReflectiveOcean) {
            --maxTextures;
        }
        if (showOceanWaves) {
            --maxTextures;
        }

        var rtc = surfaceTile.center;

        // Not used in 3D.
        var tileRectangle = tileRectangleScratch;

        // Only used for Mercator projections.
        var southLatitude = 0.0;
        var northLatitude = 0.0;
        var southMercatorY = 0.0;
        var oneOverMercatorHeight = 0.0;

        var useWebMercatorProjection = false;

        if (frameState.mode !== SceneMode.SCENE3D) {
            var projection = frameState.mapProjection;
            var southwest = projection.project(Rectangle.southwest(tile.rectangle), southwestScratch);
            var northeast = projection.project(Rectangle.northeast(tile.rectangle), northeastScratch);

            tileRectangle.x = southwest.x;
            tileRectangle.y = southwest.y;
            tileRectangle.z = northeast.x;
            tileRectangle.w = northeast.y;

            // In 2D and Columbus View, use the center of the tile for RTC rendering.
            if (frameState.mode !== SceneMode.MORPHING) {
                rtc = rtcScratch;
                rtc.x = 0.0;
                rtc.y = (tileRectangle.z + tileRectangle.x) * 0.5;
                rtc.z = (tileRectangle.w + tileRectangle.y) * 0.5;
                tileRectangle.x -= rtc.y;
                tileRectangle.y -= rtc.z;
                tileRectangle.z -= rtc.y;
                tileRectangle.w -= rtc.z;
            }

            if (projection instanceof WebMercatorProjection) {
                southLatitude = tile.rectangle.south;
                northLatitude = tile.rectangle.north;

                southMercatorY = WebMercatorProjection.geodeticLatitudeToMercatorAngle(southLatitude);

                oneOverMercatorHeight = 1.0 / (WebMercatorProjection.geodeticLatitudeToMercatorAngle(northLatitude) - southMercatorY);

                useWebMercatorProjection = true;
            }
        }

        var centerEye = Matrix4.multiplyByPoint(viewMatrix, rtc, centerEyeScratch);
        Matrix4.setTranslation(viewMatrix, centerEye, modifiedModelViewScratch);

        var tileImageryCollection = surfaceTile.imagery;
        var imageryIndex = 0;
        var imageryLen = tileImageryCollection.length;

        var firstPassRenderState = tileProvider._renderState;
        var otherPassesRenderState = tileProvider._blendRenderState;
        var renderState = firstPassRenderState;

        var initialColor = tileProvider._firstPassInitialColor;

        var context = frameState.context;

        if (!defined(tileProvider._debug.boundingSphereTile)) {
            debugDestroyPrimitive();
        }

        do {
            var numberOfDayTextures = 0;

            var command;
            var uniformMap;

            if (tileProvider._drawCommands.length <= tileProvider._usedDrawCommands) {
                command = new DrawCommand();
                command.owner = tile;
                command.cull = false;
                command.boundingVolume = new BoundingSphere();
                command.orientedBoundingBox = undefined;

                uniformMap = createTileUniformMap();

                tileProvider._drawCommands.push(command);
                tileProvider._uniformMaps.push(uniformMap);
            } else {
                command = tileProvider._drawCommands[tileProvider._usedDrawCommands];
                uniformMap = tileProvider._uniformMaps[tileProvider._usedDrawCommands];
            }

            command.owner = tile;

            ++tileProvider._usedDrawCommands;

            if (tile === tileProvider._debug.boundingSphereTile) {
                // If a debug primitive already exists for this tile, it will not be
                // re-created, to avoid allocation every frame. If it were possible
                // to have more than one selected tile, this would have to change.
                if (defined(surfaceTile.orientedBoundingBox)) {
                    getDebugOrientedBoundingBox(surfaceTile.orientedBoundingBox, Color.RED).update(frameState);
                } else if (defined(surfaceTile.boundingSphere3D)) {
                    getDebugBoundingSphere(surfaceTile.boundingSphere3D, Color.RED).update(frameState);
                }
            }

            Cartesian4.clone(initialColor, uniformMap.initialColor);
            uniformMap.oceanNormalMap = oceanNormalMap;
            uniformMap.lightingFadeDistance.x = tileProvider.lightingFadeOutDistance;
            uniformMap.lightingFadeDistance.y = tileProvider.lightingFadeInDistance;
            uniformMap.zoomedOutOceanSpecularIntensity = tileProvider.zoomedOutOceanSpecularIntensity;

            uniformMap.center3D = surfaceTile.center;

            Cartesian4.clone(tileRectangle, uniformMap.tileRectangle);
            uniformMap.southAndNorthLatitude.x = southLatitude;
            uniformMap.southAndNorthLatitude.y = northLatitude;
            uniformMap.southMercatorYAndOneOverHeight.x = southMercatorY;
            uniformMap.southMercatorYAndOneOverHeight.y = oneOverMercatorHeight;
            Matrix4.clone(modifiedModelViewScratch, uniformMap.modifiedModelView);

            // For performance, use fog in the shader only when the tile is in fog.
            var applyFog = enableFog && CesiumMath.fog(tile._distance, frameState.fog.density) > CesiumMath.EPSILON3;

            var applyBrightness = false;
            var applyContrast = false;
            var applyHue = false;
            var applySaturation = false;
            var applyGamma = false;
            var applyAlpha = false;

            while (numberOfDayTextures < maxTextures && imageryIndex < imageryLen) {
                var tileImagery = tileImageryCollection[imageryIndex];
                var imagery = tileImagery.readyImagery;
                ++imageryIndex;

                if (!defined(imagery) || imagery.state !== ImageryState.READY || imagery.imageryLayer.alpha === 0.0) {
                    continue;
                }

                var imageryLayer = imagery.imageryLayer;

                if (!defined(tileImagery.textureTranslationAndScale)) {
                    tileImagery.textureTranslationAndScale = imageryLayer._calculateTextureTranslationAndScale(tile, tileImagery);
                }

                uniformMap.dayTextures[numberOfDayTextures] = imagery.texture;
                uniformMap.dayTextureTranslationAndScale[numberOfDayTextures] = tileImagery.textureTranslationAndScale;
                uniformMap.dayTextureTexCoordsRectangle[numberOfDayTextures] = tileImagery.textureCoordinateRectangle;

                uniformMap.dayTextureAlpha[numberOfDayTextures] = imageryLayer.alpha;
                applyAlpha = applyAlpha || uniformMap.dayTextureAlpha[numberOfDayTextures] !== 1.0;

                uniformMap.dayTextureBrightness[numberOfDayTextures] = imageryLayer.brightness;
                applyBrightness = applyBrightness || uniformMap.dayTextureBrightness[numberOfDayTextures] !== ImageryLayer.DEFAULT_BRIGHTNESS;

                uniformMap.dayTextureContrast[numberOfDayTextures] = imageryLayer.contrast;
                applyContrast = applyContrast || uniformMap.dayTextureContrast[numberOfDayTextures] !== ImageryLayer.DEFAULT_CONTRAST;

                uniformMap.dayTextureHue[numberOfDayTextures] = imageryLayer.hue;
                applyHue = applyHue || uniformMap.dayTextureHue[numberOfDayTextures] !== ImageryLayer.DEFAULT_HUE;

                uniformMap.dayTextureSaturation[numberOfDayTextures] = imageryLayer.saturation;
                applySaturation = applySaturation || uniformMap.dayTextureSaturation[numberOfDayTextures] !== ImageryLayer.DEFAULT_SATURATION;

                uniformMap.dayTextureOneOverGamma[numberOfDayTextures] = 1.0 / imageryLayer.gamma;
                applyGamma = applyGamma || uniformMap.dayTextureOneOverGamma[numberOfDayTextures] !== 1.0 / ImageryLayer.DEFAULT_GAMMA;

                if (defined(imagery.credits)) {
                    var creditDisplay = frameState.creditDisplay;
                    var credits = imagery.credits;
                    for (var creditIndex = 0, creditLength = credits.length; creditIndex < creditLength; ++creditIndex) {
                        creditDisplay.addCredit(credits[creditIndex]);
                    }
                }

                ++numberOfDayTextures;
            }

            // trim texture array to the used length so we don't end up using old textures
            // which might get destroyed eventually
            uniformMap.dayTextures.length = numberOfDayTextures;
            uniformMap.waterMask = waterMaskTexture;
            Cartesian4.clone(surfaceTile.waterMaskTranslationAndScale, uniformMap.waterMaskTranslationAndScale);

            var encoding = surfaceTile.pickTerrain.mesh.encoding;
            uniformMap.minMaxHeight.x = encoding.minimumHeight;
            uniformMap.minMaxHeight.y = encoding.maximumHeight;
            Matrix4.clone(encoding.matrix, uniformMap.scaleAndBias);

            command.shaderProgram = tileProvider._surfaceShaderSet.getShaderProgram(frameState, surfaceTile, numberOfDayTextures, applyBrightness, applyContrast, applyHue, applySaturation, applyGamma, applyAlpha, showReflectiveOcean, showOceanWaves, tileProvider.enableLighting, hasVertexNormals, useWebMercatorProjection, applyFog);
            command.renderState = renderState;
            command.primitiveType = PrimitiveType.TRIANGLES;
            command.vertexArray = surfaceTile.vertexArray;
            command.uniformMap = uniformMap;
            command.pass = Pass.GLOBE;

            if (tileProvider._debug.wireframe) {
                createWireframeVertexArrayIfNecessary(context, tileProvider, tile);
                if (defined(surfaceTile.wireframeVertexArray)) {
                    command.vertexArray = surfaceTile.wireframeVertexArray;
                    command.primitiveType = PrimitiveType.LINES;
                }
            }

            var boundingVolume = command.boundingVolume;
            var orientedBoundingBox = command.orientedBoundingBox;

            if (frameState.mode !== SceneMode.SCENE3D) {
                BoundingSphere.fromRectangleWithHeights2D(tile.rectangle, frameState.mapProjection, surfaceTile.minimumHeight, surfaceTile.maximumHeight, boundingVolume);
                Cartesian3.fromElements(boundingVolume.center.z, boundingVolume.center.x, boundingVolume.center.y, boundingVolume.center);

                if (frameState.mode === SceneMode.MORPHING) {
                    boundingVolume = BoundingSphere.union(surfaceTile.boundingSphere3D, boundingVolume, boundingVolume);
                }
            } else {
                command.boundingVolume = BoundingSphere.clone(surfaceTile.boundingSphere3D, boundingVolume);
                command.orientedBoundingBox = OrientedBoundingBox.clone(surfaceTile.orientedBoundingBox, orientedBoundingBox);
            }

            frameState.commandList.push(command);

            renderState = otherPassesRenderState;
            initialColor = otherPassesInitialColor;
        } while (imageryIndex < imageryLen);
    }

    function addPickCommandsForTile(tileProvider, drawCommand, frameState) {
        var pickCommand;
        if (tileProvider._pickCommands.length <= tileProvider._usedPickCommands) {
            pickCommand = new DrawCommand();
            pickCommand.cull = false;

            tileProvider._pickCommands.push(pickCommand);
        } else {
            pickCommand = tileProvider._pickCommands[tileProvider._usedPickCommands];
        }

        ++tileProvider._usedPickCommands;

        var surfaceTile = drawCommand.owner.data;
        var useWebMercatorProjection = frameState.projection instanceof WebMercatorProjection;

        pickCommand.shaderProgram = tileProvider._surfaceShaderSet.getPickShaderProgram(frameState, surfaceTile, useWebMercatorProjection);
        pickCommand.renderState = tileProvider._pickRenderState;

        pickCommand.owner = drawCommand.owner;
        pickCommand.primitiveType = drawCommand.primitiveType;
        pickCommand.vertexArray = drawCommand.vertexArray;
        pickCommand.uniformMap = drawCommand.uniformMap;
        pickCommand.boundingVolume = drawCommand.boundingVolume;
        pickCommand.orientedBoundingBox = pickCommand.orientedBoundingBox;
        pickCommand.pass = drawCommand.pass;

        frameState.commandList.push(pickCommand);
    }

    return GlobeSurfaceTileProvider;
});
