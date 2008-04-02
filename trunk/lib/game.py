import sys
import getopt
import pygame
from pygame.locals import *
from board import Board
from intro_screen import presentation

class Game:
    def __init__(self, screen_width, screen_height, screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_height = screen_height - 24
        self.board_width = screen_width
        self.font_size = 24
        self.screen = screen


    def run_intro(self):
        presentation()

    def run_level(self, level):
        load_fonts()
        board = Board(self)
        clock = pygame.time.Clock()

        while( pygame.event.poll().type != KEYDOWN  ):
            time_passed = clock.tick(30)
            time_passed_seconds = time_passed / 1000.0
            board.update(time_passed_seconds, 1)
            rectlist = board.draw()
            pygame.display.update()

            board.clear()

def main():
    pygame.init()
    screen = pygame.display.set_mode( [ 800, 600] )
    g = Game(800,600,screen)

    g.run_level(1)


def load_fonts():
    global launch_timer_font,active_marbles_font,popup_font,info_font, panel_font
    font_size = 24

    pygame.font.init()
    panel_font = pygame.font.Font(None, font_size) 


if __name__ == "__main__":
    main()




