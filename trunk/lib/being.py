"""clase abstracta para generar persona
int(round(uniform(1,2))
"""
import sys
import getopt
import data
import pygame
from random import uniform
from pygame.locals import *

class Being(pygame.sprite.Sprite):
    def __init__(self, carril):
        #self.image, self.rect = load_image('baldef __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializerl.png')
        self.image = pygame.Surface([15, 30])
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.image.fill([255,0,0])
        self.rect = self.image.get_rect()
        self.rect.topleft = carril
        self.speed = 10
    
    def update(self,direction):
        screen = pygame.display.get_surface()
        if self.rect.left < self.area.width  and direction == "right":
            self.rect.left = self.rect.left +1
        elif self.rect.left > 0 and direction == "left":
            self.rect.left = self.rect.left -1
            
    def setpos(self,newpos):
        self.rect.topleft = newpos
        print "hola samigos"
       

# metodo baston 
def main():
    # ver http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml
    
    pygame.init()

    screen = pygame.display.set_mode([800, 600])
    pygame.display.update()

    being = Being((0,500))
    direction = "right"
    area = screen.get_rect()
    while pygame.event.poll().type != KEYDOWN:
        screen.fill([0, 0, 0]) # blank the screen.

        # Save time by only calling this once
        time = pygame.time.get_ticks() 
        being.update(direction)
        print area.width
        if (being.rect.left == area.width and direction == "right") or (being.rect.left == 0 and direction == "left"):
            prob = int(round(uniform(1,2)))
            if prob == 1:
                being.setpos((0,500))
                direction = "right"
            else:
                being.setpos((800,500))
                direction = "left"
        screen.blit(being.image, being.rect)

        pygame.display.update()

if __name__ == "__main__":
    main()

