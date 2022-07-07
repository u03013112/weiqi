
class Core8X8:
    def __init__(self):
        self.startGame()

    def startGame(self):
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

    def isJie(self,x,y):
        # TODO:判断是否属于打劫中，打劫中不可下
        return False

    def do(self,x,y):
        status = self.status
        # 检查这个位置是否已经有别的子
        if status['qipan'][x][y] != 0:
            # 暂时不报错，下了白下
            return
        if self.isJie(x,y):
            return
        a = 0
        if status['status'] == 'turn1':
            a = 1
        elif status['status'] == 'turn2':
            a = 2
        else:
            # 暂时只有这两个状态可以下子
            return
        status['qipan'][x][y] = a
        # log here，暂时没想好应该怎么记录，可能最简单的记录方式是只记录下一步下在哪了
        # 开始检测提子或者胜利
        self.killCheck()

        # 更换下棋方
        if status['status'] == 'turn1':
            status['status'] = 'turn2'
        elif status['status'] == 'turn2':
            status['status'] = 'turn1'
    # 获得相连的所有棋子，这个逻辑太过复杂，暂时递归
    def getNeighbor(self,x,y,chan):
        status = self.status

        # 确认这个位置是什么颜色
        color = status['qipan'][x][y]

        # 先把自己加进去，防止递归反向搜索
        if [x,y] not in chan:
            chan.append([x,y])

        # 把他周围的4个方向搜索一遍
        if x>0 and status['qipan'][x-1][y] == color:
            if [x-1,y] not in chan:
                self.getNeighbor(x-1,y,chan)
                
        if x<7 and status['qipan'][x+1][y] == color:
            if [x+1,y] not in chan:
                self.getNeighbor(x+1,y,chan)
            
        if y>0 and status['qipan'][x][y-1] == color:
            if [x,y-1] not in chan:
                self.getNeighbor(x,y-1,chan)

        if y<7 and status['qipan'][x][y+1] == color:
            if [x,y+1] not in chan:
                self.getNeighbor(x,y+1,chan)
        
        return chan

    # 获得还有多少气，简易版本，没有考虑公用气
    def isDead(self,chan):
        qipan = self.status['qipan']
        for p in chan:
            x = p[0]
            y = p[1]
            if x > 0 and qipan[x-1][y] == 0:
                return False
            if x < 7 and qipan[x+1][y] == 0:
                return False
            if y > 0 and qipan[x][y-1] == 0:
                return False
            if y < 7 and qipan[x][y+1] == 0:
                return False
        return True

    def killCheck(self):
        status = self.status
        if status['status'] == 'turn1':
            self.killCheckWhite()
            self.killCheckBlack()
        
        if status['status'] == 'turn2':
            self.killCheckBlack()
            self.killCheckWhite()

    def killCheckBlack(self):
        status = self.status
        blacks = []
        for x in range(len(status['qipan'])):
            line = status['qipan'][x]
            for y in range(len(line)):
                point = status['qipan'][x][y]
                if point == 1:
                    blacks.append([x,y])
        blacks2 = []
        blackChans = []
        for black in blacks:
            if black in blacks2:
                continue
            chan = self.getNeighbor(black[0],black[1],[])
            blacks2 += chan
            blackChans.append(chan)

        # 遍历每个数组是否还有气
        for chan in blackChans:
            if self.isDead(chan):
                # 没有气的就要提子，并计分
                for p in chan:
                    x = p[0]
                    y = p[1]
                    status['qipan'][x][y] = 0
                status['score2'] += len(chan)
                if status['score2'] >= 3:
                    # 胜负也可以在这里判断 
                    status['status'] = 'win2'
    
    def killCheckWhite(self):
        status = self.status
        whites = []
        for x in range(len(status['qipan'])):
            line = status['qipan'][x]
            for y in range(len(line)):
                point = status['qipan'][x][y]
                if point == 2:
                    whites.append([x,y])
        whites2 = []
        whiteChans = []
        for white in whites:
            if white in whites2:
                continue
            chan = self.getNeighbor(white[0],white[1],[])
            whites2 += chan
            whiteChans.append(chan)

        # 遍历每个数组是否还有气
        for chan in whiteChans:
            if self.isDead(chan):
                # 没有气的就要提子，并计分
                for p in chan:
                    x = p[0]
                    y = p[1]
                    status['qipan'][x][y] = 0
                status['score1'] += len(chan)
                if status['score1'] >= 3:
                    # 胜负也可以在这里判断 
                    status['status'] = 'win1'
        
if __name__ == '__main__':
    core = Core8X8()
    
    core.status['qipan'] = [
            [0,0,2,1,2,0,0,0],
            [0,0,2,1,2,0,0,0],
            [0,0,2,1,2,0,0,0],
            [0,0,2,1,2,0,0,0],
            [0,0,1,2,1,0,0,0],
            [0,0,0,1,2,1,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,0],
            ]
    # chan = core.getNeighbor(3,3,[])
    # print(chan)
    core.killCheck()
    print(core.status)