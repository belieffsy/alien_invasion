
class GameStats():
    """跟踪游戏的统计信息"""
    def __init__(self,ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #让游戏处于非活动状态
        self.game_active = False
        #在任何情况下都不应该重置最高得分
        self.read_high_score()

    def reset_stats(self):
        """初始化游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def read_high_score(self):
        with open("high_score.txt",'r') as f:
            lines = f.readlines()
            if lines ==[]:
                self.high_score = 0
            else:
                self.high_score = int(lines[-1])

