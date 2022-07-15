import sys
sys.path.append('/ai')

from testEnv import Env
from dqn import DQNAgent
import numpy as np

# 测试目前训练结果，很失败
def test1():
    env = Env()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    agent.load("/ai/mod/dqn.h5")
    state,stateRaw = env.reset()
    s = state.reshape(1, agent.state_size)
    act_values = agent.model.predict(s)
    print(act_values[0].reshape(-1,8))
    # action = np.argmax(act_values[0])

from tensorflow import keras
from keras.models import Sequential, load_model, Model
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, add
from keras import regularizers


def test2():
    
    input_shape = (8,8,1)
    inputLayer = Input(input_shape)
    x = Conv2D(
		filters = 2
		, kernel_size = (1,1)
		, data_format="channels_first"
		, padding = 'same'
		, use_bias=False
		, activation='linear'
		, kernel_regularizer = regularizers.l2(0.0001)
		)(inputLayer)

    x = BatchNormalization(axis=1)(x)
    x = LeakyReLU()(x)
    print(x)
    return (x)
    

if __name__ == "__main__":
    test2()


    