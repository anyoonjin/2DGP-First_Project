from pico2d import *
from pygame.examples.cursors import image

import game_world
import logo_mode
import game_framework
from player import Player
from background import Background, Cover
from Weapon import Arrow
import server
import object_wall
import key

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


first_key = False
second_key = False
third_key = False

def init():
    server.key1 = key.Key()
    server.key2 = key.Key(120, 2020)
    server.key3 = key.Key(500,2020)
    server.escape_open=key.Escape()

    server.b_g=Background()
    game_world.add_object(server.b_g,0)

    server.player=Player()
    game_world.add_object(server.player,1)

    game_world.add_collision_pair('player:wall',server.player,None)
    for wall in server.walls:
        game_world.add_collision_pair('player:wall',None,wall)

    server.cover=Cover()
    game_world.add_object(server.cover,2)

def finish():
    game_world.clear()
    pass

def update():
    global first_key, second_key, third_key

    if not first_key and 5.0 <= get_time() - server.start_time <= 5.9:
        game_world.add_object(server.key1, 1)
        game_world.add_collision_pair('player:key', server.player, None)
        game_world.add_collision_pair('player:key', None, server.key1)
        text_key = key.key_open_text()
        game_world.add_object(text_key, 1)
        first_key = True
    elif not second_key and server.player.key_count==1 :
        game_world.add_object(server.key2, 1)
        game_world.add_collision_pair('player:key', server.player, None)
        game_world.add_collision_pair('player:key', None, server.key2)
        text_key = key.key_open_text(2)
        game_world.add_object(text_key, 1)
        second_key = True
    elif not third_key and server.player.key_count==2 :
        game_world.add_object(server.key3, 1)
        game_world.add_collision_pair('player:key', server.player, None)
        game_world.add_collision_pair('player:key', None, server.key3)
        text_key = key.key_open_text(3)
        game_world.add_object(text_key, 1)
        third_key = True
    elif server.player.key_count == 3:
        game_world.add_object(server.escape_open, 1)
        game_world.add_collision_pair('player:escape', server.player, None)
        game_world.add_collision_pair('player:escape', None, server.escape_open)
        server.player.key_count = 4
        text_key = key.key_open_text(4)
        game_world.add_object(text_key, 1)

    game_world.update()
    game_world.handle_collisions()
    if server.player.success:
       finish()
       game_framework.change_mode(logo_mode)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()