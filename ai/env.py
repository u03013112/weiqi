# 与core连接，为ai提供env
# 争取做到和gym类似，这样可以较为快速的试用现成代码看效果
import gym
from gym import spaces

import requests
import numpy as np

class Env(gym.Env):
    def __init__(self):
        super(Env, self).__init__()
        self.action_space = spaces.Discrete(64)
        # 暂时简单处理
        self.observation_space = spaces.Box(low=0, high=255,shape=(8,8,3), dtype=np.uint8)


    # 将core返回的status变换成标准的state，需要做什么转换都在这里进行
    def getState(self,status):
        # N个8X8
        # 暂时不分黑白棋，需要下黑子时候黑色就是主色，白子就是对色；反之亦然
        # 本色 4个 8X8 ，目前所有，1、2、3口气
        # 对色 4个 8X8 ，目前所有，1、2、3口气
        # 暂时不用卷积，先试试看
        
        # 重新涂色，根据目前该什么颜色下棋，来确定自己的颜色
        selfColor = 1
        oppoColor = 2
        if status['status'] == 'turn2':
            selfColor = 2
            oppoColor = 1

        qipan = status['qipan']
        # 拆分成8个8x8，共512个输入单元，直接拍平做输入
        # 1、目前自己所有子
        qipanNp = np.array(qipan)
        qipanNpSelf = qipanNp.copy()
        qipanNpSelf[qipanNpSelf==oppoColor]=0
        qipanNpSelf[qipanNpSelf==selfColor]=1
        # 2、目前对方所有子
        qipanNpOppo = qipanNp.copy()
        qipanNpOppo[qipanNpOppo==selfColor]=0
        qipanNpOppo[qipanNpOppo==oppoColor]=1
        # 3、目前可以下子的地方
        qipanNpNull = qipanNp.copy()
        qipanNpNull[:]=0
        qipanNpNull[qipanNp==0]=1

        # TODO：暂时先做两个，后面的确实比较麻烦
        ret = np.stack((qipanNpSelf,qipanNpOppo,qipanNpNull), axis = -1)
        
        # 拍平
        return ret

    # 返回两个值，一个处理后为了机器学习，一个原始为了getAllActions
    def reset(self):
        self.lastBlackReward = 0
        self.lastWhiteReward = 0
        r = requests.get('http://weiqi_core:8080/start')
        status = r.json()
        self.status = status
        return self.getState(status)

    # 获得所有可以落子的地方，如果是不能落子的地方，就直接给一个惩罚吧
    def getAllActions(self):
        status = self.status
        actions = []
        qipan = status['qipan']
        for x in range(8):
            for y in range(8):
                if qipan[x][y] == 0:
                    actions.append(x*8+y)
        return actions

    # return next_state, reward, done, _
    def step(self,action):
        aActions = self.getAllActions()
        if action not in aActions:
            return self.getState(self.status),-100,False,{'err':True}

        # action 是0~63
        x = action/8
        y = action%8
        body = {
            'x':int(x),
            'y':int(y)
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post('http://weiqi_core:8080/do', json=body,headers=headers)
        status = r.json()
        self.status = status

        reward = 0
        if status['status'] == 'turn1':
            reward = (status['score2'] - self.lastWhiteReward)*10
        if status['status'] == 'turn2':
            reward = (status['score1'] - self.lastBlackReward)*10
        self.lastBlackReward = status['score1']
        self.lastWhiteReward = status['score2']
        done = False
        if status['status'] == 'win1' or status['status'] == 'win2':    
            # 只有下最后一步的人才能赢，这里简单处理，为了防止自杀，core需要补上自杀可能bug
            # 如果之后有认输，再重新考虑
            reward += 100
            done = True
        # 第四个返回值到底是干啥的，先借用一下
        return self.getState(status),reward,done,{}

from stable_baselines3.common.env_checker import check_env
if __name__ == '__main__':
    # env = Env()
    # s,sr = env.reset()
    # # print(s)
    # env.step(43)
    # env.step(44)
    # _,r,_,_ = env.step(34)
    # print(r)
    # print(env.getAllActions(s))
    env = Env()
    # check_env(env)
    env.reset()
    print(env.getAllActions())
    print(env.step(27))