
from pico2d import *

import game_world
from state_machine import *
import game_framework
from Weapon import Arrow
import background
import zombie
import server
import key
import occupation_select_mode
import os

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.8
ACTION_PER_TIME = 2.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

#상하 키 누르다가 좌우 키 동시에 누르면 눌린키와 반대방향으로 이동함
# 상=0 / 우=1 / 좌=2 / 하=3
class Idle:
    @staticmethod
    def enter(player, e):
        if start_event(e):
            player.action = 3
            player.face_dir = 3
        elif right_down(e) or left_up(e) or up_up(e) or down_up(e):
            player.action = 2
            player.face_dir = 2
        elif left_down(e) or right_up(e) or up_up(e) or down_up(e):
            player.action = 1
            player.face_dir = 1
        elif down_down(e) or up_up(e) or right_up(e) or left_up(e):  # 아래로 RUN
            player.face_dir, player.action = 3, 3
        elif up_down(e) or down_up(e) or right_up(e) or left_up(e):  # 위로 RUN
            player.face_dir, player.action = 0, 0


        player.frame = 0
        player.wait_time = get_time()
        pass

    @staticmethod
    def exit(player, e):
        print(f"뭔놈의 event: {e}")
        print(f"x={player.x}  y={player.y}")
        if space_down(e):
            player.attack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame )* 75,int(player.action)* 75, 75, 75, int(player.x),int( player.y),player.size,player.size)

# 상=0 / 우=1 / 좌=2 / 하=3
class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e) or up_up(e) or down_up(e):   # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e) or up_up(e) or down_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = 2, 2, 2
        elif down_down(e) or up_up(e) or right_up(e) or left_up(e):    #아래로 RUN
            player.dir, player.face_dir, player.action = 3, 3, 3
        elif up_down(e) or down_up(e) or right_up(e) or left_up(e):    #위로 RUN
            player.dir, player.face_dir, player.action = 0, 0, 0

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.attack()

    # 상=0 / 우=1 / 좌=2 / 하=3
    @staticmethod
    def do(player):
        player.frame = 3+(player.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) %3
        if player.dir==0:
            if player.y<=900 :
                player.y += 1* RUN_SPEED_PPS * game_framework.frame_time
        elif player.dir==1:
            if player.x <=1520:
                player.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
        elif player.dir==2:
            if player.x>=105:
                player.x -= 1 * RUN_SPEED_PPS * game_framework.frame_time
        elif player.dir==3:
            if player.y>=80 :
                player.y -= 1 * RUN_SPEED_PPS * game_framework.frame_time

                #print(f'~~~~~~~~~~ BG Y:{player.b_g.y1}')

        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 75, int(player.action)* 75, 75, 75, int(player.x), int(player.y),player.size,player.size)


# 상=0 / 우=1 / 좌=2 / 하=3
class Player:
    def __init__(self,x=800,y=500, size=120):
        self.image=load_image('player2.png')
        self.x,self.y=x,y
        self.face_dir=3
        self.dir=3
        self.choice=False
        self.key_count=0
        self.frame=0
        self.action=0
        self.size=size
        self.success=False
        self.state_machine=StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, up_down:Run, down_down:Run, left_up: Run, right_up: Run,up_up:Run,down_up:Run,space_down:Idle },
                Run: {right_down: Idle, left_down: Idle,up_down:Idle, down_down:Idle, left_up: Idle, right_up: Idle ,up_up:Idle ,down_up:Idle ,space_down:Run }
            }
        )

        self.sound=load_wav('skill.wav')
        self.sound.set_volume(128)
        self.bb_draw=True
        pass

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        if self.bb_draw:
            draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x-30,self.y-50,self.x+10,self.y
        pass

    def attack(self):
        arrow= Arrow(self.x,self.y,self.dir,self.bb_draw)
        game_world.add_object(arrow,1)
        self.sound.play(1)
        pass

    def handle_collision(self, group, other):
        if group =='player:wall':
            print('----------------------------player:wall')
            if self.dir == 0:
                self.y -= 1 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 1:
                self.x -= 1 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 2:
                self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 3:
                self.y += 1 * RUN_SPEED_PPS * game_framework.frame_time
        elif group == 'player:job_desk':
            if self.dir == 0:
                self.y -= 1 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 1:
                self.x -= 1 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 2:
                self.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 3:
                self.y += 1 * RUN_SPEED_PPS * game_framework.frame_time
            pass


class job_desk:
    def __init__(self, x1=100, y1=100.0, x2=200, y2=200.0):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.choice=False
        self.bb_draw = True
        pass

    def update(self, val: float = 0.0):
        self.y1 += val
        self.y2 += val
        pass

    def draw(self):
        if self.bb_draw :
            draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x1, self.y2, self.x2, self.y1
        pass

    def attack(self):
        pass

    def handle_collision(self, group, other):
        if group == 'arrow:job_desk' and not self.choice:
            self.choice = True
            job= job_chice()
            game_world.add_object(job,3)
            occupation_select_mode.countdown = get_time()
            t = text(3)
            game_world.add_object(t, 3)
            pass
        pass

class job_chice:
    def __init__(self):
        self.image=load_image('arrow_title.png')
        pass

    def update(self, val: float = 0.0):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 1025, 1031, 180, 780, 90, 90)
        pass

    def get_bb(self):
        pass

    def attack(self):
        pass

    def handle_collision(self, group, other):
        pass

class text:
    def __init__(self,num =3):
        self.image = load_image(f'{num}.png')
        self.count=0
        self.num=num
        self.b_choice =False

    def update(self):
        self.count+=1
        if self.count==850:
            self.num-=1
            game_world.remove_object(self)
            if self.num >= 1:
                t = text(self.num)
                game_world.add_object(t, 3)
            elif self.num ==0:
                server.mode='play'
        pass

    def draw(self):
        if self.count <= 800:
            self.image.clip_draw(0, 0, 100, 100,800, 800,200,200)
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass

class Wall:
    def __init__(self, x1=100, y1=100.0, x2=200, y2=200.0):
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.bb_draw = True
        pass
    def update(self, val: float = 0.0):
        # if (self.y1 > 20.0):
        self.y1 += val
        self.y2 += val
        pass
    def draw(self):
        if self.bb_draw:
            draw_rectangle(*self.get_bb())
        pass
    def get_bb(self):
        return self.x1, self.y2, self.x2, self.y1
        pass
    def attack(self):
        pass
    def handle_collision(self, group, other):
        if group == 'player:wall':
            # print('------------------------------------------------------player:wall')
            pass
        pass