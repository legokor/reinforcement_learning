import retro
import numpy as np

from pathlib import Path
from time import sleep


env_name = 'MortalKombatII-Genesis'
state_name = 'AFK.SubZeroVsJax'
state_path = Path(f'states/{state_name}.state').resolve()

env = retro.make(env_name,
    use_restricted_actions=retro.Actions.ALL,
    state=str(state_path))

state = env.reset()
while True:
    for i in range(100000):
        _ = env.step(f'{0:012b}')
        env.render()
        sleep(1/45)
        _ = env.step(f'{1024:012b}')
        env.render()
        sleep(1/45)
    env.reset()
