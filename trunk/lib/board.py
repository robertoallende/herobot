"""Game brackground
"""
import sys
import getopt

class Board:
    def __init__(self, game, pos):
        pass


# metodo baston 
def main():
    # ver http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml
    import pygame
    from pygame.locals import *

    pygame.init()
    boxes = []

    screen = pygame.display.set_mode([800, 600])
    pygame.display.update()
    while pygame.event.poll().type != KEYDOWN: pygame.time.delay(10) 


if __name__ == "__main__":
    main()

