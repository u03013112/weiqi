# env改进
# 1、env可以接受参数，即可以使用一个模型来做对手
# 2、env添加允许动作集合，并将不允许动作的reward设置为-100，并且不改变任何state
# 3、env应该一直让正确的人来下棋，比如下错了位置还是由刚才的选手来操作
from env import Env
from stable_baselines3 import DQN

class Env2(Env):
    def __init__(self,modeName = ''):
        super().__init__()
        self.model = DQN.load(modeName, env=self)

    def step(self,action):
        # 操作者操作一下
        next_state, reward, done, info = super().step(action)
        if 'err' in info:
            # 下的位置不对，直接返回惩罚
            return next_state, reward, done, info

        # 让ai下一个子
        while True:
            action, _states = self.model.predict(next_state, deterministic=False)
            next_state, reward, done, info = super().step(action)
            if 'err' not in info:
                # 下的位置不对就重新下
                break

        return next_state, reward, done, info

if __name__ == '__main__':
    env = Env2('mod/dqn01')
    print(env.reset())
    print(env.step(27))
    print(env.step(26))