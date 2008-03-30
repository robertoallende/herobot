"""Game brackground
"""
import sys
import getopt
import pygame
from pygame.locals import *


class Box(pygame.sprite.Sprite):

    def __init__(self, color, initial_position, surface = [200, 200] ):
        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
      
        # Create the image that will be displayed and fill it with the
        # right color.
        self.image = pygame.Surface(surface)
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position


class Board:

    def __init__(self, game, screen):
        self.game = game
#        self.board_complete = 0
#        self.board_timeout = -1
#        self.paused = 0
#        self.launched = 1
        self.screen = screen

        self.graph_bottom = 18
        self.graph_sides = 2

        self.score = 0
        self.time = 30
        self.lives = 3

        #background
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.draw_score()
        self.draw_time()
        self.draw_lives()

        self.draw_background()
        self.draw_railone()
        self.draw_railtwo()
        self.draw_railthree()
        self.draw_street()

    def draw_background(self):
        b = Box([255, 0, 0], [0, 0], [screen_width, screen_height *  30 / 100 ]) 
        self.background.blit(b.image, b.rect)

    def draw_railone(self):
        b = Box([0, 255, 0], [0, board_height *  30 / 100], \
             [screen_width, screen_height *  20 / 100  ]) 
        self.background.blit(b.image, b.rect)

    def draw_railtwo(self):
        b = Box([0, 0, 255], [0, board_height *  50 / 100], \
             [screen_width, screen_height *  20 / 100 ]) 
        self.background.blit(b.image, b.rect)

    def draw_railthree(self):
        b = Box([255, 255, 255], [0, board_height *  70 / 100], \
             [screen_width, screen_height *  20 / 100 ]) 
        self.background.blit(b.image, b.rect)

    def draw_street(self):
        b = Box([0, 200, 200], [0, board_height *  90 / 100], \
            [screen_width, screen_height *  10 / 100 ]) 
        self.background.blit(b.image, b.rect)

    def draw_score(self):
        #drawing score
        score_text = panel_font.render( "Score: " + str(self.score) , 1, (255, 255, 255))
        textpos = score_text.get_rect()
        textpos.topleft = (self.graph_sides, screen_height - self.graph_bottom)
        self.background.blit(score_text, textpos)

    def draw_time(self):
        #drawing time
        time_text = panel_font.render( "Time Left: " + str(self.time) , 1, (255, 255, 255))
        textpos = time_text.get_rect()
        textpos.topleft = (self.background.get_rect().centerx - textpos.right /2 \
                          , screen_height - self.graph_bottom)
        self.background.blit(time_text, textpos)

    def draw_lives(self):
        #lives 
        time_text = panel_font.render( "Error Margin: " + str(self.lives) , 1, (255, 255, 255))
        textpos = time_text.get_rect()
        textpos.topleft = ( screen_width - textpos.right - self.graph_sides, screen_height -  \
                          self.graph_bottom)
        self.background.blit(time_text, textpos)

    def update(self):
        '''Blit everything to the screen'''
        self.screen.blit(self.background, (0, 0)) 
        pygame.display.flip()
        pygame.display.update()


# metodo baston 
def load_fonts():
    global launch_timer_font,active_marbles_font,popup_font,info_font, panel_font
    font_size = 24

    pygame.font.init()
    panel_font = pygame.font.Font(None, font_size) 


def main():
    # ver http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml
    global screen_width
    global screen_height
    global font_size
    global board_height
    board_height = 576
    screen_height = 600
    screen_width = 800

    load_fonts()

    pygame.init()
    boxes = []

    screen = pygame.display.set_mode( [screen_width, screen_height] )
    pygame.display.update()

    board = Board(1, screen)
    board.update()

    
    while pygame.event.poll().type != KEYDOWN: pygame.time.delay(10) 


if __name__ == "__main__":
    main()



