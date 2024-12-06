from pico2d import *

import game_framework
import server
import occupation_select_mode
import game_world
import logo_mode

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_r:  # R 키 조건 추가
                server.mode='logo'
                # 원하는 동작 추가

def init():
    global image
    global logo_start_time
    global bgm
    bgm=load_music('re_bgm.mp3')
    bgm.set_volume(50)
    bgm.repeat_play()
    if server.mode=='fail':
        image = load_image('Fail.png')
    else:
        image=load_image('succes.png')
    logo_start_time = get_time()

def finish():
    global image
    del image
    game_world.clear()
    server.player = None
    server.walls = []


def update():
        if server.mode=='logo':
            game_framework.change_mode(logo_mode)


def draw():
    clear_canvas()
    image.clip_draw(0,0,800,600,800,500,1600,1000)

    update_canvas()