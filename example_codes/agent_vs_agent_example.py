import retro
import numpy as np

from pathlib import Path
from time import sleep

env_name = 'MortalKombatII-Genesis'
state_name = 'AFK.SubZeroVsJax'
state_path = Path(f'../states/{state_name}.state').resolve()

env = retro.make(env_name,
    use_restricted_actions=retro.Actions.ALL,
    state=str(state_path),
    players=2)

class Agent(object):
    def __init__(self, action_space):
        self.action_space = action_space
    
    #return a random move
    def act(self, observation, reward, done):
        return self.action_space.sample()

state = env.reset()
agent1 = Agent(env.action_space)
agent2 = Agent(env.action_space)
action1 = f'{0|2048:012b}'
action2 = f'{0|2048:012b}'
ob, reward, done, info = env.step( action1 + action2 )
while True:
    for i in range(100000):
        action1 = agent1.act(ob, reward, done)
        action2 = agent2.act(ob, reward, done)
        ob, reward, done, info = env.step( action1 + action2 )
        env.render()
        sleep(1/45)
    env.reset()
