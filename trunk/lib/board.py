"""Game brackground
"""
# game.board_height = 576 
# railone = 30% de game.board_height
# railtwo = 50% de game.board_height
# railthree = 70% de game.board_height
# street = 90% de game.board_height

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

class Text(pygame.sprite.Sprite):
    def __init__(self, text, initial_pos, center=0, color = (255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.panel_font = load_fonts()
        self.render_text = self.panel_font.render(text, True, color)
        self.image = self.render_text

        if center: 
            pos = (initial_pos[0]-(self.render_text.get_width() / 2 ), initial_pos[1])
        else:
            pos = (initial_pos[0] , initial_pos[1])

        self.rect = list(pos)
        self.width = self.render_text.get_width()
        self.height = self.render_text.get_height()
        self.alive = True
        self.time_passed = 0
        self.initial_pos = pos
        self.color = color

    def __str__(self):
        return self.text

    def update(self, time_passed, text):
        self.text = text
        self.render_text = self.panel_font.render(text, True, self.color)
        self.image = self.render_text
        self.rect = list(self.initial_pos)
        self.width = self.render_text.get_width()

class Board:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.time_passed = 0

        self.graph_bottom = 20
        self.graph_sides = 2

        self.score = 0
        self.time = 30
        self.lives = 3
        self.target = 100

        #background
        self.background = pygame.Surface(self.game.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.sprites = pygame.sprite.RenderUpdates()

        self.sprites.add( self.draw_background() )
        self.sprites.add( self.draw_time() )
        self.sprites.add( self.draw_score() )
        self.sprites.add( self.draw_target() )
        self.sprites.add( self.draw_lives() )
#       self.draw_background()

    def draw_background(self):
        b = Box([255, 0, 0], [0, 0], [self.game.board_width, self.game.board_height ]) 
        return(b)

    def draw_score(self):
        initial_pos = (self.graph_sides, self.game.board_height - self.graph_bottom)
        self.score_text = Text("Score: " + str(self.score) , initial_pos )
        return self.score_text

    def draw_time(self):
        initial_pos = (self.background.get_rect().centerx - 125 \
                      , self.game.board_height - self.graph_bottom)
        self.time_text = Text("Time Left: " + str(self.time) , initial_pos, 1 )
        return self.time_text


    def draw_target(self):
        initial_pos = (self.background.get_rect().centerx + 125 \
                      , self.game.board_height - self.graph_bottom)
        self.target_text = Text("Required Deaths: " + str(self.time) , initial_pos, 1 )
        return self.target_text


    def draw_lives(self):
        #lives 
        initial_pos = ( self.game.board_width - 60 - self.graph_sides, \
                        self.game.board_height - self.graph_bottom )
        self.lives_text = Text("Error Margin: " + str(self.lives) , initial_pos, 1 )
        return self.lives_text


    def update(self, time_passed, hits ):
        '''Blit everything to the screen'''
        if self.time_passed <= 0:
            self.time -= 1
            self.time_text.update(time_passed, "Time Left: " + str(self.time) )
            self.time_passed = 1

        if hits > 0:
            self.score += hits * 10
            self.score_text.update(time_passed, "Score: " + str( self.score ) )

        if self.target > 0:
            self.target -= hits
            self.target_text.update(time_passed, "Required Deaths: " + str( self.target ) )

        self.time_passed -= time_passed


    def clear(self):
        self.sprites.clear(self.screen, self.background)

    def draw(self):
        self.sprites.draw(self.screen)




# metodo baston 
def load_fonts():
    pygame.font.init()
    panel_font = pygame.font.Font(None, 24) 
    return panel_font


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
    screen = pygame.display.set_mode( [self.game.board_width, self.game.board_height] )

    board = Board(screen)

    clock = pygame.time.Clock()

    while( pygame.event.poll().type != KEYDOWN  ):
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0
        
        board.update(time_passed_seconds, 1)

        rectlist = board.draw()
        pygame.display.update()

        board.clear()

if __name__ == "__main__":
    main()
