import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        self.scene = []
        self.clearColor = [1.0, 1.0, 1.0, 1.0]
        _, _, self.width, self.height = screen.get_rect()
        self.activeShader = None
        #View Matrix
        self.cameraPosition = glm.vec3(0.0, 0.0, 0.0)
        self.cameraRotation = glm.vec3(0.0, 0.0, 0.0)
        #Projection Matrix
        self.projectionMatrix = glm.perspective(
            glm.radians(60.0),  #FOV
            self.width / self.height,  #Aspect Ratio
            0.1,  #Near Plane
            1000.0  #Far Plane
        )
        self.elapsedTime = 0.0

        self.dirLight = glm.vec3(1, 0, 0)
        self.lightIntensity = 1.0

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

    def getViewMatrix(self):
        #Identity matrix
        identity = glm.mat4(1.0)

        #Calculo de matrices de rotación
        pitch = glm.rotate(identity, glm.radians(self.cameraRotation.x), glm.vec3(1.0, 0.0, 0.0))
        yaw = glm.rotate(identity, glm.radians(self.cameraRotation.y), glm.vec3(0.0, 1.0, 0.0))
        roll = glm.rotate(identity, glm.radians(self.cameraRotation.z), glm.vec3(0.0, 0.0, 1.0))
        rotateMatrix = pitch * yaw * roll

        #Calculo de matriz de traslación
        translateMatrix = glm.translate(identity, self.cameraRotation)

        #Calculo de matriz de transformación
        cameraMatrix = translateMatrix * rotateMatrix
        return glm.inverse(cameraMatrix)

    def setShader(self, vertex_shader=None, fragment_shader=None):

        #Si no se especifica un shader, se desactiva el shader
        if vertex_shader is None and fragment_shader is None:
            self.activeShader = None
        else:
            self.activeShader = compileProgram(
                compileShader(vertex_shader, GL_VERTEX_SHADER),
                compileShader(fragment_shader, GL_FRAGMENT_SHADER)
            )
    def draw_background(self, background_image, background_rect):
        glUseProgram(0)  # Desactivar el uso del shader para el fondo
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(-1, -1)
        glTexCoord2f(1, 1)
        glVertex2f(1, -1)
        glTexCoord2f(1, 0)
        glVertex2f(1, 1)
        glTexCoord2f(0, 0)
        glVertex2f(-1, 1)
        glEnd()

    def render(self):
        glClearColor(*self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.activeShader is not None:
            glUseProgram(self.activeShader)
            #Envia la matriz de transformación a la tarjeta de video
            glUniformMatrix4fv(
                glGetUniformLocation(self.activeShader, "viewMatrix"),
                1,
                GL_FALSE,
                glm.value_ptr(self.getViewMatrix())
            )
            glUniformMatrix4fv(
                glGetUniformLocation(self.activeShader, "projectionMatrix"),
                1,
                GL_FALSE,
                glm.value_ptr(self.projectionMatrix)
            )
            glUniform1f(
                glGetUniformLocation(self.activeShader, "time"),
                self.elapsedTime
            )
            glUniform3fv(
                glGetUniformLocation(self.activeShader, "dirLight"),
                1,
                glm.value_ptr(self.dirLight)
            )
            glUniform1f(
                glGetUniformLocation(self.activeShader, "lightIntensity"),
                self.lightIntensity
            )

        for obj in self.scene:

            #Envia la matriz de transformación a la tarjeta de video
            if self.activeShader is not None:
                glUniformMatrix4fv(
                    glGetUniformLocation(self.activeShader, "modelMatrix"),
                    1,
                    GL_FALSE,
                    glm.value_ptr(obj.getModelMatrix())
                )
            obj.render()

