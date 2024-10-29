from pico2d import*

import background
import player
import game_world

def reset_world():

   pass

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

def update_world():
    game_world.update()
    pass

open_canvas(1300,1000)
reset_world()
