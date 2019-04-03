import retro
import numpy as np
#import Agent

from pathlib import Path
from time import sleep

env_name = 'MortalKombatII-Genesis'
state_name = 'AFK.SubZeroVsJax'
state_path = Path(f'../states/{state_name}.state').resolve()

env = retro.make(env_name,
    use_restricted_actions=retro.Actions.ALL,
    state=str(state_path),
    players=2)

class RandomAgent(object):
    def __init__(self, action_space):
        self.action_space = action_space
    
    #return a random move
    def act(self, observation, reward, done):
        lst = []
        for i in range(12):
            x = np.random.randint(2)
            lst.append(x)
        return np.asarray(lst)

class Daredevil(object):
    def __init__(self, action_space):
        self.action_space = action_space
    
    #return a move
    def act(self, observation, reward, done, time):
        #TODO read this array from a file, from 'time'-th row
        move = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
        return move

state = env.reset()
agent1 = Daredevil(env.action_space)
agent2 = RandomAgent(env.action_space)
action1 = f'{0|2048:012b}'
action2 = f'{0|2048:012b}'
ob, reward, done, _ = env.step( action1 + action2 )
while True:
    for i in range(100000):
        action1 = agent1.act(ob, reward, done,i)
        action2 = agent2.act(ob, reward, done)
        #print(action1)
        #print(action2)
        #print(action1+action2)
        #ob, reward, done, _ = env.step( action1 + action2 )
        x = np.concatenate((action1,action2))
        #print(x)
        ob, reward, done, _ = env.step(x)
        env.render()
        sleep(1/45)
    env.reset()
