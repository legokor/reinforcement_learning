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

pushed_keys = list('000000000000'+'000000000000')
keymap = {key.UP: 12+4, key.DOWN: 12+5, key.LEFT: 12+6, key.RIGHT: 12+7, key.RSHIFT: 12+8, key.RCTRL: 12+1, key.MINUS: 12+3, 
          key.W: 4, key.S: 5, key.A: 6, key.D: 7, key.Q: 3, key.LCTRL: 1, key.LSHIFT: 8, key.E: 2}

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
        _ = env.step("".join(pushed_keys) + '000000000000')
        env.render()
        sleep(0.001)
    env.reset()
