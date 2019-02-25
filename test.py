import retro
import numpy as np

from pathlib import Path


env_name = 'MortalKombatII-Genesis'
state_name = 'AFK.SubZeroVsJax'
state_path = Path(f'states/{state_name}.state').resolve()

env = retro.make(env_name,
    use_restricted_actions=retro.Actions.ALL,
    state=str(state_path))

state = env.reset()
while(True):
    for i in range(100000):
        state, reward, done, info = env.step('0')
        env.render()
    env.reset()
