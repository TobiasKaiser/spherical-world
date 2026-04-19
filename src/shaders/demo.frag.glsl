#version 300 es
precision highp float;

const float PI = 3.141592653589793;

in vec3 v_color;
in float spherical_dist;

out vec4 fragColor;

void main() {
    // Distance-based shading
    float brightness = 0.9 * (1.0 - spherical_dist / PI) + 0.1;
    fragColor.rgb = brightness * v_color.rgb;
    fragColor.a = 1.0;

    // Correct z ordering by spherical distance
    gl_FragDepth = spherical_dist / PI;
}
