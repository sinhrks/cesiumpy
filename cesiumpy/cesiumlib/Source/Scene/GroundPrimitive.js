/*global define*/
define([
        '../Core/BoundingSphere',
        '../Core/Cartesian3',
        '../Core/Cartographic',
        '../Core/defaultValue',
        '../Core/defined',
        '../Core/defineProperties',
        '../Core/destroyObject',
        '../Core/DeveloperError',
        '../Core/GeometryInstance',
        '../Core/isArray',
        '../Core/Math',
        '../Core/Matrix3',
        '../Core/Matrix4',
        '../Core/OrientedBoundingBox',
        '../Core/Rectangle',
        '../Renderer/DrawCommand',
        '../Renderer/RenderState',
        '../Renderer/ShaderProgram',
        '../Renderer/ShaderSource',
        '../Shaders/ShadowVolumeFS',
        '../Shaders/ShadowVolumeVS',
        '../ThirdParty/when',
        './BlendingState',
        './DepthFunction',
        './Pass',
        './PerInstanceColorAppearance',
        './Primitive',
        './SceneMode',
        './StencilFunction',
        './StencilOperation'
    ], function(
        BoundingSphere,
        Cartesian3,
        Cartographic,
        defaultValue,
        defined,
        defineProperties,
        destroyObject,
        DeveloperError,
        GeometryInstance,
        isArray,
        CesiumMath,
        Matrix3,
        Matrix4,
        OrientedBoundingBox,
        Rectangle,
        DrawCommand,
        RenderState,
        ShaderProgram,
        ShaderSource,
        ShadowVolumeFS,
        ShadowVolumeVS,
        when,
        BlendingState,
        DepthFunction,
        Pass,
        PerInstanceColorAppearance,
        Primitive,
        SceneMode,
        StencilFunction,
        StencilOperation) {
    "use strict";

    /**
     * A ground primitive represents geometry draped over the terrain in the {@link Scene}.  The geometry must be from a single {@link GeometryInstance}.
     * Batching multiple geometries is not yet supported.
     * <p>
     * A primitive combines the geometry instance with an {@link Appearance} that describes the full shading, including
     * {@link Material} and {@link RenderState}.  Roughly, the geometry instance defines the structure and placement,
     * and the appearance defines the visual characteristics.  Decoupling geometry and appearance allows us to mix
     * and match most of them and add a new geometry or appearance independently of each other. Only the {@link PerInstanceColorAppearance}
     * is supported at this time.
     * </p>
     * <p>
     * Valid geometries are {@link CircleGeometry}, {@link CorridorGeometry}, {@link EllipseGeometry}, {@link PolygonGeometry}, and {@link RectangleGeometry}.
     * </p>
     *
     * @alias GroundPrimitive
     * @constructor
     *
     * @param {Object} [options] Object with the following properties:
     * @param {GeometryInstance} [options.geometryInstance] A single geometry instance to render.
     * @param {Boolean} [options.show=true] Determines if this primitive will be shown.
     * @param {Boolean} [options.vertexCacheOptimize=false] When <code>true</code>, geometry vertices are optimized for the pre and post-vertex-shader caches.
     * @param {Boolean} [options.interleave=false] When <code>true</code>, geometry vertex attributes are interleaved, which can slightly improve rendering performance but increases load time.
     * @param {Boolean} [options.compressVertices=true] When <code>true</code>, the geometry vertices are compressed, which will save memory.
     * @param {Boolean} [options.releaseGeometryInstances=true] When <code>true</code>, the primitive does not keep a reference to the input <code>geometryInstances</code> to save memory.
     * @param {Boolean} [options.allowPicking=true] When <code>true</code>, each geometry instance will only be pickable with {@link Scene#pick}.  When <code>false</code>, GPU memory is saved.
     * @param {Boolean} [options.asynchronous=true] Determines if the primitive will be created asynchronously or block until ready.
     * @param {Boolean} [options.debugShowBoundingVolume=false] For debugging only. Determines if this primitive's commands' bounding spheres are shown.
     *
     *
     * @example
     * var rectangleInstance = new Cesium.GeometryInstance({
     *   geometry : new Cesium.RectangleGeometry({
     *     rectangle : Cesium.Rectangle.fromDegrees(-140.0, 30.0, -100.0, 40.0)
     *   }),
     *   id : 'rectangle',
     *   attributes : {
     *     color : new Cesium.ColorGeometryInstanceAttribute(0.0, 1.0, 1.0, 0.5)
     *   }
     * });
     * scene.primitives.add(new Cesium.GroundPrimitive({
     *   geometryInstance : rectangleInstance
     * }));
     * 
     * @see Primitive
     * @see GeometryInstance
     * @see Appearance
     */
    function GroundPrimitive(options) {
        options = defaultValue(options, defaultValue.EMPTY_OBJECT);

        /**
         * The geometry instance rendered with this primitive.  This may
         * be <code>undefined</code> if <code>options.releaseGeometryInstances</code>
         * is <code>true</code> when the primitive is constructed.
         * <p>
         * Changing this property after the primitive is rendered has no effect.
         * </p>
         *
         * @type Array
         *
         * @default undefined
         */
        this.geometryInstance = options.geometryInstance;
        /**
         * Determines if the primitive will be shown.  This affects all geometry
         * instances in the primitive.
         *
         * @type Boolean
         *
         * @default true
         */
        this.show = defaultValue(options.show, true);
        /**
         * This property is for debugging only; it is not for production use nor is it optimized.
         * <p>
         * Draws the bounding sphere for each draw command in the primitive.
         * </p>
         *
         * @type {Boolean}
         *
         * @default false
         */
        this.debugShowBoundingVolume = defaultValue(options.debugShowBoundingVolume, false);

        this._sp = undefined;
        this._spPick = undefined;

        this._rsStencilPreloadPass = undefined;
        this._rsStencilDepthPass = undefined;
        this._rsColorPass = undefined;
        this._rsPickPass = undefined;

        this._boundingVolumes = [];
        this._boundingVolumes2D = [];

        this._ready = false;
        this._readyPromise = when.defer();

        this._primitive = undefined;

        var appearance = new PerInstanceColorAppearance({
            flat : true
        });

        this._primitiveOptions = {
            geometryInstances : undefined,
            appearance : appearance,
            vertexCacheOptimize : defaultValue(options.vertexCacheOptimize, false),
            interleave : defaultValue(options.interleave, false),
            releaseGeometryInstances : defaultValue(options.releaseGeometryInstances, true),
            allowPicking : defaultValue(options.allowPicking, true),
            asynchronous : defaultValue(options.asynchronous, true),
            compressVertices : defaultValue(options.compressVertices, true),
            _createRenderStatesFunction : undefined,
            _createShaderProgramFunction : undefined,
            _createCommandsFunction : undefined
        };
    }

    defineProperties(GroundPrimitive.prototype, {
        /**
         * When <code>true</code>, geometry vertices are optimized for the pre and post-vertex-shader caches.
         *
         * @memberof GroundPrimitive.prototype
         *
         * @type {Boolean}
         * @readonly
         *
         * @default true
         */
        vertexCacheOptimize : {
            get : function() {
                return this._primitiveOptions.vertexCacheOptimize;
            }
        },

        /**
         * Determines if geometry vertex attributes are interleaved, which can slightly improve rendering performance.
         *
         * @memberof GroundPrimitive.prototype
         *
         * @type {Boolean}
         * @readonly
         *
         * @default false
         */
        interleave : {
            get : function() {
                return this._primitiveOptions.interleave;
            }
        },

        /**
         * When <code>true</code>, the primitive does not keep a reference to the input <code>geometryInstances</code> to save memory.
         *
         * @memberof GroundPrimitive.prototype
         *
         * @type {Boolean}
         * @readonly
         *
         * @default true
         */
        releaseGeometryInstances : {
            get : function() {
                return this._primitiveOptions.releaseGeometryInstances;
            }
        },

        /**
         * When <code>true</code>, each geometry instance will only be pickable with {@link Scene#pick}.  When <code>false</code>, GPU memory is saved.
         *
         * @memberof GroundPrimitive.prototype
         *
         * @type {Boolean}
         * @readonly
         *
         * @default true
         */
        allowPicking : {
            get : function() {
                return this._primitiveOptions.allowPicking;
            }
        },

        /**
         * Determines if the geometry instances will be created and batched on a web worker.
         *
         * @memberof GroundPrimitive.prototype
         *
         * @type {Boolean}
         * @readonly
         *
         * @default true
         */
        asynchronous : {
            get : function() {
                return this._primitiveOptions.asynchronous;
            }
        },

        /**
         * When <code>true</code>, geometry vertices are compressed, which will save memory.
         *
         * @memberof GroundPrimitive.prototype
         *
         * @type {Boolean}
         * @readonly
         *
         * @default true
         */
        compressVertices : {
            get : function() {
                return this._primitiveOptions.compressVertices;
            }
        },

        /**
         * Determines if the primitive is complete and ready to render.  If this property is
         * true, the primitive will be rendered the next time that {@link GroundPrimitive#update}
         * is called.
         *
         * @memberof GroundPrimitive.prototype
         *
         * @type {Boolean}
         * @readonly
         */
        ready : {
            get : function() {
                return this._ready;
            }
        },

        /**
         * Gets a promise that resolves when the primitive is ready to render.
         * @memberof GroundPrimitive.prototype
         * @type {Promise.<GroundPrimitive>}
         * @readonly
         */
        readyPromise : {
            get : function() {
                return this._readyPromise.promise;
            }
        }
    });

    /**
     * Determines if GroundPrimitive rendering is supported.
     *
     * @param {Scene} scene The scene.
     * @returns {Boolean} <code>true</code> if GroundPrimitives are supported; otherwise, returns <code>false</code>
     */
    GroundPrimitive.isSupported = function(scene) {
        return scene.context.fragmentDepth;
    };

    GroundPrimitive._maxHeight = undefined;
    GroundPrimitive._minHeight = undefined;
    GroundPrimitive._minOBBHeight = undefined;

    GroundPrimitive._maxTerrainHeight = 9000.0;
    GroundPrimitive._minTerrainHeight = -100000.0;
    GroundPrimitive._minOBBTerrainHeight = -11500.0;

    function computeMaximumHeight(granularity, ellipsoid) {
        var r = ellipsoid.maximumRadius;
        var delta = (r / Math.cos(granularity * 0.5)) - r;
        return GroundPrimitive._maxHeight + delta;
    }

    function computeMinimumHeight(granularity, ellipsoid) {
        return GroundPrimitive._minHeight;
    }

    var stencilPreloadRenderState = {
        colorMask : {
            red : false,
            green : false,
            blue : false,
            alpha : false
        },
        stencilTest : {
            enabled : true,
            frontFunction : StencilFunction.ALWAYS,
            frontOperation : {
                fail : StencilOperation.KEEP,
                zFail : StencilOperation.DECREMENT_WRAP,
                zPass : StencilOperation.DECREMENT_WRAP
            },
            backFunction : StencilFunction.ALWAYS,
            backOperation : {
                fail : StencilOperation.KEEP,
                zFail : StencilOperation.INCREMENT_WRAP,
                zPass : StencilOperation.INCREMENT_WRAP
            },
            reference : 0,
            mask : ~0
        },
        depthTest : {
            enabled : false
        },
        depthMask : false
    };

    var stencilDepthRenderState = {
        colorMask : {
            red : false,
            green : false,
            blue : false,
            alpha : false
        },
        stencilTest : {
            enabled : true,
            frontFunction : StencilFunction.ALWAYS,
            frontOperation : {
                fail : StencilOperation.KEEP,
                zFail : StencilOperation.KEEP,
                zPass : StencilOperation.INCREMENT_WRAP
            },
            backFunction : StencilFunction.ALWAYS,
            backOperation : {
                fail : StencilOperation.KEEP,
                zFail : StencilOperation.KEEP,
                zPass : StencilOperation.DECREMENT_WRAP
            },
            reference : 0,
            mask : ~0
        },
        depthTest : {
            enabled : true,
            func : DepthFunction.LESS_OR_EQUAL
        },
        depthMask : false
    };

    var colorRenderState = {
        stencilTest : {
            enabled : true,
            frontFunction : StencilFunction.NOT_EQUAL,
            frontOperation : {
                fail : StencilOperation.KEEP,
                zFail : StencilOperation.KEEP,
                zPass : StencilOperation.DECREMENT_WRAP
            },
            backFunction : StencilFunction.NOT_EQUAL,
            backOperation : {
                fail : StencilOperation.KEEP,
                zFail : StencilOperation.KEEP,
                zPass : StencilOperation.DECREMENT_WRAP
            },
            reference : 0,
            mask : ~0
        },
        depthTest : {
            enabled : false
        },
        depthMask : false,
        blending : BlendingState.ALPHA_BLEND
    };

    var pickRenderState = {
        stencilTest : {
            enabled : true,
            frontFunction : StencilFunction.NOT_EQUAL,
            frontOperation : {
                fail : StencilOperation.KEEP,
                zFail : StencilOperation.KEEP,
                zPass : StencilOperation.DECREMENT_WRAP
            },
            backFunction : StencilFunction.NOT_EQUAL,
            backOperation : {
                fail : StencilOperation.KEEP,
                zFail : StencilOperation.KEEP,
                zPass : StencilOperation.DECREMENT_WRAP
            },
            reference : 0,
            mask : ~0
        },
        depthTest : {
            enabled : false
        },
        depthMask : false
    };

    var scratchBVCartesianHigh = new Cartesian3();
    var scratchBVCartesianLow = new Cartesian3();
    var scratchBVCartesian = new Cartesian3();
    var scratchBVCartographic = new Cartographic();
    var scratchBVRectangle = new Rectangle();

    function createBoundingVolume(primitive, frameState, geometry) {
        var highPositions = geometry.attributes.position3DHigh.values;
        var lowPositions = geometry.attributes.position3DLow.values;
        var length = highPositions.length;

        var ellipsoid = frameState.mapProjection.ellipsoid;

        var minLat = Number.POSITIVE_INFINITY;
        var minLon = Number.POSITIVE_INFINITY;
        var maxLat = Number.NEGATIVE_INFINITY;
        var maxLon = Number.NEGATIVE_INFINITY;

        for (var i = 0; i < length; i +=3) {
            var highPosition = Cartesian3.unpack(highPositions, i, scratchBVCartesianHigh);
            var lowPosition = Cartesian3.unpack(lowPositions, i, scratchBVCartesianLow);

            var position = Cartesian3.add(highPosition, lowPosition, scratchBVCartesian);
            var cartographic = ellipsoid.cartesianToCartographic(position, scratchBVCartographic);

            var latitude = cartographic.latitude;
            var longitude = cartographic.longitude;

            minLat = Math.min(minLat, latitude);
            minLon = Math.min(minLon, longitude);
            maxLat = Math.max(maxLat, latitude);
            maxLon = Math.max(maxLon, longitude);
        }

        var rectangle = scratchBVRectangle;
        rectangle.north = maxLat;
        rectangle.south = minLat;
        rectangle.east = maxLon;
        rectangle.west = minLon;

        var obb = OrientedBoundingBox.fromRectangle(rectangle, GroundPrimitive._maxHeight, GroundPrimitive._minOBBHeight, ellipsoid);
        primitive._boundingVolumes.push(obb);

        if (!frameState.scene3DOnly) {
            var projection = frameState.mapProjection;
            var boundingVolume = BoundingSphere.fromRectangleWithHeights2D(rectangle, projection, GroundPrimitive._maxHeight, GroundPrimitive._minOBBHeight);
            Cartesian3.fromElements(boundingVolume.center.z, boundingVolume.center.x, boundingVolume.center.y, boundingVolume.center);

            primitive._boundingVolumes2D.push(boundingVolume);
        }
    }

    function createRenderStates(primitive, context, appearance, twoPasses) {
        if (defined(primitive._rsStencilPreloadPass)) {
            return;
        }

        primitive._rsStencilPreloadPass = RenderState.fromCache(stencilPreloadRenderState);
        primitive._rsStencilDepthPass = RenderState.fromCache(stencilDepthRenderState);
        primitive._rsColorPass = RenderState.fromCache(colorRenderState);
        primitive._rsPickPass = RenderState.fromCache(pickRenderState);
    }

    function createShaderProgram(primitive, frameState, appearance) {
        if (defined(primitive._sp)) {
            return;
        }

        var context = frameState.context;

        var vs = Primitive._modifyShaderPosition(primitive, ShadowVolumeVS, frameState.scene3DOnly);
        vs = Primitive._appendShowToShader(primitive._primitive, vs);

        var fs = ShadowVolumeFS;
        var attributeLocations = primitive._primitive._attributeLocations;

        primitive._sp = ShaderProgram.replaceCache({
            context : context,
            shaderProgram : primitive._sp,
            vertexShaderSource : vs,
            fragmentShaderSource : fs,
            attributeLocations : attributeLocations
        });

        if (primitive._primitive.allowPicking) {
            var pickFS = new ShaderSource({
                sources : [fs],
                pickColorQualifier : 'varying'
            });
            primitive._spPick = ShaderProgram.replaceCache({
                context : context,
                shaderProgram : primitive._spPick,
                vertexShaderSource : ShaderSource.createPickVertexShaderSource(vs),
                fragmentShaderSource : pickFS,
                attributeLocations : attributeLocations
            });
        } else {
            primitive._spPick = ShaderProgram.fromCache({
                context : context,
                vertexShaderSource : vs,
                fragmentShaderSource : fs,
                attributeLocations : attributeLocations
            });
        }
    }

    function createCommands(groundPrimitive, appearance, material, translucent, twoPasses, colorCommands, pickCommands) {
        var primitive = groundPrimitive._primitive;
        var length = primitive._va.length * 3;

        colorCommands.length = length;
        pickCommands.length = length;

        var vaIndex = 0;

        for (var i = 0; i < length; i += 3) {
            var vertexArray = primitive._va[vaIndex];

            // stencil preload command
            var command = colorCommands[i];
            if (!defined(command)) {
                command = colorCommands[i] = new DrawCommand({
                    owner : groundPrimitive,
                    primitiveType : primitive._primitiveType
                });
            }

            command.vertexArray = vertexArray;
            command.renderState = groundPrimitive._rsStencilPreloadPass;
            command.shaderProgram = groundPrimitive._sp;
            command.uniformMap = {};
            command.pass = Pass.GROUND;

            // stencil depth command
            command = colorCommands[i + 1];
            if (!defined(command)) {
                command = colorCommands[i + 1] = new DrawCommand({
                    owner : groundPrimitive,
                    primitiveType : primitive._primitiveType
                });
            }

            command.vertexArray = vertexArray;
            command.renderState = groundPrimitive._rsStencilDepthPass;
            command.shaderProgram = groundPrimitive._sp;
            command.uniformMap = {};
            command.pass = Pass.GROUND;

            // color command
            command = colorCommands[i + 2];
            if (!defined(command)) {
                command = colorCommands[i + 2] = new DrawCommand({
                    owner : groundPrimitive,
                    primitiveType : primitive._primitiveType
                });
            }

            command.vertexArray = vertexArray;
            command.renderState = groundPrimitive._rsColorPass;
            command.shaderProgram = groundPrimitive._sp;
            command.uniformMap = {};
            command.pass = Pass.GROUND;

            // pick stencil preload and depth are the same as the color pass
            pickCommands[i] = colorCommands[i];
            pickCommands[i + 1] = colorCommands[i + 1];

            command = pickCommands[i + 2];
            if (!defined(command)) {
                command = pickCommands[i + 2] = new DrawCommand({
                    owner : groundPrimitive,
                    primitiveType : primitive._primitiveType
                });
            }

            command.vertexArray = vertexArray;
            command.renderState = groundPrimitive._rsPickPass;
            command.shaderProgram = groundPrimitive._spPick;
            command.uniformMap = {};
            command.pass = Pass.GROUND;
        }
    }

    function updateAndQueueCommands(primitive, frameState, colorCommands, pickCommands, modelMatrix, cull, debugShowBoundingVolume, twoPasses) {
        var boundingVolumes;
        if (frameState.mode === SceneMode.SCENE3D) {
            boundingVolumes = primitive._boundingVolumes;
        } else if (frameState.mode !== SceneMode.SCENE3D && defined(primitive._boundingVolumes2D)) {
            boundingVolumes = primitive._boundingVolumes2D;
        }

        var commandList = frameState.commandList;
        var passes = frameState.passes;
        if (passes.render) {
            var colorLength = colorCommands.length;
            for (var j = 0; j < colorLength; ++j) {
                colorCommands[j].modelMatrix = modelMatrix;
                colorCommands[j].boundingVolume = boundingVolumes[Math.floor(j / 3)];
                colorCommands[j].cull = cull;
                colorCommands[j].debugShowBoundingVolume = debugShowBoundingVolume;

                commandList.push(colorCommands[j]);
            }
        }

        if (passes.pick) {
            var pickLength = pickCommands.length;
            for (var k = 0; k < pickLength; ++k) {
                pickCommands[k].modelMatrix = modelMatrix;
                pickCommands[k].boundingVolume = boundingVolumes[Math.floor(k / 3)];
                pickCommands[k].cull = cull;

                commandList.push(pickCommands[k]);
            }
        }
    }

    /**
     * Called when {@link Viewer} or {@link CesiumWidget} render the scene to
     * get the draw commands needed to render this primitive.
     * <p>
     * Do not call this function directly.  This is documented just to
     * list the exceptions that may be propagated when the scene is rendered:
     * </p>
     *
     * @exception {DeveloperError} All instance geometries must have the same primitiveType.
     * @exception {DeveloperError} Appearance and material have a uniform with the same name.
     */
    GroundPrimitive.prototype.update = function(frameState) {
        var context = frameState.context;
        if (!context.fragmentDepth || !this.show || (!defined(this._primitive) && !defined(this.geometryInstance))) {
            return;
        }

        if (!defined(GroundPrimitive._maxHeight)) {
            var exaggeration = frameState.terrainExaggeration;
            GroundPrimitive._maxHeight = GroundPrimitive._maxTerrainHeight * exaggeration;
            GroundPrimitive._minHeight = GroundPrimitive._minTerrainHeight * exaggeration;
            GroundPrimitive._minOBBHeight = GroundPrimitive._minOBBTerrainHeight * exaggeration;
        }

        if (!defined(this._primitive)) {
            var instance = this.geometryInstance;
            var geometry = instance.geometry;

            var instanceType = geometry.constructor;
            if (defined(instanceType) && defined(instanceType.createShadowVolume)) {
                instance = new GeometryInstance({
                    geometry : instanceType.createShadowVolume(geometry, computeMinimumHeight, computeMaximumHeight),
                    attributes : instance.attributes,
                    modelMatrix : Matrix4.IDENTITY,
                    id : instance.id,
                    pickPrimitive : this
                });
            }

            var primitiveOptions = this._primitiveOptions;
            primitiveOptions.geometryInstances = instance;

            var that = this;
            this._primitiveOptions._createBoundingVolumeFunction = function(frameState, geometry) {
                createBoundingVolume(that, frameState, geometry);
            };
            this._primitiveOptions._createRenderStatesFunction = function(primitive, context, appearance, twoPasses) {
                createRenderStates(that, context);
            };
            this._primitiveOptions._createShaderProgramFunction = function(primitive, frameState, appearance) {
                createShaderProgram(that, frameState);
            };
            this._primitiveOptions._createCommandsFunction = function(primitive, appearance, material, translucent, twoPasses, colorCommands, pickCommands) {
                createCommands(that, undefined, undefined, true, false, colorCommands, pickCommands);
            };
            this._primitiveOptions._updateAndQueueCommandsFunction = function(primitive, frameState, colorCommands, pickCommands, modelMatrix, cull, debugShowBoundingVolume, twoPasses) {
                updateAndQueueCommands(that, frameState, colorCommands, pickCommands, modelMatrix, cull, debugShowBoundingVolume, twoPasses);
            };

            this._primitive = new Primitive(primitiveOptions);
            this._primitive.readyPromise.then(function(primitive) {
                that._ready = true;

                if (that.releaseGeometryInstances) {
                    that.geometryInstance = undefined;
                }

                var error = primitive._error;
                if (!defined(error)) {
                    that._readyPromise.resolve(that);
                } else {
                    that._readyPromise.reject(error);
                }
            });
        }

        this._primitive.debugShowBoundingVolume = this.debugShowBoundingVolume;
        this._primitive.update(frameState);
    };

    /**
     * Returns the modifiable per-instance attributes for a {@link GeometryInstance}.
     *
     * @param {Object} id The id of the {@link GeometryInstance}.
     * @returns {Object} The typed array in the attribute's format or undefined if the is no instance with id.
     *
     * @exception {DeveloperError} must call update before calling getGeometryInstanceAttributes.
     *
     * @example
     * var attributes = primitive.getGeometryInstanceAttributes('an id');
     * attributes.color = Cesium.ColorGeometryInstanceAttribute.toValue(Cesium.Color.AQUA);
     * attributes.show = Cesium.ShowGeometryInstanceAttribute.toValue(true);
     */
    GroundPrimitive.prototype.getGeometryInstanceAttributes = function(id) {
        //>>includeStart('debug', pragmas.debug);
        if (!defined(this._primitive)) {
            throw new DeveloperError('must call update before calling getGeometryInstanceAttributes');
        }
        //>>includeEnd('debug');
        return this._primitive.getGeometryInstanceAttributes(id);
    };

    /**
     * Returns true if this object was destroyed; otherwise, false.
     * <p>
     * If this object was destroyed, it should not be used; calling any function other than
     * <code>isDestroyed</code> will result in a {@link DeveloperError} exception.
     * </p>
     *
     * @returns {Boolean} <code>true</code> if this object was destroyed; otherwise, <code>false</code>.
     *
     * @see GroundPrimitive#destroy
     */
    GroundPrimitive.prototype.isDestroyed = function() {
        return false;
    };

    /**
     * Destroys the WebGL resources held by this object.  Destroying an object allows for deterministic
     * release of WebGL resources, instead of relying on the garbage collector to destroy this object.
     * <p>
     * Once an object is destroyed, it should not be used; calling any function other than
     * <code>isDestroyed</code> will result in a {@link DeveloperError} exception.  Therefore,
     * assign the return value (<code>undefined</code>) to the object as done in the example.
     * </p>
     *
     * @returns {undefined}
     *
     * @exception {DeveloperError} This object was destroyed, i.e., destroy() was called.
     *
     *
     * @example
     * e = e && e.destroy();
     * 
     * @see GroundPrimitive#isDestroyed
     */
    GroundPrimitive.prototype.destroy = function() {
        this._primitive = this._primitive && this._primitive.destroy();
        this._sp = this._sp && this._sp.destroy();
        this._spPick = this._spPick && this._spPick.destroy();
        return destroyObject(this);
    };

    return GroundPrimitive;
});
