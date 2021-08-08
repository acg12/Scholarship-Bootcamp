import pygame
import random

class Enemy():
    def __init__(self):
        self.__missiles = []
        self.__last_shoot = pygame.time.get_ticks()
        self.__amplitude = random.randint(0, 230)
        self.__speed = random.randint(2, 5)
        self.__rect = pygame.Rect(900, random.randint(0, 460), 100, 40)
        
    def getRect(self):
        return self.__rect
    
    def getAmplitude(self):
        return self.__amplitude
    
    def getX(self):
        return self.__rect.x
    
    def getY(self):
        return self.__rect.y

    def getWidth(self):
        return self.__rect.width

    def getHeight(self):
        return self.__rect.height
    
    def ready_shoot(self):
        now = pygame.time.get_ticks()
        delay = random.randint(2000, 4001)
        if now - self.__last_shoot >= delay:
            self.__last_shoot = now
            return True
        else:
            return False
    
    def move(self):
        self.__rect.x -= self.__speed