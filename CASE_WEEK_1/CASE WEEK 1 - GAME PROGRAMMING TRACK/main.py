import pygame
import os
from pygame.constants import QUIT
from player import Player
from enemy import Enemy
from spritesheet import Spritesheet
from missile import Missile
from explosion import Explosion
import random
import math
pygame.font.init()

WIDTH, HEIGHT = 900, 500
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 40
MISSILE_WIDTH, MISSILE_HEIGHT = 50, 50

# Fonts
pygame.font.init()
MAIN_FONT = pygame.font.SysFont('comicsans', 100)
PRESS_ENTER = pygame.font.SysFont('comicsans', 60)
SCORE_FONT = pygame.font.SysFont('DroidSans', 40)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Site-X')

# Background Position
BG_X = 0
BG_X2 = WIDTH

# Images
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'images/background.png')), (WIDTH, HEIGHT))
WHITE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'images/f35.png'))
BLACK_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'images/sylph.png'))
MISSILE_IMAGE = pygame.image.load(os.path.join('assets', 'images/missile.png'))
EXPLOSION_IMAGE = pygame.image.load(os.path.join('assets', 'images/explosion.png'))

# Velocity
VEL = 5 

# BULLET
pygame.mixer.init()
BULLET_FIRE_SOUND = pygame.mixer.Sound('assets/sounds/sounds/Probe-Gun.wav')
EXPLODE_SOUND = pygame.mixer.Sound('assets/sounds/sounds/Doom-Barrel-Exp.wav')

# FPS
FPS = 60

# Color
BLACK = (0, 0, 0)
MINT = (150, 230, 207)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# SCALING
WHITE_SPACESHIP = pygame.transform.scale(WHITE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
BLACK_SPACESHIP = pygame.transform.scale(BLACK_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Event
LASER_HIT = pygame.USEREVENT + 1
GAME_OVER = pygame.USEREVENT + 2

# Movement
def white_movement(keys_pressed, white):
    if keys_pressed[pygame.K_a] and white.x - VEL > 0:
        white.x -= VEL

    if keys_pressed[pygame.K_d] and white.x + VEL + white.width < WIDTH - 15:
        white.x += VEL

    if keys_pressed[pygame.K_w] and white.y - VEL > 0:
        white.y -= VEL
    
    if keys_pressed[pygame.K_s] and white.y + VEL + white.height < HEIGHT - 15:
        white.y += VEL 
        
def generate_laser(player):
    player_rect = player.getRect()
    if player.ready_shoot():
        laser = pygame.Rect(player_rect.x + player_rect.width,
                            player_rect.y + player_rect.height/2, 30, 5)
        player.shoot(laser)
        BULLET_FIRE_SOUND.play()

def generate_enemy(enemy_last_spawn, enemies):
    delay = random.randint(1000, 2001)
    now = pygame.time.get_ticks()
    
    if now - enemy_last_spawn >= delay:
        enemy = Enemy()
        enemies.append(enemy)
        enemy_last_spawn = now
        
    return enemy_last_spawn

def generate_missile(player, enemies, missiles):
    for enemy in enemies:
        if enemy.ready_shoot():
            x = abs(enemy.getX() - player.getX())
            y = abs(enemy.getY() - player.getY())
            angle = (y/x * 360) % 360
            
            missile_rect = pygame.Rect(enemy.getX(
            ) + enemy.getWidth()/2, enemy.getY() + enemy.getHeight()/2, MISSILE_WIDTH, MISSILE_HEIGHT)
            pos_x = enemy.getX() + enemy.getWidth()/2
            pos_y = enemy.getY() + enemy.getHeight()/2
            missile = Missile(missile_rect, angle, x, y)
            missiles.append(missile)

def move_all(keys_pressed, player, enemies, missiles):
    # move white
    white_movement(keys_pressed, player.getRect())
    
    # move lasers by white
    player.move_lasers()
    
    # move enemies
    for enemy in enemies:
        enemy.move()
    
    # move missiles
    for missile in missiles:
        missile.move()

def rotate(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

# Draw Windows
def draw_window(player, enemies, missiles, explosions, animation_missile, animation_explosion, score):
    # draw background
    global BG_X
    global BG_X2
    BG_X -= 1
    BG_X2 -= 1
    white = player.getRect()
    
    if BG_X < BG_IMG.get_width() * (-1):
        BG_X = BG_IMG.get_width()
    if BG_X2 < BG_IMG.get_width() * (-1):
        BG_X2 = BG_IMG.get_width()
    WIN.blit(BG_IMG, (BG_X, 0))
    WIN.blit(BG_IMG, (BG_X2, 0))
    
    # draw player
    WIN.blit(WHITE_SPACESHIP, (white.x, white.y))
    
    # draw lasers by player (if any)
    x, y = player.draw_lasers(WIN, enemies)
    
    # handle if any new explosions
    if len(x) > 0 and len(y) > 0:
        for i in range(len(x)):
            exp = Explosion(0, x[i], y[i])
            explosions.append(exp)
            EXPLODE_SOUND.play()
    
    for explosion in explosions:
        # print(explosion.getFrame())
        WIN.blit(animation_explosion[explosion.getFrame()], (explosion.getX(), explosion.getY()))
        if explosion.getFrame() >= 15:
            explosions.remove(explosion)
        else:
            explosion.setFrame(explosion.getFrame() + 1)
    
    # draw enemies
    for enemy in enemies:
        WIN.blit(BLACK_SPACESHIP, (enemy.getX(), enemy.getY()))
        if (enemy.getRect()).colliderect(player.getRect()):
            pygame.event.post(pygame.event.Event(GAME_OVER))
        if enemy.getX() < 0 - enemy.getWidth():
            enemies.remove(enemy)
    
    # draw missiles
    for missile in missiles:
        if missile.getX() > WIDTH or missile.getY() > HEIGHT:
            missiles.remove(missile)
            
        # WIN.blit(rotate(pygame.transform.scale(animation_missile[missile.getFrame()], (MISSILE_WIDTH, MISSILE_HEIGHT)), missile.getAngle()), (missile.getX(), missile.getY()))
        WIN.blit(rotate(pygame.transform.scale(animation_missile[missile.getFrame()], (MISSILE_WIDTH, MISSILE_HEIGHT)), 180), (missile.getX(), missile.getY()))
        if missile.getFrame() == 0:
            missile.setFrame(1)
        else:
            missile.setFrame(0)
            
        if missile.getRect().colliderect(player.getRect()):
            pygame.event.post(pygame.event.Event(GAME_OVER))
            missiles.remove(missile)
            

    # SCORE TEXT
    score_text = SCORE_FONT.render("SCORE: " + str(score), 1, WHITE)
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    pygame.display.update()
    
def main_menu():
    WIN.fill(BLACK)
    title = MAIN_FONT.render('Site-X', 1, MINT)
    press_enter = PRESS_ENTER.render('Press ENTER to Start', 1, WHITE)
    
    WIN.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2 - 100))
    WIN.blit(press_enter, (WIDTH/2 - press_enter.get_width()/2, HEIGHT/2 + 50))
    
    pygame.display.update()
    
    play = False
    while not play:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play = True
            if event.type == pygame.QUIT:
                pygame.quit()
    
def game_over(points):
    WIN.fill(BLACK)
    title = MAIN_FONT.render('Game Over', 1, RED)
    score = MAIN_FONT.render('Score: ' + str(points), 1, WHITE)
    press_enter = PRESS_ENTER.render('Press ENTER to restart', 1, WHITE)

    WIN.blit(title, (WIDTH/2 - title.get_width()/2, 100))
    WIN.blit(score, (WIDTH/2 - score.get_width()/2, HEIGHT/2 - score.get_height()/2))
    WIN.blit(press_enter, (WIDTH/2 - press_enter.get_width()/2, HEIGHT - 100))

    pygame.display.update()

    play = False
    while not play:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play = True
            if event.type == pygame.QUIT:
                pygame.quit()

# Main
def main():
    main_menu()
    
    animation_missile = []
    animation_explosion = []
    missile_ss = Spritesheet(MISSILE_IMAGE)
    explosion_ss = Spritesheet(EXPLOSION_IMAGE)
    animation_missile.append(missile_ss.image_at((0, 0, 127, 127), colorkey=-1))
    animation_missile.append(missile_ss.image_at((128, 0, 127, 127), colorkey=-1))
    
    exp_width = 65
    exp_height = 65
    
    for i in range(4):
        for j in range(4):
            animation_explosion.append(explosion_ss.image_at((exp_width * j, exp_height * i, exp_width, exp_height), colorkey=-1))
    
    while True:
        clock = pygame.time.Clock()
    
        # White spaceship rectangle
        white = pygame.Rect(50, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        player = Player(white)
        enemies = []
        missiles = []
        explosions = []
        
        enemy_last_spawn = pygame.time.get_ticks()
        score = 0
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == LASER_HIT:
                    score += 1
                if event.type == GAME_OVER:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        generate_laser(player)
                        
            keys_pressed = pygame.key.get_pressed()
            move_all(keys_pressed, player, enemies, missiles)
            
            enemy_last_spawn = generate_enemy(enemy_last_spawn, enemies)
            generate_missile(player, enemies, missiles)

            draw_window(player, enemies, missiles, explosions, animation_missile, animation_explosion, score)
        # udah game over
        game_over(score)
    

if __name__ == '__main__':
    main()
