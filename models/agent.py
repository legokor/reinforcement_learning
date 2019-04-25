import tensorflow as tf
from keras import backend as K

num_cores = 6

num_CPU = 1
num_GPU = 1

config = tf.ConfigProto(intra_op_parallelism_threads=num_cores,\
        inter_op_parallelism_threads=num_cores, allow_soft_placement=True,\
        device_count = {'CPU' : num_CPU, 'GPU' : num_GPU})
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
K.set_session(session)


from tensorflow import set_random_seed
from keras.models import Sequential, Model
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
from keras.layers import Dropout, Conv2D, Flatten, MaxPooling2D
import numpy as np
import random

# Set random seed to always predict the same values
np.random.seed(42)
# set_random_seed(69) # Tensoflow

class Agent(object):
    def __init__(self, action_space, input_shape):
        self.action_space = action_space
        model = Sequential()
        model.add(Conv2D(32, (3, 3), padding="same", activation="relu", input_shape=input_shape))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, (3, 3), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(100, activation='sigmoid'))
        model.add(Dense(80, activation='sigmoid'))
        model.add(Dense((action_space), activation='linear'))
        sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='mae', optimizer=sgd, metrics=['mae','mse'])
        self.model = model

    # return a random move
    def act(self, state, exploration_rate=0):
        if np.random.rand() <= exploration_rate:
            action = np.random.randint(self.action_space)
        else:
            Q = self.model.predict(np.expand_dims(state, axis=0))  # Q-values predictions
            action = np.argmax(Q)

        return action
