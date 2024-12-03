from pico2d import open_canvas, delay, close_canvas, get_time
import game_framework

import logo_mode as start_mode
import server

open_canvas(1600,1000)
game_framework.run(start_mode)
server.mode='logo'
close_canvas()
