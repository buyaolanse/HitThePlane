# -*- coding: utf-8 -*- 

#17.5.23 待制作down图片
#17.5.24 bullet1 ing


import pygame
import sys
import traceback
import myplane
import enemy
import bullet
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen  = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')

background = pygame.image.load('images/background.png').convert()

#定义颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#载入音乐
pygame.mixer.music.load('sound/background.mp3')
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#bomb
bomb_sound = pygame.mixer.Sound('sound/bullet.wav')
bomb_sound.set_volume(0.2)
#supply
supply_sound = pygame.mixer.Sound('sound/bullet.wav')
supply_sound.set_volume(0.2)
#get_bomb
get_bomb_sound = pygame.mixer.Sound('sound/bullet.wav')
get_bomb_sound.set_volume(0.2)
#get_bullet
get_bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
get_bullet_sound.set_volume(0.2)
#upgrade
upgrade_sound = pygame.mixer.Sound('sound/bullet.wav')
upgrade_sound.set_volume(0.2)
#enemy3_fly
enemy3_fly_sound = pygame.mixer.Sound('sound/bullet.wav')
enemy3_fly_sound.set_volume(0.2)
#enemy1_dowm
enemy1_dowm_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_dowm_sound.set_volume(0.2)
#enemy2_down
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2) 
#enemy3_down
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)
#me_down
me_down_sound = pygame.mixer.Sound('sound/bullet.wav')
me_down_sound.set_volume(0.2)



def add_small_enemies(group1, group2, num):
    for i in range (num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range (num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range (num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def main():
    pygame.mixer.music.play(-1)


    #生成我方飞机
    me = myplane.MyPlane(bg_size)

    #生成地方飞机
    enemies = pygame.sprite.Group()

    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    #生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    #生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    #生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4

    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))


    clock = pygame.time.Clock()


    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    
    #用于切换图片
    switch_image = True


    #用于延迟
    delay = 100

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        #检测用户键盘操作
        key_pressed = pygame.key.get_pressed()
        #

        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
            
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()

        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft()

        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()

        screen.blit(background, (0, 0))

        #发射子弹
        if not(delay % 10):
            bullet1[bullet1_index].reset(me.rect.midtop)
            bullet1_index = (bullet1_index + 1) % BULLET1_NUM

        #检测子弹是否打中敌机

        for b in bullet1:
            if b.active:
                b.move()
                screen.blit(b.image, b.rect)
                enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        if e in mid_enemies or e in big_enemies: #中、大型机打一次掉一血
                            e.energy -=1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active = False

        #draw big plane

        for each in big_enemies:
            if each.active:
                each.move()
                if switch_image:
                    screen.blit(each.image1, each.rect)
                else:
                    screen.blit(each.image2, each.rect)

                #血条
                pygame.draw.line(screen, BLACK,\
                                 (each.rect.left, each.rect.top - 5),\
                                 (each.rect.right, each.rect.top - 5),\
                                 2)
                #当生命大约20% 显示绿色，否则显示红色
                energy_remain = each.energy / float(enemy.BigEnemy.energy) #转为float，不然被打一次后就一直为0
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen, energy_color,\
                                 (each.rect.left, each.rect.top - 5),\
                                 (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),\
                                 2)
                    

                #即将出现会播放音效
                if each.rect.bottom == -50:
                    enemy3_fly_sound.play(-1)
            else:
                #destroy
                
                if not(delay % 3):

                    if e3_destroy_index == 0:
                        enemy3_down_sound.play()  #播放e3的destroy音乐
                    screen.blit(each.destroy_images[e3_destroy_index//2],each.rect)
                    e3_destroy_index = (e3_destroy_index + 1) % 12
                    if e3_destroy_index == 0:
                        enemy3_fly_sound.stop()
                        each.reset()
                    
                
                

        #draw mid plane
        for each in mid_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)

                #血条
                pygame.draw.line(screen, BLACK,\
                                 (each.rect.left, each.rect.top - 5),\
                                 (each.rect.right, each.rect.top - 5),\
                                 2)
                #当生命大约20% 显示绿色，否则显示红色
                energy_remain = each.energy / float(enemy.MidEnemy.energy)
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen, energy_color,\
                                 (each.rect.left, each.rect.top - 5),\
                                 (each.rect.left + (each.rect.width * energy_remain), each.rect.top - 5),\
                                 2)
                
            

            else:
                #destroy
                
                if not(delay % 3):
                    if  e2_destroy_index == 0:
                        enemy2_down_sound.play()  #播放e2的destroy音乐
                    
                    screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                    e2_destroy_index = (e2_destroy_index + 1) % 4
                    if e2_destroy_index == 0:
                        each.reset()

        #draw small plane
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)


            else:
                #destroy
                
                if not(delay % 3):
                    print (e1_destroy_index)
                    if  e1_destroy_index == 0:
                        enemy1_dowm_sound.play()  #播放e1的destroy音乐
                    
                    screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 8

                    if e1_destroy_index == 0:
                        each.reset()
        #检测我方飞机是否被撞

        enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)

        if enemies_down:
            #me.active = False         #我方飞机无敌ing
            for e in enemies_down:
                e.active = False
        
        #draw my plane
        if me.active:
                
            if switch_image:
                screen.blit(me.image1, me.rect)
            else:
                screen.blit(me.image2, me.rect)

        else:
            #destroy
            me_down_sound.play()  #播放me的destroy音乐
            if not(delay % 3):
                screen.blit(me.destroy_images[me_destroy_index], me.rect)
                
                me_destroy_index = (me_destroy_index +1) % 4
                if me_destroy_index == 0:
                    print('Game Over')
                    running = False
        #切换图片

        if not (delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()

    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
        




















    

