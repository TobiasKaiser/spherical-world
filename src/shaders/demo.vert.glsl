#version 300 es
precision highp float;

const float PI = 3.141592653589793;

in vec4 a_position;
in vec3 a_color;

out vec3 v_color;
out float spherical_dist;

uniform vec4 view_s;
uniform vec4 view_t;
uniform mat4 proj;

// 4D spherical -> 3D stereographic projection through 1.
vec4 stereographic_proj_4to3(vec4 v) {
    float divisor = v.w + 1.0;
    return vec4(v.xyz / divisor, 1.0);
}

// Quaternion multiplication
vec4 qmul(vec4 a, vec4 b) {
    vec4 ret;
    ret.w = a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z;
    ret.x = a.w*b.x + a.x*b.w + a.y*b.z - a.z*b.y;
    ret.y = a.w*b.y - a.x*b.z + a.y*b.w + a.z*b.x;
    ret.z = a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w;
    return ret;
}

void main() {
    // Apply view transformation: view_s * position * view_t
    vec4 pos4_modelview = qmul(qmul(view_s, a_position), view_t);

    spherical_dist = acos(pos4_modelview.w);

    vec4 pos3 = stereographic_proj_4to3(pos4_modelview);

    gl_Position = proj * pos3;

    v_color = a_color;
}
