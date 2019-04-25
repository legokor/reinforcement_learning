from models.agent import Agent
from utils.model import *
from q_learning.worker import *
from utils.config import *
import matplotlib.pyplot as plt
from keras.models import model_from_json


gamma = 0.95                                 # Discounted future reward. How much we care about steps further in time
batch_size = 512                                # Learning minibatch size
episodes = 10000

min_exploration_rate = 0.05
max_exploration_rate = .99
exploration_decay_rate = 0.01

if __name__ == '__main__':
    env = retro.make(env_name,
                     use_restricted_actions=retro.Actions.ALL,
                     state=str(state_path),
                     players=2)

    observation = env.reset()
    frame = scale_frame(observation)
    state = np.expand_dims(frame/255, axis=2)
    print(state.shape)

    episode = 0
    agent = Agent(input_shape=state.shape, action_space=env.action_space.shape[0]//2)
    memory = Memory()

    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
    loaded_model.compile(loss='mae', optimizer=sgd, metrics=['mae', 'mse'])
    print("Loaded model from disk")

    agent.model = loaded_model

    losses = []
    round = 0

    while True:
        # print("Creating samples...")
        episode += 1
        exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * \
                                np.exp(-exploration_decay_rate * episode)
        print("Episode: {}\nExploration rate: {:.5f}".format(episode, exploration_rate))

        observation = env.reset()

        b = 0
        broken = False
        round += 1

        while b < 4000//128 and not broken:
            b += 1
            # print('{}/{}'.format(b, 4000//128), end="\r", flush=True)

            for i in range(128):
                frame = scale_frame(observation)
                state1 = np.expand_dims(frame / 255, axis=2)
                state2 = np.flip(state1, 1)  # Flip original state for player2

                action1 = agent.act(state1, exploration_rate)
                action2 = agent.act(state2, exploration_rate)
                observation, reward, done, info = env.step(f'{2 ** action1:012b}' + f'{2 ** action2:012b}')

                frame = scale_frame(observation)

                new_state1 = np.expand_dims(frame / 255, axis=2)  # Normalize input for NN
                new_state2 = np.flip(new_state1, 1)

                memory.append(state1, action1, reward[0] - reward[1], new_state1)
                memory.append(state2, action2, reward[1] - reward[0], new_state2)

                if info['rounds_won'] > 0 or info['enemy_rounds_won'] > 0:
                    broken = True
                    break  # Round ended with win/lose, restart round

            if broken:
                continue


            # print("Training model...")
            s = np.array(memory.state)
            s_new = np.array(memory.new_state)

            targets = agent.model.predict(s)
            Q_sa = agent.model.predict(s_new)

            targets[:, np.array(memory.action)] = np.array(memory.reward) + gamma * np.max(Q_sa)

            train_result = agent.model.train_on_batch(s, targets)
            losses.append(train_result[0])
            # print(train_result, agent.model.metrics_names)

            memory.clear()

            try:
                model_json = agent.model.to_json()
                with open("model.json", "w") as json_file:
                    json_file.write(model_json)
                # serialize weights to HDF5
                agent.model.save_weights("model.h5")
                # print("Saved model to disk")
            except:
                print("Model save failed")
                pass

        print()

        if(len(losses)>=50):
            plt.plot([i for i in range(len(losses)-50, len(losses))], losses[-50:])
            plt.show()

        if round % 10 == 0:
            print('Testing model...')

            observation = env.reset()

            reward0 = 0
            reward1 = 0

            for i in range(4000):
                env.render()

                frame = scale_frame(observation)
                state1 = np.expand_dims(frame / 255, axis=2)
                state2 = np.flip(state1, 1)  # Flip original state for player2

                action1 = agent.act(state1, 0)
                action2 = agent.act(state2, 0)
                observation, reward, done, info = env.step(f'{2 ** action1:012b}' + f'{2 ** action2:012b}')

                frame = scale_frame(observation)

                new_state1 = np.expand_dims(frame / 255, axis=2)  # Normalize input for NN
                new_state2 = np.flip(new_state1, 1)

                reward0 += reward[0] - reward[1]
                reward1 += reward[1] - reward[0]

                if info['rounds_won'] > 0 or info['enemy_rounds_won'] > 0:
                    broken = True
                    break  # Round ended with win/lose, restart round

            print('Rewards: ', reward0, reward1)
