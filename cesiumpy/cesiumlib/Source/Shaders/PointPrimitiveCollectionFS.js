//This file is automatically rebuilt by the Cesium build process.
/*global define*/
define(function() {
    "use strict";
    return "varying vec4 v_color;\n\
varying vec4 v_outlineColor;\n\
varying float v_innerPercent;\n\
varying float v_pixelDistance;\n\
\n\
#ifdef RENDER_FOR_PICK\n\
varying vec4 v_pickColor;\n\
#endif\n\
\n\
void main()\n\
{\n\
    // The distance in UV space from this fragment to the center of the point, at most 0.5.\n\
    float distanceToCenter = length(gl_PointCoord - vec2(0.5));\n\
    // The max distance stops one pixel shy of the edge to leave space for anti-aliasing.\n\
    float maxDistance = max(0.0, 0.5 - v_pixelDistance);\n\
    float wholeAlpha = 1.0 - smoothstep(maxDistance, 0.5, distanceToCenter);\n\
    float innerAlpha = 1.0 - smoothstep(maxDistance * v_innerPercent, 0.5 * v_innerPercent, distanceToCenter);\n\
\n\
    vec4 color = mix(v_outlineColor, v_color, innerAlpha);\n\
    color.a *= wholeAlpha;\n\
    if (color.a < 0.005)\n\
    {\n\
        discard;\n\
    }\n\
\n\
#ifdef RENDER_FOR_PICK\n\
    gl_FragColor = v_pickColor;\n\
#else\n\
    gl_FragColor = color;\n\
#endif\n\
}";
});