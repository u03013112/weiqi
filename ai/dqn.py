# -*- coding: utf-8 -*-
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

import sys
sys.path.append('/ai')

from env import Env

EPISODES = 1000

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

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
    batch_size = 32

    for e in range(EPISODES):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        # 每一盘做两套mem，为了可以将奖励往回传
        memBlack = []
        memWhite = []
        lastState = None
        lastAction = None
        lastReward = 0
        for time in range(500):
            # color == 0 的时候是黑色的，否则是白色的
            color = time%2

            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            # reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            # agent.memorize(state, action, reward, next_state, done)
            
            if lastAction:
                if color == 0:
                    # 如果现在是下黑色，那么上一次应该是下白色，并且现在下完黑色的样子是下白色的下一状态
                    # lastReward是上次白旗下完自己的奖励，这次黑棋的奖励应该是白旗的惩罚，所以要减去
                    memWhite.append([lastState,lastAction,lastReward - reward,next_state,done])
                else:
                    memBlack.append([lastState,lastAction,lastReward - reward,next_state,done])
            
            if done:
                if color == 0:
                    # 如果现在是下黑色，那么代表黑色的操作导致游戏结束，直接给这次操作奖励
                    memBlack.append([state,action,reward,next_state,done])
                else:
                    memWhite.append([state,action,reward,next_state,done])
                # 整理黑白两个mem，计算reward
                for i in range(len(memBlack)):
                    if i == 0:
                        continue
                    # 这里认为至少会有2步，不会1步认输，所以暂不考虑越界
                    memBlack[len(memBlack)-1-i][2] += agent.gamma * memBlack[len(memBlack)-i][2]
                
                for i in range(len(memWhite)):
                    if i == 0:
                        continue
                    memWhite[len(memWhite)-1-i][2] += agent.gamma * memWhite[len(memWhite)-i][2]
                # 然后拼到一起以供replay
                for m in memBlack:
                    agent.memorize(m[0], m[1], m[2], m[3], m[4])
                for m in memWhite:
                    agent.memorize(m[0], m[1], m[2], m[3], m[4])
                break

            lastAction = action
            lastState = state
            lastReward = reward
            state = next_state
            # if len(agent.memory) > batch_size:
            #     agent.replay(batch_size)
        # if e % 10 == 0:
        #     agent.save("./save/cartpole-dqn.h5")