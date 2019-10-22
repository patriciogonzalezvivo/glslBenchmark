#ifdef GL_ES
precision mediump float;
#endif

uniform sampler2D u_scene;

uniform vec2 u_resolution;
uniform float u_time;

varying vec4 v_position;
varying vec4 v_color;
varying vec3 v_normal;
varying vec2 v_texcoord;

void main(void) {
   vec4 color = vec4(1.0);
   vec2 st = gl_FragCoord.xy/u_resolution.xy;
   vec2 pixel = 1./u_resolution.xy;

#ifdef POSTPROCESSING
    color.rgb = vec3(1.0,0.0,0.5) * texture2D(u_scene, st).rgb;
#else
    color.rgb = v_color.rgb;
    float shade = dot(v_normal, normalize(vec3(0.0, 0.75, 0.75)));
    color.rgb *= smoothstep(-1.0, 1.0, shade);
#endif

    gl_FragColor = color;
}
