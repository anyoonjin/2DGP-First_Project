from pico2d import *
import game_world
import server

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


server.walls=[]

wall=Wall(1100,685,1190,115)    #시작시 바로 오른쪽에 있는 벽
game_world.add_object(wall, 1)
server.walls.append(wall)
wall=Wall(1100,1680,1190,800)    #윗문벽
game_world.add_object(wall, 1)
server.walls.append(wall)
wall=Wall(980,1000,1100,830)    #캐비넷
game_world.add_object(wall, 1)
server.walls.append(wall)
wall = Wall(500, 750, 680, 700)     #교탁
game_world.add_object(wall, 1)
server.walls.append(wall)
wall = Wall(0, 1230, 1100, 905)  # 칠판벽
game_world.add_object(wall, 1)
server.walls.append(wall)
wall = Wall(50, 830, 280, 750)  # 선생님책상
game_world.add_object(wall, 1)
server.walls.append(wall)