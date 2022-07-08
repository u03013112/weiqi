# 与core连接，为ai提供env
# 争取做到和gym类似，这样可以较为快速的试用现成代码看效果
import requests

class Env:
    def __init__(self):
        self.observation_space = []
        self.action_space = {}
        self.action_space.n = 64

    def reset(self):
        # body = {
        
        # }
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # r = requests.post('https://hq1.appsflyer.com/api/cohorts/v1/data/app/com.topwar.gp?format=json', json=body,headers=headers)
        # print(r.json())
        r = requests.get('http://weiqi_core:8080/start')
        ret = r.json()
        print(ret)

    # return next_state, reward, done, _
    def step(self,action):
        pass

if __name__ == '__main__':
    env = Env()
    env.reset()