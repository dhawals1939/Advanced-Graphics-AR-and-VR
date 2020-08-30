#version 430

in vec2 out_tex;
in vec3 out_color;

out vec4 frag_color;

uniform sampler2D tex;
void main() {
    frag_color = texture(tex, out_tex)*vec4(out_color, 1.0);
}