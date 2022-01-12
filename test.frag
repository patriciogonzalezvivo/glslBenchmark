
#ifdef GL_ES
precision mediump float;
#endif

uniform vec2    u_resolution;
uniform vec2    u_mouse;
uniform float   u_time;

void main(void) {
    vec3 color = vec3(1.0);
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.x *= u_resolution.x/u_resolution.y;
    
    color = vec3(st.x,st.y,abs(sin(u_time)));
    
    gl_FragColor = vec4(color, 1.0);
}
