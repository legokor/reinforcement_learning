from pyglet.window import key
from models.agent import Agent
from q_learning.worker import *
from utils.config import *
from keras.models import model_from_json

if __name__ == '__main__':
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

    env = retro.make(env_name,
                     use_restricted_actions=retro.Actions.ALL,
                     state=str(state_path),
                     players=2)

    observation = env.reset()
    env.render()
    env.viewer.window.on_key_press = key_press
    env.viewer.window.on_key_release = key_release

    frame = scale_frame(observation)
    state = np.expand_dims(frame/255, axis=2)
    print(state.shape)

    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    agent = Agent(input_shape=state.shape, action_space=env.action_space.shape[0]//2)
    agent.model = loaded_model

    while True:
        observation = env.reset()

        for i in range(4000):
            env.render()
            frame = scale_frame(observation)
            state1 = np.expand_dims(frame / 255, axis=2)
            state2 = np.flip(state1, 1)  # Flip original state for player2

            action1 = agent.act(state1, 0)
            action2 = agent.act(state2, 0)
            observation, reward, done, info = env.step(f'{2 ** action1:012b}' + ''.join(pushed_keys)) #''.join(pushed_keys)

            frame = scale_frame(observation)

            new_state1 = np.expand_dims(frame / 255, axis=2)  # Normalize input for NN
            new_state2 = np.flip(new_state1, 1)

            if info['rounds_won'] > 0 or info['enemy_rounds_won'] > 0:
                break  # Round ended with win/lose, restart round
