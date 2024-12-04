from pico2d import *

import game_world
import game_framework
import math
import random

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 8.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0


class Zombie:
    image = None

    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)
        self.image = load_image('zombie.png')
        self.dir = random.randint(0, 3)
        self.face_dir = self.dir
        self.speed = 0.0
        self.frame = 0
        self.state = 'Idle'
        self.build_behavior_tree()
        self.wander_num=random.randint(0,3)     # 배회할 때\
        self.tx,self.ty=0,0
        self.set_random_location()

    def get_bb(self):
        if self.face_dir==3 or self.face_dir ==2:
            return self.x - 48, self.y - 50, self.x + 48, self.y + 50
        else:
            return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def update(self,val=0):
        self.y+=val
        self.frame = (self.frame + 4 * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.bt.run()

    def draw(self):
        self.image.clip_draw(int(self.frame) * 100, int(self.face_dir) * 100, 100, 100, self.x, self.y, 150, 150)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'arrow:zombie':
            game_world.remove_object(self)
            remove_zombie(self)
        elif group == 'player:zombie':
            close_canvas()

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        if abs(ty - self.y) >= abs(tx - self.x):
            if ty - self.y < 0:  # 상
                self.face_dir = 3
            else:  # 하
                self.face_dir = 2
        else:
            if tx - self.x < 0:  # 왼쪽
                self.face_dir = 1
            else:  # 오른쪽
                self.face_dir = 0
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def is_boy_nearby(self, r):
        if self.distance_less_than(server.player.x, server.player.y, self.x, self.y, r):
            self.build_behavior_tree(300)
            print("소년 발견!")
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(server.player.x, server.player.y)
        if self.distance_less_than(server.player.x, server.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        if self.wander_num == 0:  # 오른쪽
            self.tx = self.x + 100
            self.wander_num=1
        elif self.wander_num == 1:  # 왼쪽
            self.tx = self.x - 100
            self.wander_num = 0
        elif self.wander_num == 2:  # 위쪽
            self.ty = self.y + 100
            self.wander_num = 3
        elif self.wander_num == 3:  # 아래쪽
            self.ty = self.y - 100
            self.wander_num=2
        return BehaviorTree.SUCCESS

    def move_to(self, r=0.5):  # r=반지름, 반경
        # 이동 위해선 속도와 시간 필요.
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def build_behavior_tree(self,r=10):
        a2 = Action('Move to', self.move_to)
        a3 = Action('Set random location', self.set_random_location)
        root = wander = Sequence('Wander', a3, a2)

        c1 = Condition('소년이 근처에 있는가?', self.is_boy_nearby, r)  # 9미터로 설정

        # 'Move to boy' 행동 (플레이어에게 접근)
        a4 = Action('소년한테 접근', self.move_to_boy)
        chase_boy = Sequence('소년을 추적', c1, a4)

        root = chase_or_wander = Selector('추적 또는 배회', chase_boy, wander)

        # 행동 트리 루트 설정
        self.bt = BehaviorTree(root)


Zombies=[]
def remove_zombie(o):
    if o in Zombies:
        Zombies.remove(o)
        return