#version 440


in vec3 v_color;
in float spherical_dist;

void main() {
    float z = gl_FragCoord.z / gl_FragCoord.w;
    
    // Regular color:
    //gl_FragColor.rgb = v_color;
    
    // Shade by z:
    gl_FragColor.rgb = 0.1*v_color+0.5/(vec3(z, z, z)+0.5);
    
    /*
    if(spherical_dist<3.141592653589793/2) {
        gl_FragColor.rgb = 0.1*v_color+vec3(0.5, 0.5, 0.5);
    } else {
        gl_FragColor.rgb = 0.1*v_color;
    }
    */

    float brightness;
    brightness = 0.9*(1-tanh(spherical_dist))+0.1;

    gl_FragColor.rgb = brightness*v_color.rgb;

    
    gl_FragColor.a = 1.0;
}