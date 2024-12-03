from pico2d import *
import game_world
import game_framework

class Arrow:
    image=None
    # 상=0 / 우=1 / 좌=2 / 하=3
    def __init__(self,x=400,y=300 ,dir=0):
        if Arrow.image==None:
            Arrow.image=load_image('arrow.png')
            #print("Arrow.image is not loaded properly.")
        self.x,self.y,self.dir=x,y,dir
        game_world.add_collision_pair('arrow:job_desk', None, self)


    def update(self):
        if self.dir == 0:
            self.y += 8 * 100 * game_framework.frame_time
        elif self.dir == 1:
            self.x += 8 * 100 * game_framework.frame_time
        elif self.dir == 2:
            self.x -= 8 * 100 * game_framework.frame_time
        elif self.dir == 3:
            self.y -= 8 * 100 * game_framework.frame_time

        if self.x < 10 or self.x > 1600 - 10:
            game_world.remove_object(self)
        pass

    def draw(self):
        #print(f"Drawing arrow at x={self.x}, y={self.y}, dir={self.dir}")
        if self.dir==0:
            self.image.clip_composite_draw(0, 0, 200, 200,4.7, 'h', self.x-10, self.y, 100, 100)
        elif self.dir ==1:
            self.image.clip_composite_draw(0, 0, 200, 200, 3.1, 'h', self.x, self.y, 100, 100)
        elif self.dir ==2:
            self.image.clip_composite_draw(0, 0, 200, 200, 0, 'h', self.x, self.y, 100, 100)
        elif self.dir ==3:
            self.image.clip_composite_draw(0, 0, 200, 200, 1.6, 'h', self.x-10, self.y, 100, 100)
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        if self.dir == 0:
            return self.x - 15, self.y , self.x -5, self.y + 35
        elif self.dir == 1:
            return self.x , self.y - 6, self.x+35, self.y+3
        elif self.dir == 2:
            return self.x -38, self.y -3, self.x, self.y +6
        elif self.dir == 3:
            return self.x - 15, self.y - 35, self.x -5, self.y
        pass

    def attack(self):
        pass

    def handle_collision(self, group, other):
        if group =='arrow:job_desk':
            print("직업선택완료")

        pass
