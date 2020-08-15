#version 430

in vec3 in_vert;
in vec3 in_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 frag_in_color;
void main()
{
	gl_Position = projection * view * model * vec4(in_vert, 1.0);
	frag_in_color = in_color;
}