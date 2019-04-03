import retro
from pyglet.window import key
import numpy as np
import cv2
import imutils

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
rgb = cv2.cvtColor(state, cv2.COLOR_BGR2RGB)
cv2.imshow("Mortal Kombat II", rgb)

print(state.shape)
env.render()
env.viewer.window.on_key_press = key_press
env.viewer.window.on_key_release = key_release

counter = 0
done = False

s = []

while not done:
    state, reward, done, info = env.step("".join(pushed_keys))
    env.render() # Show original image
    s_ = [reward, done, info]

    frame = cv2.cvtColor(state, cv2.COLOR_BGR2GRAY)
    frame = frame[24:, :] # Drop upper part of frame  (heath bar, etc.)
    frame = imutils.resize(frame, width=160) # Scale frane
    cv2.imshow("Mortal Kombat II", frame) # Show modified image

    input = frame / 255 # Normalization

    counter += 1
    if s != s_:
        print(counter, s_)
        s = s_

    key = cv2.waitKey(10) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
