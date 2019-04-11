import retro
from pyglet.window import key
import numpy as np

from pathlib import Path
from time import sleep


env_name = 'MortalKombatII-Genesis'
state_name = 'AFK.SubZeroVsJax'
state_path = Path("../states/AFK.SubZeroVsJax.state").resolve()


env = retro.make(env_name,
    use_restricted_actions=retro.Actions.ALL,
    state=str(state_path),
    players=2)

PLAYER1, PLAYER2 = 0, 12
LOW_KICK, PUNCH, BLOCK, JUMP, SQUAT, MOVE_LEFT, MOVE_RIGHT, HIGH_KICK = 0, 1, 3, 4, 5, 6, 7, 8

pushed_keys = list('000000000000'+'000000000000')
keymap = {
          key.UP: PLAYER2+JUMP,
          key.DOWN: PLAYER2+SQUAT,
          key.LEFT: PLAYER2+MOVE_LEFT,
          key.RIGHT: PLAYER2+MOVE_RIGHT,
          key.MINUS: PLAYER2+BLOCK,
          key.RCTRL: PLAYER2+LOW_KICK,
          key.PERIOD: PLAYER2+HIGH_KICK,
          key.RSHIFT: PLAYER2+PUNCH,
          key.W: PLAYER1+JUMP,
          key.S: PLAYER1+SQUAT,
          key.A: PLAYER1+MOVE_LEFT,
          key.D: PLAYER1+MOVE_RIGHT,
          key.Q: PLAYER1+BLOCK,
          key.LCTRL: PLAYER1+LOW_KICK,
          key.LSHIFT: PLAYER1+HIGH_KICK,
          key.E: PLAYER1+PUNCH
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

while True:
    for i in range(100000):
        observation, reward, done, info = env.step("".join(pushed_keys))
        env.render()
        sleep(0.001)
    env.reset()
