from pico2d import *
from pygame.examples.cursors import image

import game_world
import game_framework
from player import Player
from background import Background
from zombie import Wall
from Weapon import Arrow

def handle_events():
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def update_Wall(val):
    for wall in walls:
        wall.update(val)

def init():
    global  b_g, player,walls

    walls=[]

    b_g=Background()
    game_world.add_object(b_g,0)

    player=Player()
    game_world.add_object(player,1)

    wall=Wall(1100,685,1190,115)    #시작시 바로 오른쪽에 있는 벽
    game_world.add_object(wall, 1)
    walls.append(wall)

    wall=Wall(1100,1000,1190,800)    #윗문벽
    game_world.add_object(wall, 1)
    walls.append(wall)

    wall=Wall(980,1000,1100,830)    #캐비넷
    game_world.add_object(wall, 1)
    walls.append(wall)

    wall = Wall(500, 750, 680, 700)     #교탁
    game_world.add_object(wall, 1)
    walls.append(wall)

    wall = Wall(0, 1000, 1000, 905)  # 칠판벽
    game_world.add_object(wall, 1)
    walls.append(wall)

    wall = Wall(50, 830, 280, 750)  # 선생님책상
    game_world.add_object(wall, 1)
    walls.append(wall)

    game_world.add_collision_pair('player:wall',player,None)
    for wall in walls:
        game_world.add_collision_pair('player:wall',None,wall)



def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()