from pico2d import open_canvas, delay, close_canvas, get_time
import game_framework

import play_mode as start_mode
import server
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
server.mode='play'
close_canvas()
