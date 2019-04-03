import retro
import numpy as np

env_name = 'MortalKombatII-Genesis'
env = retro.make(env_name, use_restricted_actions=retro.Actions.ALL)

state = env.reset()
pass
while(True):
    for i in range(100000):
        state, reward, done, info = env.step('0')
        env.render()
    env.reset()
