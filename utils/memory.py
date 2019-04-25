import numpy as np

class Memory(object):
    def __init__(self):
        self.state = []
        self.action = []
        self.reward = []
        self.new_state = []

    def append(self, state, action, reward, new_state):
        self.state.append(state)
        self.action.append(action)
        self.reward.append(reward)
        self.new_state.append(new_state)

    def appendWithMemory(self, memory):
        for i in range(memory.size()):
            self.state.append(memory.state[i])
            self.action.append(memory.action[i])
            self.reward.append(memory.reward[i])
            self.new_state.append(memory.new_state[i])

    def size(self):
        return len(self.state)

    def clear(self):
        self.state = []
        self.action = []
        self.reward = []
        self.new_state = []

    def pop(self, n=1):
        res = self.state[:n], self.action[:n], self.reward[:n], self.new_state[:n]
        self.state, self.action, self.reward, self.new_state = self.state[n:], self.action[n:], self.reward[n:], self.new_state[n:]
        return res
