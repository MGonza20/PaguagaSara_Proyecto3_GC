vertex_shader ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 norms;
out vec3 pos;

void main()
{
    UVs = texcoords;
    norms = normals;
    pos = (modelMatrix * vec4(position, 1.0)).xyz;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
}
'''

fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform sampler2D tex;

void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));
    fragColor = texture(tex, UVs) * intensity;
}
'''

toon_fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform sampler2D tex;

void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));
    float newIntensity = 0;

    if (intensity < 0.2){
        newIntensity = 0.1;
    }
    else if (intensity < 0.5){
        newIntensity = 0.4;
    }
    else if (intensity < 0.8){
        newIntensity = 0.7;
    }
    else if (intensity <= 1){
        newIntensity = 1;
    }

    fragColor = texture(tex, UVs) * newIntensity;
}
'''

wave_vertex_shader ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float waveDepth;
uniform vec2 waveFrequency;
uniform float time;

out vec2 UVs;
out vec3 norms;
out vec3 pos;

void main()
{
    UVs = texcoords;
    norms = normals;
    pos = (modelMatrix * vec4(position, 1.0)).xyz;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    gl_Position.y += sin((gl_Position.z * waveFrequency.y)*1.5 + time) * sin((gl_Position.y * waveFrequency.y)/3 + time) * waveDepth; 
}
'''

explode_vertex_shader ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;
uniform float explode;

out vec2 UVs;
out vec3 norms;
out vec3 pos;

void main()
{
    UVs = texcoords;
    norms = normals;
    pos = (modelMatrix * vec4((position + normals*sin(explode)), 1.0)).xyz;

    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4((position + normals*sin(explode)), 1.0);
}
'''

explode_fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform sampler2D tex;

uniform float explodeColor;

void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));
    fragColor = texture(tex, UVs) * intensity;
    fragColor.z += explodeColor; 
}
'''


lightPower_fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform float force;

uniform vec3 pointLight;
uniform sampler2D tex;

void main()
{   
    vec2 uvss = UVs;
    float forcee = force;
    float xx = (floor(uvss.x*10)/10)*1.2 + forcee/2;
    float xy = (floor(uvss.y*10)/10)*1.2 + forcee/2;
    float y = 2.0;
    float mod1 = (xx-y)*floor(xx/y);
    float mod2 = (xy-y)*floor(xy/y);

    float intensity = dot(norms, normalize(pointLight - pos));
    intensity *= mod1;
    intensity *= mod2;

    fragColor = texture(tex, uvss) * intensity;
}
'''

displacement_fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform sampler2D tex;
uniform sampler2D dispTex;
uniform float change;


void main()
{
    vec4 disp = texture2D(dispTex, UVs);
    vec2 dispUVs = vec2(UVs.x, UVs.y + change*disp);
    float intensity = dot(norms, normalize(pointLight - pos));
    fragColor = texture(tex, dispUVs) * intensity;
}
'''