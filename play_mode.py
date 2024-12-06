from pico2d import *

import game_world
import logo_mode
import game_framework
from player import Player
from background import Background, Cover
import server
import object_wall
import key
import zombie
import random
import result

def key_point_set():
    key_point_l=[(1050,2190),(200,2200),(400,1300),(1450,2400),(1080,-150),(120,860),(120,200),(120,2020)]
    k1 = random.choice(key_point_l)
    server.key1 = key.Key(k1[0], k1[1])  # 튜플에서 x, y 값을 직접 사용
    key_point_l.remove(k1)  # 뽑은 페어는 제거

    k2 = random.choice(key_point_l)
    server.key2 = key.Key(k2[0], k2[1])  # 튜플에서 x, y 값을 직접 사용
    key_point_l.remove(k2)  # 뽑은 페어는 제거

    k3 = random.choice(key_point_l)
    server.key3 = key.Key(k3[0], k3[1])  # 튜플에서 x, y 값을 직접 사용
    key_point_l.remove(k3)  # 뽑은 페어는 제거

    e1=random.choice(key_point_l)
    server.escape_open = key.Escape(e1[0], e1[1])  # 튜플에서 x, y 값을 직접 사용
    key_point_l.remove(e1)
    pass

def handle_events():
    events=get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.player.handle_event(event)

def init():
    global bgm
    bgm=load_music('bgm.mp3')
    bgm.set_volume(50)
    bgm.repeat_play()
    global first_key, second_key, third_key
    first_key = False
    second_key = False
    third_key = False
    server.start_time = get_time()
    if server.mode =='play':
        key_point_set()
        game_world.add_object(server.escape_open, 1)
        for i in range(1, 4):  # key1, key2, key3에 접근하려는 의도라면 범위는 1부터 4
            game_world.add_object(getattr(server, f'key{i}'), 1)

        zom=zombie.Zombie(300,800,True)
        game_world.add_object(zom,2)
        zom = zombie.Zombie(500, -50, True)
        game_world.add_object(zom, 2)
        zom = zombie.Zombie(1200, 1100, True)
        game_world.add_object(zom, 2)
        zom = zombie.Zombie(200, 2300, True)
        game_world.add_object(zom, 2)

        server.b_g=Background()
        game_world.add_object(server.b_g,0)

        server.player=Player()
        game_world.add_object(server.player,1)

        object_wall.wall_make()
        game_world.add_collision_pair('player:wall',server.player,None)
        for wall in server.walls:
            game_world.add_collision_pair('player:wall',None,wall)

        game_world.add_collision_pair('player:zombie', server.player, None)

        server.cover=Cover()
        game_world.add_object(server.cover,3)

def finish():
    game_world.clear()
    game_world.collision_pairs={}
    server.player = None
    server.b_g = None
    server.walls = []
    server.start_time = None
    server.key1 = None
    server.key2 = None
    server.key3 = None
    server.cover = None
    server.escape_open = None
    pass

def update():
    global first_key, second_key, third_key

    if not first_key and 5.0 <= get_time() - server.start_time <= 5.9:
        server.key1.key_draw=True
        game_world.add_collision_pair('player:key', server.player, None)
        game_world.add_collision_pair('player:key', None, server.key1)
        text_key = key.key_open_text()
        game_world.add_object(text_key, 3)
        first_key = True
    elif not second_key and server.player.key_count==1 :
        server.key2.key_draw = True
        game_world.add_collision_pair('player:key', server.player, None)
        game_world.add_collision_pair('player:key', None, server.key2)
        text_key = key.key_open_text(2)
        game_world.add_object(text_key, 3)
        second_key = True

        #zombie.set_phase2()
    elif not third_key and server.player.key_count==2 :
        server.key3.key_draw = True
        game_world.add_collision_pair('player:key', server.player, None)
        game_world.add_collision_pair('player:key', None, server.key3)
        text_key = key.key_open_text(3)
        game_world.add_object(text_key, 3)
        third_key = True
    elif server.player.key_count == 3:
        server.escape_open.succes = True
        game_world.add_collision_pair('player:escape', server.player, None)
        game_world.add_collision_pair('player:escape', None, server.escape_open)
        server.player.key_count = 4
        text_key = key.key_open_text(4)
        game_world.add_object(text_key, 3)

    game_world.update()
    game_world.handle_collisions()
    if server.player.success or server.mode=='fail':
        delay(3)
        finish()
        game_framework.change_mode(result)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()