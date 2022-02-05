#version 440

in vec4 a_position;
in vec3 a_color;

out vec3 v_color;

uniform vec4 view_s;
uniform vec4 view_t;

uniform mat4 proj;

out float spherical_dist;

// 4D spherical -> 3D space steregraphic projection through 1.
vec4 stereographic_proj_4to3(vec4 v) {
    vec4 ret;

    float divisor;
    divisor = (v.w + 1);
    ret.xyz = v.xyz/divisor;
    ret.w = 1.0;

    return ret;
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
    // Step 1: translate & rotate
    vec4 pos4_modelview;

    pos4_modelview=qmul(qmul(view_s, a_position.yzwx), view_t);

    spherical_dist = acos(pos4_modelview.w);


    vec4 pos3;

    pos3 = stereographic_proj_4to3(pos4_modelview);
    
    
    vec4 my_pos;

    my_pos = proj * pos3;
    //my_pos.z = 0.0;

    gl_Position = my_pos;

    v_color = a_color;
}