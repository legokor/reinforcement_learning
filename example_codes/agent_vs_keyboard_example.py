#
# Controlls: MOVE: W A S D 
#            HIT: right arrow
#            BLOCK: left arrow
#            KICK LOW: down arrow
#            KICK HIGH: up arrow
#

import retro
from pyglet.window import key
import numpy as np
import random

from pathlib import Path
from time import sleep


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

PLAYER1 = 0
LOW_KICK, PUNCH, BLOCK, JUMP, SQUAT, MOVE_LEFT, MOVE_RIGHT, HIGH_KICK = 0, 1, 3, 4, 5, 6, 7, 8

pushed_keys = list('000000000000') 
keymap = {
          key.W: PLAYER1+JUMP,
          key.S: PLAYER1+SQUAT,
          key.A: PLAYER1+MOVE_LEFT,
          key.D: PLAYER1+MOVE_RIGHT,
          key.LEFT: PLAYER1+BLOCK,
          key.DOWN: PLAYER1+LOW_KICK,
          key.UP: PLAYER1+HIGH_KICK,
          key.RIGHT: PLAYER1+PUNCH
          }

def key_press(pressed_key, modifier):
    global pushed_keys
    for key, position in keymap.items():
        if key == pressed_key:
            pushed_keys[position] = "1"

def key_release(pressed_key, modifier):
    global pushed_keys
    for key, position in keymap.items():
        if key == pressed_key:
            pushed_keys[position] = "0"

state = env.reset()
env.render()
env.viewer.window.on_key_press = key_press
env.viewer.window.on_key_release = key_release
agent = Agent(env.action_space)
action = f'{0|2048:012b}'
ob, reward, done, info = env.step( action + "".join(pushed_keys) )
while True:
    for i in range(100000):
        action = agent.act(ob, reward, done)
        ob, reward, done, info = env.step("".join(pushed_keys) + action )
        env.render()
        sleep(1/90)
    env.reset()
