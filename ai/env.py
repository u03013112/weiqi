# 与core连接，为ai提供env
# 争取做到和gym类似，这样可以较为快速的试用现成代码看效果
import requests
import numpy as np

class ActionSpace:
    def __init__(self,n):
        self.n = n

class Env:
    def __init__(self):
        self.observation_space = np.zeros(128)
        self.action_space = ActionSpace(64)

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
        # 2、目前对方所有子
        qipanNpOppo = qipanNp.copy()
        qipanNpOppo[qipanNpOppo==selfColor]=0
        # TODO：暂时先做两个，后面的确实比较麻烦
        ret = np.concatenate((qipanNpSelf,qipanNpOppo))
        
        # 拍平
        return ret.reshape(-1)

    def reset(self):
        r = requests.get('http://weiqi_core:8080/start')
        status = r.json()
        return self.getState(status)

    # 获得所有可以落子的地方，如果是不能落子的地方，就直接给一个惩罚吧
    def getAllActions(self,status):
        return

    # return next_state, reward, done, _
    def step(self,action):
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
        return self.getState(status)

if __name__ == '__main__':
    env = Env()
    env.reset()
    env.step(0)
    env.step(1)
    env.step(2)