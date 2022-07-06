
class Core8X8:
    def __init__(self):
        self.startGame()

    def startGame(self):
        qipan = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            ]
        # status 解释：
        # score1 黑旗比分（提子数） 
        # score2 白旗
        # status 里面有 turn1，turn2，win1，win2
        self.status = {
            'qipan':qipan,
            'score1':0,
            'score2':0,
            'status':'turn1'
        }

    def getStatus(self):
        return self.status

    def do(self,x,y):
        # 检查这个位置是否已经有别的子
        if self.status.qipan[x,y] != 0:
            # 暂时不报错，下了白下
            return

        pass