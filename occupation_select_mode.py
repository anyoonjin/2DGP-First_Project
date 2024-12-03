from pico2d import *
from pygame import get_error

import game_framework as game_framework
import game_world
import play_mode
import choice_mode_class
import player
import text

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global image,arrow_image
    global logo_start_time
    image = load_image('occupation selection.png')
    arrow_image=load_image('아처.png')
    #game_world.add_object(b_g_image, 0)
    global boy
    boy=player.Player(800,400,170)
    game_world.add_object(boy,1)

    walls=[]
    wall=object_wall.Wall(0,1000,130,0)
    game_world.add_object(wall,1)
    walls.append(wall)
    wall = object_wall.Wall(1460, 1000, 1600, 0)
    game_world.add_object(wall, 1)
    walls.append(wall)
    wall = object_wall.Wall(740, 620, 825, 500)
    game_world.add_object(wall, 1)
    walls.append(wall)
    wall = object_wall.Wall(0, 1000, 1600, 750)
    game_world.add_object(wall, 1)
    walls.append(wall)
    wall = object_wall.Wall(1300, 1000, 1600, 690)
    game_world.add_object(wall, 1)
    walls.append(wall)

    game_world.add_collision_pair('player:wall', boy, None)
    for wall in walls:
        game_world.add_collision_pair('player:wall', None, wall)

    ch_text=text.Text()
    game_world.add_object(ch_text,2)
    logo_start_time = get_time()

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    global logo_start_time
    if get_time() - logo_start_time >= 5.0 and not boy.choice:
        ch_text = text.Text()
        game_world.add_object(ch_text, 2)
        logo_start_time=get_time()



def draw():
    clear_canvas()
    image.clip_draw(0,0,800,500,800,500,1600,1000)
    arrow_image.clip_draw(0, 0, 1025, 1031, 180, 780, 90, 90)
    game_world.render()
    update_canvas()