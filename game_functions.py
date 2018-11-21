import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event,ai_settings,screen,ship,bullets,bullets_R):
    """#响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_0:
        fire_bullet_R(ai_settings, screen, ship, bullets_R)
    elif event.key == pygame.K_q:
        sys.exit( )

def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings,screen,ship,bullets,bullets_R):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets,bullets_R)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def fire_bullet(ai_settings,screen,ship,bullets):
    """如果没有达到限制就发射一颗子弹"""
    #创建新的子弹，并加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def fire_bullet_R(ai_settings,screen,ship,bullets_R):
    """如果没有达到限制就发射一颗子弹"""
    #创建新的子弹，并加入到编组bullets中
    if len(bullets_R) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets_R.add(new_bullet)

def update_screen(ai_settings,screen,ship,alien,bulltes,bulltes_R):
    """更新屏幕上的图像，并且换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)

    #在飞船和外星人后面重绘所有子弹
    for bullte in bulltes.sprites():
        bullte.draw_bullet()
    for bullte in bulltes_R.sprites():
        bullte.draw_bullet()
    ship.blitme()
    #alien.blitme()
    alien.draw(screen)
    ##让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bullets,bullets_R):
    """更新子弹位置，并删除已消失的子弹"""
    #更新子弹位置
    bullets.update()
    for bullet in bullets_R:
        bullet.right()
    #bullets_R.update()
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    for bullet in bullets_R.copy():
        if bullet.rect.bottom < 0:
            bullets_R.remove(bullet)

def create_fleet(ai_settings,screen,aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少外星人
    #外星人间距为一个外星人的距离
    alien  = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))

    #创建第一行外星人
    for alien_number in range(number_aliens_x):
        alien = Alien(ai_settings,screen)
        alien.x = alien_width+2*alien_width*alien_number
        alien.rect.x = alien.x
        aliens.add(alien)
        #创建一个外星人并将其加入当前行
