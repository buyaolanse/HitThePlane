# -*- coding: utf-8 -*- 

import pygame
import sys
import traceback
import myplane
import enemy
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen  = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')

background = pygame.image.load('images/background.png').convert()

#载入音乐
pygame.mixer.music.load('sound/background.mp3')
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#bomb
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#supply
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#get_bomb
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#get_bullet
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#upgrade
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#enemy3_fly
enemy3_fly_sound = pygame.mixer.Sound('sound/bullet.wav')
enemy3_fly_sound.set_volume(0.2)
#enemy1_dowm
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#enemy2_down
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2) 
#enemy3_down
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
#me_down
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)



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


    clock = pygame.time.Clock()

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



        #draw big plane

        for each in big_enemies:
            each.move()
            if switch_image:
                screen.blit(each.image1, each.rect)
            else:
                screen.blit(each.image2, each.rect)

            #即将出现会播放音效
            if each.rect.bottom > -50:
                enemy3_fly_sound.play()

        #draw mid plane
        for each in mid_enemies:
            each.move()
            screen.blit(each.image, each.rect)

        #draw small plane
        for each in small_enemies:
            each.move()
            screen.blit(each.image, each.rect)                

        
        #draw my plane

        if switch_image:
            screen.blit(me.image1, me.rect)
        else:
            screen.blit(me.image2, me.rect)
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
        




















    

