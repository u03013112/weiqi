# 尝试记录棋谱
# 暂时思路是每一行记录一局，用分号隔开，每一步用x,y
# 然后尝试指定文件名，每次都是添加在最后面，append
# 文件分割什么的暂时手动处理
class Log:
    def __init__(self,filename='/core/log/log.txt'):
        self.filename = filename
        
    def log(self,steps):
        logStr = ''
        for step in steps:
            logStr += step[0] + ',' + step[1] + ';'
        logStr += '\n'
        with open(self.filename, 'a+') as f:
            f.write(logStr)
    
    # 批量写日志，为了可以在ai下棋的时候进行高效记录
    def logBat(self,stepsList):
        with open(self.filename, 'a+') as f:
            logStr = ''
            for steps in stepsList:
                for step in steps:
                    logStr += str(step[0]) + ',' + str(step[1]) + ';'
                logStr += '\n'
            f.write(logStr)
