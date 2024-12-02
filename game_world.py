# world[0] : 백그라운드 객체들
# world[1] : foreground 객체들
from pico2d import get_time

import server

world = [[]for _ in range(4)]
collision_pairs={}

def add_collision_pair(group,a,b):
    if group not in collision_pairs:
        collision_pairs[group]=[[],[]]
    if a:   #a가 있을 때만 추가
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def add_object(o,depth):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_collision_objects(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:pairs[0].remove(o)
        if o in pairs[1]:pairs[1].remove(o)
    pass

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return


def clear():
    for layer in world:
        layer.clear()



def collide(a, b):
    al,ab,ar,at=a.get_bb()
    bl,bb,br,bt=b.get_bb()

    if ar<bl: return False
    if al>br: return False
    if at<bb: return False
    if ab>bt: return False

    return True
    pass


def handle_collisions():
    #게임월드에 등록된 충돌정보를 바탕으로 실제 충돌검사를 수행
    for group, pairs in collision_pairs.items():
        print(f"Group: {group}")
        print("Objects in Group A:")
        for obj in pairs[0]:
            print(f"  {obj}")

        print("Objects in Group B:")
        for obj in pairs[1]:
            print(f"  {obj}")

        for a in pairs[0]:  # A 리스트에서 하나씩 뽑고
            for b in pairs[1]:  # B 리스트에서 하나씩 뽑고, 두 개의 객체 가져오기
                if collide(a, b):
                    # 충돌 시 각 객체에 충돌 처리 메서드 호출
                    print(f"Collision detected between {a} and {b} in group {group}")
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)




    return None