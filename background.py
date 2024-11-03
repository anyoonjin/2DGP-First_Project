from pico2d import *
from pico2d import close_canvas

#from main import update_world

#open_canvas(1600,1000)

class Background:
    def __init__(self):
        self.image = load_image('BackGround.png')

    def update(self):
        pass

    def draw(self):
        #self.image.draw(650,400)
        self.image.clip_draw(0, 180,1300, 800, 800, 500, 1600, 1000)

'''
back = Background()

while(True):
    clear_canvas()
    back.draw()
    update_canvas()

close_canvas()

'''