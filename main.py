from pico2d import open_canvas, delay, close_canvas, get_time
import game_framework

import logo_mode as start_mode
import server

open_canvas(1600,1000)
server.mode='logo'
game_framework.run(start_mode)
close_canvas()
