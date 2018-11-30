import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import os

def check_keydown_events(event,ai_settings,screen,stats,sb,ship,aliens,bullets,bullets_R):
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
        save_high_score(stats)
        sys.exit( )
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats,sb, ship, aliens, bullets, bullets_R)


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


def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,bullets_R):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(stats)
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats,sb, ship, aliens, bullets, bullets_R)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,bullets_R,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,bullets_R,mouse_x,mouse_y):
    """在玩家单击play按钮开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb,ship, aliens, bullets, bullets_R)

def start_game(ai_settings,screen,stats,sb,ship,aliens,bullets,bullets_R):
    ai_settings.initalize_dynamic_settings()
    # 隐藏游戏光标
    pygame.mouse.set_visible(False)
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    #重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    bullets_R.empty()

    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

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

def update_screen(ai_settings,screen,stats,sb,ship,alien,bulltes,bulltes_R,play_button):
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
    #显示得分
    sb.show_score()

    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()
    ##让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets,bullets_R):
    """更新子弹位置，并删除已消失的子弹"""
    #更新子弹位置
    bullets.update()
    for bullet in bullets_R:
        bullet.right()

    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    for bullet in bullets_R.copy():
        if bullet.rect.bottom < 0:
            bullets_R.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,bullets_R)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets,bullets_R):
    # 检查是否有子弹击中外星人，如果有删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    collisions_R = pygame.sprite.groupcollide(bullets_R, aliens, True, True)
    if collisions or collisions_R:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points *len(aliens)
            sb.prep_score()
        for aliens in collisions_R.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 如果整群外星人都被消灭，就提升一个等级
        bullets.empty()
        bullets_R.empty()
        ai_settings.increase_speed()
        #提升等级
        stats.level +=1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats,sb):
    """检查是否诞生最高得分"""
    if stats.score> stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def save_high_score(stats):
    """保存最高分在txt文档中"""
    with open('high_score.txt','a')as f:
        high_score = str(stats.high_score)
        f.write('\n'+high_score)

def get_number_aliens_x(ai_settings,alien_width):
    # 计算一行可容纳多少外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return  number_aliens_x

def get_number_row(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height-(3*alien_height)- ship_height)
    number_row = int(available_space_y / (2*alien_height))
    return  number_row

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人，放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    #外星人间距为一个外星人的距离
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_row(ai_settings,ship.rect.height,alien.rect.height)
    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    """有外星人到边缘，采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将外星人下移，并改变方向"""

    for alien in aliens.sprites():
        alien.rect.y +=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets,bullets_R):
    """响应被外星人撞到的飞船"""
    #将ships_left减1
    if stats.ships_left >0:
        stats.ships_left -= 1
        #更新记分牌
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        bullets_R.empty()
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets,bullets_R):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets,bullets_R)
            break
        #象飞船被撞倒一样进行处理

def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets,bullets_R):
    """检查外星人到边缘，更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets,bullets_R)
    #检查是否有飞船到达屏幕底
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets,bullets_R)

