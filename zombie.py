from pico2d import *
import game_world
import game_framework

import math
import random

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

'''
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
'''
#하=3      상=2     좌=1    우=0
class Zombie:
    image = None
    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)
        self.image=load_image('zombie.png')
        self.dir = random.randint(0, 3)
        self.speed = 0.0
        self.frame = 0
        self.state = 'Idle'
        self.tx, self.ty = 0, 0

        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # fill here
        self.bt.run()

    def draw(self):
        if math.cos(self.dir) < 0:
            Zombie.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Zombie.images[self.state][int(self.frame)].draw(self.x, self.y, 100, 100)
        self.font.draw(self.x - 10, self.y + 60, f'{self.ball_count}', (0, 0, 255))
        draw_rectangle(*self.get_bb())
        Zombie.marker_image.draw(self.tx - 25, self.ty - 25)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'arrow:zombie':
            game_world.remove_object(self)
        elif group == 'player:zombie':
            close_canvas()

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('Location should be given')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2
        pass

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)  # dir을 radian으로 해석
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
        pass

    def move_to(self, r=0.5):  # r=반지름, 반경
        # 이동 위해선 속도와 시간 필요.
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def set_random_location(self):
        self.tx, self.ty = random.randint(100, 1280 - 100), random.randint(100, 1024 - 100)
        return BehaviorTree.SUCCESS
        pass

    def is_boy_nearby(self, r):
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

        pass

    def move_to_boy(self, r=0.5):
        if self.ball_count >= play_mode.boy.ball_count:  # 공의 개수를 비교
            self.state = 'Walk'
            self.move_slightly_to(play_mode.boy.x, play_mode.boy.y)
            if (self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r)):
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.RUNNING
            pass
        else:
            self.flee_from_boy()

    def flee_from_boy(self):
        self.state = 'Walk'
        self.dir = math.atan2(self.y - play_mode.boy.y, self.x - play_mode.boy.x)  # 소년 반대 방향으로 계산
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.y += distance * math.sin(self.dir)
        self.x += distance * math.cos(self.dir)
        if not self.is_boy_nearby(0.5):  # 소년과 일정 거리 이상 벌어졌으면 성공
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def get_patrol_location(self):
        pass

    def build_behavior_tree(self):
        a1 = Action('Set target location', self.set_target_location, 1000, 1000)
        a2 = Action('Move to', self.move_to)
        root = move_to_target_location = Sequence('Move to target location', a1, a2)

        a3 = Action('Set random location', self.set_random_location)
        root = wander = Sequence('Wander', a3, a2)

        c1 = Condition('소년이 근처에 있는가?', self.is_boy_nearby, 7)  # 7미터

        a4 = Action('소년한테 접근', self.move_to_boy)
        root = chase_boy = Sequence('소년을 추적', c1, a4)

        root = chase_or_flee = Selector('추적 또는 배회', chase_boy, wander)

        self.bt = BehaviorTree(root)
        pass
