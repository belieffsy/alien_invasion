
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings=Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    #screen=pygame.display.set_mode((1200,800))
    pygame.display.set_caption("Alien Ivasion")

    #设置背景色
    #bg_color = (230,230,230)

    #创建一艘飞船
    ship = Ship(ai_settings,screen)
    #创建存储子弹的编组
    bullets = Group()
    bullets_R = Group()



    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(ai_settings,screen,ship,bullets,bullets_R)
        ship.update()
        gf.update_bullets(bullets,bullets_R)

        #print(len(bullets))
        gf.update_screen(ai_settings,screen,ship,bullets,bullets_R)

run_game()
