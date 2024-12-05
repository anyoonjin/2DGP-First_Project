from pico2d import *
from pygame.examples.cursors import image
from pygame.gfxdraw import rectangle

import game_world
import game_framework
import server
import zombie


class Key:
    image=None
    # 상=0 / 우=1 / 좌=2 / 하=3
    def __init__(self,x=1050,y=2190):
        if Key.image==None:
            Key.image=load_image('key.png')
        self.x,self.y=x,y
        self.check_key=False
        self.key_draw=False

    def update(self, val: float = 0.0):
        # if (self.y1 > 20.0):
        self.y += val
        pass

    def draw(self):
        if self.key_draw:
            self.image.clip_draw(0, 0,100, 100,self.x, self.y)
            draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 15, self.y -20, self.x +15, self.y+10
        pass

    def handle_collision(self, group, other):
        if self.key_draw:
            if group == 'player:key' and not self.check_key :
                zombie.set_phase1()
                for i in zombie.P1_zom:
                    i.yes_draw=True

                game_world.remove_object(self)
                server.player.key_count += 1
                server.start_time = get_time()
                print(f'key=           {server.player.key_count}')
                if server.player.key_count == 3:
                    pass
                self.check_key=True

        pass


class key_open_text:
    def __init__(self,num =1):
        if num==4:
            key_open_text.image = load_image('escape_open.png')
        else:
            key_open_text.image = load_image(f'key_open{num}.png')
        self.count=0

    def update(self):
        self.count+=1
        if self.count==1700:
            game_world.remove_object(self)
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 500, 100,800, 750,1000,200)
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass

class Escape:
    def __init__(self,x=1050,y=2000):
        self.image=load_image('escape.png')
        self.x, self.y = x, y
        self.succes=False

    def draw(self):
        if self.succes:
            self.image.clip_draw(0, 0, 150, 150, self.x, self.y, 200, 180)
            draw_rectangle(*self.get_bb())
        pass

    def update(self, val: float = 0.0):
        # if (self.y1 > 20.0):
        self.y += val
        pass

    def get_bb(self):
        return self.x - 50, self.y -40, self.x +50, self.y+40
        pass

    def handle_collision(self, group, other):
        if self.succes:
            if group == 'player:escape': #게임오버로 넘어감
                print('탈출구 충돌체크')
                pass