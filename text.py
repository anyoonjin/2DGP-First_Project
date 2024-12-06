from pico2d import *

import game_world
import game_framework
import server



class Text:
    def __init__(self,num =4):
        if num==4:
            self.image = load_image('choice_start.png')
        else:
            self.image = load_image(f'{num}.png')
        self.count=0

    def update(self):
        self.count+=1
        if self.count==500:
            game_world.remove_object(self)
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 800, 100,800, 750,1250,200)
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass