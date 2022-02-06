#version 440

float PI = 3.141592653589793;

in vec3 v_color;
in float spherical_dist;

void main() {
    
    bool distance_shading = true;

    if(distance_shading) {
        float brightness;
        brightness = 0.9*(1-spherical_dist/PI)+0.1;
        gl_FragColor.rgb = brightness*v_color.rgb;
    } else {
        // No shading:
        gl_FragColor.rgb = v_color;
    }
    
    // Correct z ordering by spherical distance:
    gl_FragDepth = spherical_dist/PI; 
    // Rendering currently stops at antipodal point.
    
    gl_FragColor.a = 1.0;
    
}