from pico2d import *

import game_framework as game_framework
import game_world
import play_mode
import server
import object_wall
import player


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
    global image
    global logo_start_time
    image = load_image('occupation selection.png')
    #game_world.add_object(b_g_image, 0)
    global boy
    boy=player.Player(800,400,170)
    game_world.add_object(boy,1)
    wall=object_wall.Wall(1100,685,1190,115)
    game_world.add_object(wall,1)
    #logo_start_time = get_time()

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    image.clip_draw(0,0,800,500,800,500,1600,1000)
    game_world.render()
    update_canvas()