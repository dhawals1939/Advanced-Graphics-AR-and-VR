#version 430

in vec2 in_vert;
in vec3 in_color;
uniform mat4 model;
uniform mat4 projection;

out vec3 out_color;
void main()
{
    gl_Position = projection * model * vec4(in_vert, .0, 1.0);
    out_color = in_color;
}