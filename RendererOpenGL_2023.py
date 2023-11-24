from math import radians, cos, sin

import glm

from pygame.locals  import *
from pygame.math import clamp

from gl import Renderer
from model import Model
from shaders import *
from obj import Obj
import pygame.mixer
import pygame.mouse


camera_distance = 10.0
camera_pitch = 0.0
camera_yaw = 0.0
max_camera_pitch = 89.0
min_camera_distance = 5.0
max_camera_distance = 20.0
mouse_sensitivity = 0.1
prev_mouse_pos = (0, 0)

def circular_movement(model, camera_position, deltaTime):
    global camera_yaw, camera_distance

    # Movimiento circular alrededor del modelo
    camera_yaw += deltaTime * 50
    model.position.x = camera_position.x + camera_distance * cos(radians(camera_yaw))
    model.position.z = camera_position.z + camera_distance * sin(radians(camera_yaw))


def zoom_in():
    global camera_distance, gl

    # Calculate new camera distance (move closer to the character)
    camera_distance = max(min_camera_distance, camera_distance - 1.0)
    update_camera_position()

def zoom_out():
    global camera_distance, gl

    # Calculate new camera distance (move farther from the character)
    camera_distance = min(max_camera_distance, camera_distance + 1.0)
    update_camera_position()

def update_camera_position():
    global camera_distance, camera_pitch, camera_yaw, current_model, gl

    # Update the camera position based on the current distance, pitch, and yaw
    camera_position = glm.vec3(
        current_model.position.x + camera_distance * cos(radians(camera_yaw)),
        current_model.position.y + camera_distance * sin(radians(camera_pitch)),
        current_model.position.z + camera_distance * sin(radians(camera_yaw))
    )
    gl.cameraPosition = camera_position


def vertical_movement(model, camera_position, deltaTime, up_limit, down_limit):
    global camera_pitch, camera_distance

    # Movimiento vertical centrado en el modelo
    camera_pitch += deltaTime * 50

    # Aplica límites al ángulo de inclinación
    camera_pitch = clamp(camera_pitch, down_limit, up_limit)

    # Calcula el desplazamiento vertical acumulado
    vertical_displacement = camera_distance * sin(radians(camera_pitch))

    # Actualiza la posición y del modelo
    model.position.y = vertical_displacement

    # Actualiza la posición de la cámara utilizando la posición del modelo
    gl.cameraPosition = model.position

    return vertical_displacement




def pa_arriba():
    global camera_distance, gl

    # Calculate new camera position
    camera_distance = max(min_camera_distance, camera_distance - 1.0)
    camera_position = glm.vec3(0.0, vertical_movement(current_model, gl.cameraPosition, 0, -30.0, 30.0), camera_distance)

    # Update the camera position in the renderer
    gl.cameraPosition = camera_position

def pa_abajo():
    global camera_distance, gl

    # Calculate new camera position
    camera_distance = min(max_camera_distance, camera_distance + 1.0)
    camera_position = glm.vec3(0.0, vertical_movement(current_model, gl.cameraPosition, 0, -30.0, 30.0), camera_distance)

    # Update the camera position in the renderer
    gl.cameraPosition = camera_position


width = 960
height = 540

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

gl = Renderer(screen)
gl.setShader(vertex_shader, fragment_shader)
song = pygame.mixer.Sound("space.mp3")
song.play(loops=-1)



obj = Obj("objs/robot.obj")
objData = obj.objData
model = Model(objData)
model.loadTexture("textures/robot.png")


obj2 = Obj("objs/Astronaut.obj")
objData2 = obj2.objData
model2 = Model(objData2)


obj3 = Obj("objs/Satellite.obj")
objData3 = obj3.objData
model3 = Model(objData3)


obj4 = Obj("objs/UFO_Empty.obj")
objData4 = obj4.objData
model4 = Model(objData4)


model.position.z = -200
model.position.y = -5
model.scale = glm.vec3(0.5, 0.5, 0.5)


model2.position.z = -6
model2.position.y = -2
model2.scale = glm.vec3(0.7, 0.7, 0.7)


model3.position.z = -6
model3.position.y = 0
model3.scale = glm.vec3(0.7, 0.7, 0.7)


model4.position.z = -6
model4.position.y = 0
model4.scale = glm.vec3(0.7, 0.7, 0.7)
model4.loadTexture("textures/UFO_rough.jpg")

current_model = model
gl.scene.append(current_model)
isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    gl.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if keys[K_d]:
                current_model.rotation.y += deltaTime * 50
            if keys[K_a]:
                current_model.rotation.y -= deltaTime * 50
            if keys[K_w]:
                current_model.rotation.x += deltaTime * 50
            if keys[K_s]:
                current_model.rotation.x -= deltaTime * 50
            if event.key == pygame.K_1:
                gl.scene.remove(current_model)
                model.loadTexture("textures/robot.png")
                current_model = model
                gl.scene.append(current_model)
            elif event.key == pygame.K_2:
                gl.scene.remove(current_model)
                model2.loadTexture("textures/Spacesuit_D.png")
                current_model = model2
                gl.scene.append(current_model)
            elif event.key == pygame.K_3:
                gl.scene.remove(current_model)
                model3.loadTexture("textures/Satellite.jpg")
                current_model = model3
                gl.scene.append(current_model)
            elif event.key == pygame.K_4:
                gl.scene.remove(current_model)
                current_model = model4
                gl.scene.append(current_model)
            elif event.key == pygame.K_UP:
                zoom_in()
            elif event.key == pygame.K_DOWN:
                zoom_out()
            elif event.key == pygame.K_RIGHT:
                pa_arriba()
            elif event.key == pygame.K_LEFT:
                pa_abajo()
            elif event.key == pygame.K_z:
                gl.setShader(vertex_shader, toonshader)
            elif event.key == pygame.K_x:
                gl.setShader(vertex_shader, blueprint)
            elif event.key == pygame.K_c:
                gl.setShader(vertex_shader, bit)
            elif event.key == pygame.K_v:
                gl.setShader(vertex_shader, hologram)

        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            dx, dy = x - prev_mouse_pos[0], y - prev_mouse_pos[1]
            normalized_x = (dx / width) * 2
            normalized_y = -1 * (dy / height) * 2  # Invertir el eje y para que sea consistente con OpenGL
            circular_movement(current_model, gl.cameraPosition, deltaTime)
            prev_mouse_pos = (x, y)
    gl.render()
    pygame.display.flip()

pygame.mixer.quit()
pygame.quit()