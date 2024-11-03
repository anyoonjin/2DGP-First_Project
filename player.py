from pico2d import *
from state_machine import *
import game_framework
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

# 상=0 / 우=1 / 좌=2 / 하=3
class Idle:
    @staticmethod
    def enter(player, e):
        if start_event(e):
            player.action = 3
            player.face_dir = 3
        elif right_down(e) or left_up(e):
            player.action = 2
            player.face_dir = 2
        elif left_down(e) or right_up(e):
            player.action = 1
            player.face_dir = 1
        elif down_down(e) or down_up(e):  # 아래로 RUN
            player.face_dir, player.action = 3, 3
        elif up_down(e) or up_down(e):  # 위로 RUN
            player.face_dir, player.action = 0, 0

        player.frame = 0
        player.wait_time = get_time()
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame )* 75,int(player.action)* 75, 75, 75, int(player.x),int( player.y),100,100)


class Run:
    @staticmethod
    def enter(player, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            player.dir, player.face_dir, player.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            player.dir, player.face_dir, player.action = 2, 2, 2
        elif down_down(e) or down_up(e):    #아래로 RUN
            player.dir, player.face_dir, player.action = 3, 3, 3
        elif up_down(e) or up_down(e):  #위로 RUN
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
            player.y += 1* RUN_SPEED_PPS * game_framework.frame_time
        elif player.dir==1:
            player.x += 1 * RUN_SPEED_PPS * game_framework.frame_time
        elif player.dir==2:
            player.x -= 1 * RUN_SPEED_PPS * game_framework.frame_time
        else:
            player.y -= 1 * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 75, int(player.action)* 75, 75, 75, int(player.x), int(player.y),100,100)


# 상=0 / 우=1 / 좌=2 / 하=3
class Player:
    def __init__(self):
        self.image=load_image('player2.png')
        self.x,self.y=800,500
        self.face_dir=3
        self.dir=3
        self.key_count=0
        self.frame=0
        self.action=0
        self.state_machine=StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, up_down:Run, down_down:Run, space_down: self.attack},
                Run: {right_up: Idle, left_up: Idle, up_up:Idle, down_up:Idle, space_down: self.attack}
            }
        )

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
        return self.x-30,self.y-40,self.x+10,self.y+20
        pass

    def attack(self):
        pass

    def handle_collision(self, group, other):
        if group=='boy:key':
            self.key_count+=1

        if group =='boy:zombie':
            close_canvas()
        pass