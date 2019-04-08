import retro
#from pyglet.window import key
import numpy as np
import random

from pathlib import Path
from time import sleep

import pygame

# pylint: disable=no-member
pygame.init()
screen = pygame.display.set_mode((1, 1))
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
controller = joysticks[0]
controller.init()
# pylint: enable=no-member

#Controller
# pylint: disable=no-member
def get_keys(pushed_keys):
    PLAYER1 = 0
    LOW_KICK, PUNCH, BLOCK, JUMP, SQUAT, MOVE_LEFT, MOVE_RIGHT, HIGH_KICK = 0, 1, 3, 4, 5, 6, 7, 8 #rewrite these

    #buttons = controller.get_numbuttons()

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                pushed_keys[PLAYER1+HIGH_KICK] = "1"
            if event.button == 2:
                pushed_keys[PLAYER1+LOW_KICK] = "1"
            if event.button == 1:
                pushed_keys[PLAYER1+PUNCH] = "1"                
            if event.button == 3:
                pushed_keys[PLAYER1+BLOCK] = "1"
        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                pushed_keys[PLAYER1+HIGH_KICK] = "0"
            if event.button == 2:
                pushed_keys[PLAYER1+LOW_KICK] = "0"
            if event.button == 1:
                pushed_keys[PLAYER1+PUNCH] = "0"
            if event.button == 3:
                pushed_keys[PLAYER1+BLOCK] = "0"

        if event.type == pygame.JOYHATMOTION:
            if event.value == (0,0):
                pushed_keys[PLAYER1+SQUAT] = "0"
                pushed_keys[PLAYER1+JUMP] = "0"
                pushed_keys[PLAYER1+MOVE_LEFT] = "0"
                pushed_keys[PLAYER1+MOVE_RIGHT] = "0"
            if event.value == (1,0):
                pushed_keys[PLAYER1+SQUAT] = "0"
                pushed_keys[PLAYER1+JUMP] = "0"
                pushed_keys[PLAYER1+MOVE_LEFT] = "0"
                pushed_keys[PLAYER1+MOVE_RIGHT] = "1"
            if event.value == (-1,0):
                pushed_keys[PLAYER1+SQUAT] = "0"
                pushed_keys[PLAYER1+JUMP] = "0"
                pushed_keys[PLAYER1+MOVE_LEFT] = "1"
                pushed_keys[PLAYER1+MOVE_RIGHT] = "0"
            if event.value == (0,1):
                pushed_keys[PLAYER1+SQUAT] = "0"
                pushed_keys[PLAYER1+JUMP] = "1"
                pushed_keys[PLAYER1+MOVE_LEFT] = "0"
                pushed_keys[PLAYER1+MOVE_RIGHT] = "0"
            if event.value == (0,-1):
                pushed_keys[PLAYER1+SQUAT] = "1"
                pushed_keys[PLAYER1+JUMP] = "0"
                pushed_keys[PLAYER1+MOVE_LEFT] = "0"
                pushed_keys[PLAYER1+MOVE_RIGHT] = "0"
            
    return pushed_keys
# pylint: enable=no-member

env_name = 'MortalKombatII-Genesis'
state_name = 'AFK.SubZeroVsJax'
state_path = Path("../states/AFK.SubZeroVsJax.state").resolve()


env = retro.make(env_name,
    use_restricted_actions=retro.Actions.ALL,
    state=str(state_path),
    players=2)

class Agent(object):
    def __init__(self, action_space):
        self.action_space = action_space
    
    #return a random move
    def act(self, observation, reward, done):
        i =  int(2 ** (random.random() * 12 ))
        return  f'{i|2048:012b}' 

pushed_keys = ["0","0","0","0","0","0","0","0","0","0","0","0"]

state = env.reset()
env.render()
#env.viewer.window.on_key_press = get_keys(pushed_keys)
#env.viewer.window.on_key_release = get_keys(pushed_keys)
agent = Agent(env.action_space)
action = f'{0|2048:012b}'
ob, reward, done, _ = env.step( action + "".join(pushed_keys) )
while True:
    for i in range(100000):
        pushed_keys = get_keys(pushed_keys)
        action = agent.act(ob, reward, done)
        ob, reward, done, _ = env.step("".join(pushed_keys) + action )
        env.render()
        sleep(1/90)
    env.reset()
