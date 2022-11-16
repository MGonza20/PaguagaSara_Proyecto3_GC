from math import radians, sin, cos
import pygame
from pygame.locals import *
from pygame import mixer

from shaders import *
from gl import Renderer, Model

width = 960
height = 540

deltaTime = 0.0

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(vertex_shader, fragment_shader)
rend.target.z = -5

option = 1
isRunning = True
clicking = False
clicking_r = False

mixer.music.load('lift.wav')
mixer.music.play(-1)

def renderModel(option):
    if option == 1:
        face = Model("models\SurgeonFish\SurgeonFish.obj", "models\SurgeonFish\SurgeonFish.bmp", "dispTex.bmp")
        face.scale.x = 2
        face.scale.y = 2
        face.scale.z = 2

    if option == 2:
        face = Model("models\MandarinFish\MandarinFish.obj", "models\MandarinFish\MandarinFish.bmp", "dispTex.bmp")
        face.scale.x = 0.5
        face.scale.y = 0.5
        face.scale.z = 0.5

    if option == 3:
        face = Model("models\Scallop\scallop.obj", "models\Scallop\scallop.bmp", "dispTex.bmp")
        face.scale.x = 0.5
        face.scale.y = 0.5
        face.scale.z = 0.5

    if option == 4:
        face = Model("models\Seahorse\Seahorse.obj", "models\Seahorse\Seahorse.bmp", "dispTex.bmp")
        face.scale.x = 0.5/10
        face.scale.y = 0.5/10
        face.scale.z = 0.5/10

    if option == 5:
        face = Model("models\Starfish\Starfish.obj", "models\Starfish\Starfish.bmp", "dispTex.bmp")
        face.scale.x = 2.5
        face.scale.y = 2.5
        face.scale.z = 2.5

    face.position.z -= 5

    return face

face = renderModel(option)
rend.scene.append(face)


while isRunning: 
    
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if clicking:
        if mouse_x > width/2:
            rend.angle -= 30 * deltaTime
        elif mouse_x <= width/2:
            rend.angle += 30 * deltaTime

    if clicking_r:
        if mouse_y > height/2:
            if rend.camPosition.y < 1.5:
                rend.camPosition.y += 3.5*deltaTime/2
        elif mouse_y <= height/2:
            if rend.camPosition.y > -1.5:
                rend.camPosition.y -= 3.5*deltaTime/2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_z:
                rend.filledMode()
            elif event.key == pygame.K_x:
                rend.wireframeMode()
            
            elif event.key == pygame.K_RETURN:
                if option > 4:
                    option += 1                    
                    option = ((option%5))
                    rend.scene.clear()
                    rend.scene.append(renderModel(option))
                else:
                    option +=1
                    rend.scene.clear()
                    rend.scene.append(renderModel(option))

            elif event.key == pygame.K_1:
                rend.setShaders(vertex_shader, fragment_shader)
            elif event.key == pygame.K_2:
                rend.setShaders(vertex_shader, toon_fragment_shader)
            elif event.key == pygame.K_3:
                rend.setShaders(wave_vertex_shader, fragment_shader)
            elif event.key == pygame.K_4:
                rend.setShaders(explode_vertex_shader, explode_fragment_shader)
            elif event.key == pygame.K_5:
                rend.setShaders(explode_vertex_shader, lightPower_fragment_shader)
            elif event.key == pygame.K_6:
                rend.setShaders(vertex_shader, displacement_fragment_shader)
            

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True   
            if event.button == 3:
                clicking_r = True   
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False   
            if event.button == 3:
                clicking_r = False

        elif event.type == pygame.MOUSEWHEEL:
            if(event.y < 0):
                if rend.camDistance > 2:
                    rend.camDistance -= 2 * deltaTime
            else:
                if rend.camDistance < 7:
                    rend.camDistance += 2 * deltaTime    
            

    if True:
        if keys[K_q]:
            if rend.camDistance > 2:
                rend.camDistance -= 2 * deltaTime
        elif keys[K_e]:
            if rend.camDistance < 7:
                rend.camDistance += 2 * deltaTime
        
        if keys[K_p]:
            if rend.explode <= 0.35:
                rend.explode += 1.0 * deltaTime
                rend.explode_color += 1.0 * deltaTime
        elif keys[K_o]:
            if rend.explode >= 0.0:
                rend.explode -= 1.0 * deltaTime
                rend.explode_color -= 1.0 * deltaTime

        if keys[K_f]:
            if rend.force <= 7.6:
                rend.force += 1.0 * deltaTime
        elif keys[K_c]:
            if rend.force >= 0.0:
                rend.force -= 1.0 * deltaTime
    
        if keys[K_a]:
            rend.angle -= 30 * deltaTime
        elif keys[K_d]:
            rend.angle += 30 * deltaTime

        if keys[K_w]:
            if rend.camPosition.y < 1.5:
                rend.camPosition.y += 5 * deltaTime*2
        elif keys[K_s]:
            if rend.camPosition.y > -1.5:
                rend.camPosition.y -= 5 * deltaTime*2

        rend.target.y = rend.camPosition.y 
        xDistance = sin(radians(rend.angle))
        zDistance = cos(radians(rend.angle))
        rend.camPosition.x = xDistance * rend.camDistance + rend.target.x 
        rend.camPosition.z = zDistance * rend.camDistance + rend.target.z 


    
    if keys[K_LEFT]:
        rend.pointLight.x -= 10 * deltaTime
    elif keys[K_RIGHT]:
        rend.pointLight.x += 10 * deltaTime
    elif keys[K_UP]:
        rend.pointLight.y += 10 * deltaTime
    elif keys[K_DOWN]:
        rend.pointLight.y -= 10 * deltaTime

    deltaTime = clock.tick(60) / 1000
    rend.time += deltaTime


    rend.update()
    rend.render("underwater-background.png")
    pygame.display.flip()

pygame.quit()