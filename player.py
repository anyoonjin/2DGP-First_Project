from pico2d import *

import game_world
from state_machine import *
import game_framework
from Weapon import Arrow
import play_mode
import background
import zombie
import server
import key

PIXEL_PER_METER = (10.0 / 0.5)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 9.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

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
        elif up_down(e) or down_down(e) or right_up(e) or left_up(e):  # 위로 RUN
            player.face_dir, player.action = 0, 0


        player.frame = 0
        player.wait_time = get_time()
        pass

    @staticmethod
    def exit(player, e):
        #print(f"뭔놈의 event: {e}")
        if space_down(e):
            player.attack()

    @staticmethod
    def do(player):
        player.frame = (player.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(player):
        player.image2.clip_draw(int(player.frame )* 75,int(player.action)* 75, 75, 75, int(player.x),int( player.y),player.size,player.size)

def game_word_total_y(val=0.63):
    for i in range(1,3):
        for obj in game_world.world[i]:
            if obj is not server.player:
                #print(f'{obj}')
                obj.update(val)

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
        elif up_down(e) or down_down(e) or right_up(e) or left_up(e):    #위로 RUN
            player.dir, player.face_dir, player.action = 0, 0, 0

    @staticmethod
    def exit(player, e):
        print(f"뭔이벤트냐..event: {e}")
        print(f"x={player.x}  y={player.y}")
        if space_down(e):
            player.attack()

    # 상=0 / 우=1 / 좌=2 / 하=3
    @staticmethod
    def do(player):
        bg_x1,bg_y1= server.b_g.check()
        player.frame =(player.frame + 4 * ACTION_PER_TIME*game_framework.frame_time) %4
        if player.dir==0:
            if bg_y1<=1400 and player.y>=500:
                server.b_g.update(0.5)
                game_word_total_y(-0.63)

            elif player.y<=900 :
                player.y += 4* RUN_SPEED_PPS * game_framework.frame_time
        elif player.dir==1:
            if player.x <=1520:
                player.x += 5 * RUN_SPEED_PPS * game_framework.frame_time
        elif player.dir==2:
            if player.x>=105:
                player.x -= 5 * RUN_SPEED_PPS * game_framework.frame_time
        elif player.dir==3:
            if  bg_y1>20 and player.y<=600 :    #밑으로 내려갈 배경이 남았을 때/ 남지않았으면 50
                server.b_g.update(-0.5)
                game_word_total_y(0.63)
               #play_mode.b_g.check()
            elif player.y>=80 :
                player.y -= 4 * RUN_SPEED_PPS * game_framework.frame_time

                #print(f'~~~~~~~~~~ BG Y:{player.b_g.y1}')
        print(f"x={player.x}  y={player.y}")
        pass

    @staticmethod
    def draw(player):
        player.image1.clip_draw(int(player.frame) * 75, int(player.action)* 75, 75, 75, int(player.x), int(player.y),player.size,player.size)


# 상=0 / 우=1 / 좌=2 / 하=3
class Player:
    def __init__(self,x=800,y=500, size=120):
        self.image1=load_image('player.png')
        self.image2=load_image('player2.png')
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
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x-30,self.y-50,self.x+10,self.y
        pass

    def attack(self):
        arrow= Arrow(self.x,self.y,self.dir)
        game_world.add_object(arrow,1)
        self.sound.play(1)

        pass

    def handle_collision(self, group, other):
        if group=='player:key':
            pass

        elif group =='player:zombie':
            #close_canvas()
            server.mode='fail'

        elif group =='player:wall':
            print('----------------------------player:wall')
            if self.dir == 0:
                self.y -= 4 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 1:
                self.x -= 5 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 2:
                self.x += 5 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.dir == 3:
                self.y += 4 * RUN_SPEED_PPS * game_framework.frame_time

        elif group =='player:escape':
            self.success=True
            server.mode='clear'
            print("탈출성공!!!!")

