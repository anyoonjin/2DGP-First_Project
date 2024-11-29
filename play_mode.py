from pico2d import *
from pygame.examples.cursors import image

import game_world
import game_framework
from player import Player
from background import Background
from Weapon import Arrow
import server
import object_wall

server.start_time=get_time()


def handle_events():
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.player.handle_event(event)

def update_Wall(val):
    for wall in server.walls:
        wall.update(val)

def init():

    server.b_g=Background()
    game_world.add_object(server.b_g,0)

    server.player=Player()
    game_world.add_object(server.player,1)

    game_world.add_collision_pair('player:wall',server.player,None)
    for wall in server.walls:
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