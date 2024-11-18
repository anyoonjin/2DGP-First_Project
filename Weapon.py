from pico2d import *
import game_world
import game_framework

class Arrow:
    image=None
    # 상=0 / 우=1 / 좌=2 / 하=3
    def __init__(self,x=400,y=300 ,dir=0):
        if(Arrow.image==None):
            Arrow.image=load_image('arrow.png')
        self.x,self.y,self.dir=x,y,dir


    def update(self):
        if self.dir == 0:
            self.y += 3 * 100 * game_framework.frame_time
        elif self.dir == 1:
            self.x +=3 * 100 * game_framework.frame_time
        elif self.dir == 2:
            self.x -=3 * 100 * game_framework.frame_time
        elif self.dir == 3:
            self.y -= 3 * 100 * game_framework.frame_time

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
        pass

    def draw(self):
        if self.dir==0:
            self.clip_composite_draw(0, 0, 200, 200, 90, 'h', self.x, self.y, 200, 200)
        elif self.dir ==1:
            self.clip_composite_draw(0, 0, 200, 200, 0, 'h', self.x, self.y, 200, 200)
        elif self.dir ==2:
            self.clip_composite_draw(0, 0, 200, 200, 180, 'h', self.x, self.y, 200, 200)
        elif self.dir ==3:
            self.clip_composite_draw(0, 0, 200, 200, 270, 'h', self.x, self.y, 200, 200)
        pass

    def get_bb(self):
        pass

    def attack(self):
        pass

    def handle_collision(self, group, other):

        pass

class Bomb:
    image = None

    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def get_bb(self):
        pass

    def attack(self):
        pass

    def handle_collision(self, group, other):
        pass