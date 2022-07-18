from env import Env
from stable_baselines3 import DQN

def dqn():
    env = Env()
    model = DQN('MlpPolicy', env)
    model.learn(total_timesteps=100, log_interval=4)
    model.save("mod/dqn01")

if __name__ == '__main__':
    dqn()
