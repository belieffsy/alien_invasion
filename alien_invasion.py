import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreborad import Scoreboard

def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings=Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    #screen=pygame.display.set_mode((1200,800))
    pygame.display.set_caption("Alien Ivasion")

    #创建play按钮
    play_button = Button(ai_settings,screen,"Play")

    #创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    #创建一艘飞船
    ship = Ship(ai_settings,screen)
    #创建存储子弹的编组
    bullets = Group()
    bullets_R = Group()
    #外星人群
    aliens = Group()

    #创建外星人群
    #alien = Alien(ai_settings,screen)
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,bullets_R)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,bullets_R)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets,bullets_R)

        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,bullets_R,play_button)

run_game()
