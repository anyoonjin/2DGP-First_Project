from pico2d import open_canvas, delay, close_canvas
import game_framework

import play_mode as start_mode

'''
def reset_world():

   pass

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

def update_world():
    game_world.update()
    pass

'''

open_canvas(1600,1000)
game_framework.run(start_mode)
close_canvas()
