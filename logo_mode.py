from pico2d import load_image, get_time, clear_canvas, update_canvas, get_events

import game_framework as game_framework
import server
import occupation_select_mode
import game_world
import play_mode

def handle_events():
    event = get_events()


def init():
    global image
    global logo_start_time
    image = load_image('logo.png')
    logo_start_time = get_time()

def finish():
    global image
    del image
    #game_world.clear()


def update():
    global logo_start_time
    if get_time() - logo_start_time >= 2.0:
        logo_start_time = get_time()
        if server.mode=='play':
            game_framework.change_mode(play_mode)
        else:
            game_framework.change_mode(occupation_select_mode)


def draw():
    clear_canvas()
    image.clip_draw(0,0,800,600,800,500,1600,1000)
    update_canvas()