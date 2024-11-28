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
#아래교실
wall=Wall(1100,685,1190,115)    #시작시 바로 오른쪽에 있는 벽
game_world.add_object(wall, 1)
server.walls.append(wall)
wall=Wall(1100,-20,1190,-300)    #맨 밑에 있는 벽
game_world.add_object(wall, 1)
server.walls.append(wall)
wall=Wall(0,-150,1035,-300)    #맨 밑 사물함 모임
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

#학생들 책상
x1,x2=215,345
for i in range(4):
    wall = Wall(x1, 590, x2, 560)
    game_world.add_object(wall, 1)
    server.walls.append(wall)
    x1 = x2 + 75
    x2 = x1 + 130

y1,y2=490,420
for j in range(4):
    x1, x2 = 215, 345
    for i in range(4):
        wall = Wall(x1, y1, x2, y2)
        game_world.add_object(wall, 1)
        server.walls.append(wall)
        x1 = x2 + 75
        x2 = x1 + 130
    y1=y2-70
    y2=y1-70

x1, x2 = 215, 345
for i in range(4):
    wall = Wall(x1, -65, x2, -80)
    game_world.add_object(wall, 1)
    server.walls.append(wall)
    x1 = x2 + 75
    x2 = x1 + 130


#윗교실
wall=Wall(1100,3000,1190,1865)    #벽
game_world.add_object(wall, 1)
server.walls.append(wall)

wall=Wall(100,3000,1190,2250)    #거울
game_world.add_object(wall, 1)
server.walls.append(wall)

wall=Wall(970,3000,1190,2230)    #캐비넷
game_world.add_object(wall, 1)
server.walls.append(wall)

wall=Wall(970,2155,1190,2110)    #라디오
game_world.add_object(wall, 1)
server.walls.append(wall)


wall=Wall(100,3000,230,2230)    #에어컨
game_world.add_object(wall, 1)
server.walls.append(wall)


wall=Wall(80,2800,140,2140)    #왼쪽 책상
game_world.add_object(wall, 1)
server.walls.append(wall)

wall=Wall(80,2140,150,2050)    #왼쪽 스피커
game_world.add_object(wall, 1)
server.walls.append(wall)

wall=Wall(80,2100,215,2058)    #왼쪽 미니 스피커
game_world.add_object(wall, 1)
server.walls.append(wall)

wall=Wall(80,1970,145,1720)    #왼쪽 사물함
game_world.add_object(wall, 1)
server.walls.append(wall)

wall=Wall(0,1980,90,1000)    #왼쪽 벽
game_world.add_object(wall, 1)
server.walls.append(wall)

#학생들 책상
x1,x2=235,358
for i in range(4):
    wall = Wall(x1, 1480, x2, 1200)
    game_world.add_object(wall, 1)
    server.walls.append(wall)
    x1 = x2 + 75
    x2 = x1 + 128