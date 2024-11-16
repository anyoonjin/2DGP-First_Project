from pico2d import *
from pico2d import close_canvas

#from main import update_world

#open_canvas(1600,1000)

class Background:
    def __init__(self):
        self.image = load_image('BackGround.png')
        self.x1=0
        self.y1=180.0

    def update(self,val:float = 0.0):
        if(self.y1>=20.0):
            self.y1+=val
        pass

    def draw(self):
        #self.image.draw(650,400)
        self.image.clip_draw(self.x1, int(self.y1),1300, 800, 800, 500, 1600, 1000)

    def check(self):
        print(f'~~~~~~~~~~~bg x1{self.x1},    bg y1{self.y1}')
        return self.x1,self.y1

'''
back = Background()

while(True):
    clear_canvas()
    back.draw()
    update_canvas()

close_canvas()

'''