import glm
import pygame
from OpenGL.GL import *

from numpy import array, float32

class Model(object):
    def __init__(self, data):
        # **Inicializa el búfer de vértices**
        self.vertexBuffer = array(data, dtype=float32)

        # **Genera búferes para objetos de matriz de vértices (VAO) y búferes de vértices (VBO)**
        self.VBO = glGenBuffers(1)
        self.VAO = glGenVertexArrays(1)

        # **Establece la posición, rotación y escala inicial**
        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotation = glm.vec3(0.0, 0.0, 0.0)
        self.scale = glm.vec3(1.0, 1.0, 1.0)

        # **Inicializa las variables de textura**
        self.textureSurface = None
        self.textureData = None
        self.textureBuffer = None

    def loadTexture(self, path):
        # **Carga la imagen de textura usando pygame**
        self.textureSurface = pygame.image.load(path)

        # **Convierte los datos de la imagen a un formato compatible con OpenGL**
        self.textureData = pygame.image.tostring(self.textureSurface, "RGB", True)

        # **Genera un búfer para la textura**
        self.textureBuffer = glGenTextures(1)

    def getModelMatrix(self):
        # **Inicializa una matriz identidad**
        identity = glm.mat4(1.0)

        # **Aplica matrices de rotación para inclinación, guiñada y cabeceo**
        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1.0, 0.0, 0.0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0.0, 1.0, 0.0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0.0, 0.0, 1.0))

        # **Combina las matrices de rotación**
        rotateMatrix = pitch * yaw * roll

        # **Crea matrices de traslación y escala**
        translateMatrix = glm.translate(identity, self.position)
        scaleMatrix = glm.scale(identity, self.scale)

        # **Combina las matrices de transformación**
        return translateMatrix * rotateMatrix * scaleMatrix

    def render(self):
        # **Vincula el búfer de vértices al VAO**
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # **Especifica la disposición de los atributos de vértice**
        glBufferData(GL_ARRAY_BUFFER,
                     self.vertexBuffer.nbytes,
                     self.vertexBuffer,
                     GL_STATIC_DRAW)

        # **Establece los punteros de atributos de vértice para la posición y las coordenadas de textura**
        glVertexAttribPointer(0,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

        # **Activa y vincula la textura**
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureBuffer)

        # **Carga los datos de la textura y genera mipmaps**
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            self.textureSurface.get_width(),
            self.textureSurface.get_height(),
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            self.textureData
        )

        # **Genera mipmaps**
        glGenerateTextureMipmap(self.textureBuffer)


        # **Dibuja**
        glVertexAttribPointer(2,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(4 * 5))

        glEnableVertexAttribArray(2)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertexBuffer) // 8)
