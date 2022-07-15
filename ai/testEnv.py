# 这是一个简单的训练环境，下在没有子的位置就+1，否则-1，仅为了测试ai逻辑是否正确
import numpy as np

class ActionSpace:
    def __init__(self,n):
        self.n = n

class Env:
    def __init__(self):
        self.observation_space = np.zeros(128)
        self.action_space = ActionSpace(64)

    def getState(self):
        status = self.status
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
        qipanNpOppo[qipanNpOppo==oppoColor]=-1
        # TODO：暂时先做两个，后面的确实比较麻烦
        ret = np.concatenate((qipanNpSelf,qipanNpOppo))
        
        # 拍平
        return ret.reshape(-1)

    def reset(self):
        qipan = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            ]
        self.status = {
            'qipan':qipan,
            'status':'turn1',
            'count':0
        }
        status = self.status
        return self.getState(),status


    def step(self,action):
        # action 是0~63
        x = int(action/8)
        y = int(action%8)
        status = self.status
        reward = 0
        qipan = status['qipan']
        if qipan[x][y] == 0:
            color = 0
            if status['status'] == 'turn1':
                color = 1
            elif status['status'] == 'turn2':
                color = 2
            qipan[x][y] = color
            reward = 1
            status['count'] += 1
        else:
            reward = -1

        done = False

        s = self.getState()
        
        if status['status'] == 'turn1':
            status['status'] = 'turn2'
        elif status['status'] == 'turn2':
            status['status'] = 'turn1'

        if status['count'] >= 10:
            done = True
        
        return s,reward,done,status

if __name__ == '__main__':
    env = Env()
    s,sr = env.reset()

    s,r,_,sr = env.step(0)
    print(s,r,sr)
    s,r,_,sr = env.step(0)
    print(s,r,sr)
    s,r,_,sr = env.step(1)
    print(s,r,sr)
    # _,r,_,_ = env.step(34)
    