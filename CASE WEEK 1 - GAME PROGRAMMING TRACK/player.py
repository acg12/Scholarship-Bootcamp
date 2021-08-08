import pygame
import os

# baca array buat animasi explosion

class Player():
    def __init__(self, rect):
        self.__rect = rect
        self.__lasers = []
        self.__delay = 800
        self.__last_shoot = pygame.time.get_ticks()
        
    def getRect(self):
        return self.__rect
    
    def getX(self):
        return self.__rect.x
    
    def getY(self):
        return self.__rect.y
    
    def getLasers(self):
        return self.__lasers
    
    def draw_explosion(self, window, enem_X, enem_Y):
        pass
        
    def draw_lasers(self, window, enemies):
        x = []
        y = []
        lasers = self.__lasers
        for laser in lasers:
            pygame.draw.rect(window, (255, 255, 0), laser)
            
            for enemy in enemies: 
                if enemy.getRect().colliderect(laser):
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))
                    enemies.remove(enemy)
                    x.append(enemy.getX())
                    y.append(enemy.getY())
            
            # if laser keluar screen
            if laser.x > 900:
                lasers.remove(laser)
        return x, y
    
    def move_lasers(self):
        lasers = self.__lasers
        for laser in lasers:
            laser.x += 5
            
    def ready_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.__last_shoot >= self.__delay:
            self.__last_shoot = now
            return True
        else:
            return False
    
    def shoot(self, laser):
        self.__lasers.append(laser)