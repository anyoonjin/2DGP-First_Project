import time

from pico2d import get_time

import server
import key
import game_world


def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_mode):
    global first_key
    first_key=False
    server.start_time =get_time()

    global running, stack
    running = True
    stack = [start_mode]
    start_mode.init()

    global frame_time
    frame_time = 0.0
    current_time = time.time()
    while running:
        print(f"경과 시간: {get_time() - server.start_time}")
        if not first_key and 5.0 <= get_time() - server.start_time <= 5.9:
            print('30초다!!!!!!!!!')
            server.key = key.Key()
            game_world.add_object(server.key, 1)
            game_world.add_collision_pair('player:key', server.player, None)
            game_world.add_collision_pair('player:key', None, server.key)
            text_key = key.key_open_text()
            game_world.add_object(text_key, 1)
            first_key = True
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        new_time = time.time()
        frame_time = new_time - current_time
        frame_rate = 1.0 /  frame_time if frame_time > 0 else 60.0
        current_time += frame_time
        # print(f'Frame Time: {frame_time}, Frame Rate: {frame_rate}')

    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
