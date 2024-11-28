from pico2d import *
import game_world
import game_framework

class Zombie:

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


class Wall:
    def __init__(self,x1=100,y1=100.0,x2=200,y2=200.0):
        self.x1,self.x2,self.y1,self.y2=x1,x2,y1,y2
        pass

    def update(self, val: float = 0.0):
        #if (self.y1 > 20.0):
        self.y1 += val
        self.y2 += val
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x1, self.y2, self.x2, self.y1
        pass

    def attack(self):
        pass

    def handle_collision(self, group, other):
        if group =='player:wall':
            print('------------------------------------------------------player:wall')
            pass
        pass