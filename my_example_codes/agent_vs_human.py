import retro
from pyglet.window import key
import numpy as np
from pathlib import Path
import cv2
import imutils
import random
from models.agent import Agent
from utils.memory import Memory

animate_episode = 10
min_exploration_rate = 0.001
max_exploration_rate = .99
exploration_decay_rate = 0.01
gamma = 0.99                                 # Discounted future reward. How much we care about steps further in time
mb_size = 512                                # Learning minibatch size
episodes = 10000

env_name = 'MortalKombatII-Genesis'
state_name = 'AFK.SubZeroVsJax'
state_path = Path("../states/AFK.SubZeroVsJax.state").resolve()

env = retro.make(env_name,
                 use_restricted_actions=retro.Actions.ALL,
                 state=str(state_path),
                 players=2)

PLAYER1, PLAYER2 = 0, 12
LOW_KICK, PUNCH, BLOCK, JUMP, SQUAT, MOVE_LEFT, MOVE_RIGHT, HIGH_KICK = 0, 1, 3, 4, 5, 6, 7, 8

pushed_keys = list('000000000000')
print(pushed_keys)
keymap = {
    key.UP: JUMP,
    key.DOWN: SQUAT,
    key.LEFT: MOVE_LEFT,
    key.RIGHT: MOVE_RIGHT,
    key.MINUS: BLOCK,
    key.RCTRL: LOW_KICK,
    key.PERIOD: HIGH_KICK,
    key.RSHIFT: PUNCH,
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

def scale_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = frame[24:, :]  # Drop upper part of frame  (heath bar, etc.)
    frame = imutils.resize(frame, width=160)  # Scale frane
    return frame

observation = env.reset()
frame = scale_frame(observation)
state = np.expand_dims(frame/255, axis=2)
agent = Agent(env.action_space.shape[0]//2, (100,160,1))

# print(observation.shape)
env.render()
env.viewer.window.on_key_press = key_press
env.viewer.window.on_key_release = key_release

# s = []  # Save previous state(reward, health, etc, NO IMAGE) for debugging

exploration_rate = 1
memory = Memory()

for episode in range(episodes):
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) *\
                       np.exp(-exploration_decay_rate * episode)
    print("Episode: {}/{}\nExploration rate: {:.5f}".format(episode, episodes, exploration_rate))

    for i in range(4000):
        action = agent.act(state, exploration_rate)
        if action==7: action=0
        observation, reward, done, info = env.step(f'{2 ** action:012b}'+"".join(pushed_keys))
        # env.render()  # Show original image
        # s_ = [reward, done, info]  # New state

        frame = scale_frame(observation)
        cv2.imshow("Mortal Kombat II", frame)  # Show modified image

        new_state = np.expand_dims(frame/255, axis=2)  # Normalize input for NN
        memory.append(state, action, reward[0]-reward[1], new_state)
        state = new_state

        # If state change print to see what happened
        # if s != s_:
        #     print(counter, s_)
        #     s = s_
        if info['rounds_won'] > 0 or info['enemy_rounds_won'] > 0:
            break;  # Round ended with win/lose, restart round

        # Wait for 10ms, if 'q' pressed exit
        # key = cv2.waitKey(10) & 0xFF
        # if key == ord("q"):
        #     exit = True
        #     break
    observation = env.reset()


    # Train model
    if episode%10==0:
        if memory.size()>=mb_size:
            print("Training model:")

            minibatch_indexes = random.sample(range(memory.size()), mb_size)

            # inputs = np.zeros((mb_size, 100,160,1))

            s = np.array(memory.state)[minibatch_indexes]
            s_new = np.array(memory.new_state)[minibatch_indexes]

            targets = agent.model.predict(s)
            Q_sa = agent.model.predict(s_new)

            targets[:, np.array(memory.action)[minibatch_indexes]] = np.array(memory.reward)[minibatch_indexes] + gamma * np.max(Q_sa)

            agent.model.train_on_batch(s, targets)

            memory.clear()

        for i in range(4000):
            action = agent.act(state)
            observation, reward, done, info = env.step(f'{2 ** action:012b}' + "".join(pushed_keys))
            env.render()  # Show original image

            if info['rounds_won'] > 0 or info['enemy_rounds_won'] > 0:
                break;  # Round ended with win/lose, restart round

        observation = env.reset()

cv2.destroyAllWindows()
