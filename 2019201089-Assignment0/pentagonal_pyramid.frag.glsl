#version 430

in vec3 frag_in_color;
out vec4 out_color;
// texture samplers

void main()
{
	// linearly interpolate between both textures (80% container, 20% awesomeface)
	out_color = vec4(frag_in_color, 1.);
}