from pico2d import *
from pygame.gfxdraw import rectangle

import game_world
import game_framework
import server


class Key:
    image=None
    # 상=0 / 우=1 / 좌=2 / 하=3
    def __init__(self,x=1050,y=2190):
        if Key.image==None:
            Key.image=load_image('key.png')
            print("key.image is not loaded properly.")
        self.x,self.y=x,y

    def update(self, val: float = 0.0):
        # if (self.y1 > 20.0):
        self.y += val
        pass

    def draw(self):
        self.image.clip_draw(0, 0,100, 100,self.x, self.y)
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 15, self.y +20, self.x +15, self.y-10
        pass

    def handle_collision(self, group, other):
        if group == 'player:key':
            game_world.remove_object(self)

        pass

class key_open_text:
    def __init__(self,num =1):
        key_open_text.image = load_image(f'key_open{num}.png')
        self.count=0

    def update(self):
        self.count+=1
        if self.count==1800:
            game_world.remove_object(self)
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 500, 100,800, 750,1000,200)
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass