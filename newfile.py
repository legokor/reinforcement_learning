import retro
import numpy as np

env_name = 'MortalKombatII-Genesis'
env = retro.make(env_name, use_restricted_actions=retro.Actions.ALL)

state = env.reset()
while(True):
    for i in range(100000):
        if i%2==0:
            state, reward, done, info = env.step('1024')
        else:
            state, reward, done, info = env.step('256')
        env.render()
env.reset()
