# -*- coding: utf-8 -*-
import random
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from collections import deque

import sys
sys.path.append('/ai')

# from env import Env
from testEnv import Env

EPISODES = 30000

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=20000)
        
        self.gamma = 0.8    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.tModel = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = keras.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=tf.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def update_tModel(self):
        self.tModel.set_weights(self.model.get_weights())

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        s = state.reshape(1, self.state_size)
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(s)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        # minibatch = random.sample(self.memory, batch_size)
        # for state, action, reward, next_state, done in minibatch:
        #     target = reward
        #     if not done:
        #         target = (reward + self.gamma *
        #                   np.amax(self.tModel.predict(next_state)[0]))
        #     target_f = self.model.predict(state)
        #     target_f[0][action] = target
        #     # self.model.fit(state, target_f, epochs=1, verbose=0)
        #     history = self.model.fit(state, target_f, epochs=1, verbose=0)
        #     print(history.history['loss'])
        # if self.epsilon > self.epsilon_min:
        #     self.epsilon *= self.epsilon_decay
        
        data = random.sample(self.memory, batch_size)
        # ??????Q_target???
        states = np.array([d[0] for d in data])
        next_states = np.array([d[3] for d in data])

        y = self.model.predict(states)
        q = self.tModel.predict(next_states)

        for i, (_, action, reward, _, done) in enumerate(data):
            target = reward
            if not done:
                target += self.gamma * np.amax(q[i])
            y[i][action] = target
        
        loss = self.model.train_on_batch(states, y)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        return loss

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    env = Env()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    # agent.load("./save/cartpole-dqn.h5")
    done = False
    batch_size = 128

    loss = 0
    for e in range(EPISODES):
        state,stateRaw = env.reset()
        # ??????????????????
        color = 1
        lastState = None
        lastAction = None
        lastReward = 0
        totalReward = 0
        for time in range(500):
            action = agent.act(state)
                    
            # ??????????????????????????????????????????????????????????????????
            # 5,3;5,4;4,2;4,5;5,5;4,3;6,4;6,3;4,4;
            # actions = [[5,3],[5,4],[4,2],[4,5],[5,5],[4,3],[6,4],[6,3],[4,4]]
            # action = actions[time][0]*8+actions[time][1]

            next_state, reward, done, next_stateRaw = env.step(action)
            # reward = reward if not done else -10
            # agent.memorize(state, action, reward, next_state, done)
            totalReward += reward
            if lastAction:
                # if color == 0:
                    # ???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
                    # lastReward??????????????????????????????????????????????????????????????????????????????????????????????????????
                    # memWhite.append([lastState,lastAction,lastReward - reward,next_state,done])
                # else:
                    # memBlack.append([lastState,lastAction,lastReward - reward,next_state,done])
                agent.memorize(lastState,lastAction,lastReward - reward,next_state,done)
            
            if done:
                agent.memorize(state,action,reward,next_state,done)
                print(e,'total score:',totalReward,'time:',time,'epsilon:',agent.epsilon,'loss:',loss)
                break
            lastAction = action
            lastState = state
            lastReward = reward
            state = next_state
            stateRaw = next_stateRaw
        
            if len(agent.memory) > batch_size:
                loss = agent.replay(batch_size)
        
        if e % 20 == 0:
            agent.update_tModel()
            agent.save("/ai/mod/dqn.h5")
            print('update_tModel')
        # print(agent.memory)