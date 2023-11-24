

vertex_shader = """
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    
    out vec2 UVs;
    out vec3 normal;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        UVs = texCoords;
        normal = (modelMatrix * vec4(normals, 0.0)).xyz;
    }
"""

fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        fragColor = texture(tex, UVs);
    }
"""

toonshader = """
#version 450 core

uniform sampler2D textureMap;

in vec2 texCoord;

out vec4 fragColor;

void main() {

    vec4 color = texture(textureMap, texCoord);
    
    color = floor(color * 5.0) / 5.0;
    
    fragColor = color;
}
"""

blueprint = """
#version 450 core

uniform sampler2D textureMap;

in vec2 texCoord;

out vec4 fragColor;  

void main() {

    vec4 color = texture(textureMap, texCoord);
    
    if(color.r > 0.99) {
        discard; 
    }
    
    color.gb = vec2(0.5, 0.5); 
    
    fragColor = color;
}
"""

bit = """  
#version 450 core

uniform sampler2D textureMap;
uniform float numColors;  

in vec2 texCoord;

out vec4 fragColor;

void main() {

    vec4 color = texture(textureMap, texCoord);
    
    color = floor(color * numColors) / numColors;
    
    fragColor = color;}
"""

hologram = """
// Hologram Shader

#version 450 core

uniform sampler2D textureMap;

in vec2 texCoord;

out vec4 fragColor;

void main() {

    vec2 uv = texCoord;
    
    uv.y += 0.02 * sin(uv.x * 100.0);
    uv.x += 0.02 * cos(uv.y * 100.0);
    
    vec4 color = texture(textureMap, uv);
 
    color.r = sin(color.r * 10.0) * 0.5 + 0.5;
    color.g = sin(color.g * 15.0) * 0.5 + 0.5; 
    color.b = sin(color.b * 20.0) * 0.5 + 0.5;

    fragColor = color;
}
"""

