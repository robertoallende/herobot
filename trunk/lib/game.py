import sys
import getopt
import pygame
from random import randint
from pygame.locals import *
from board import Board
from shoter import Shoter
from beign import *
from intro_screen import presentation

botton_rail = [300, 420, 540]
img_size = ['small', 'medium', 'large']

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
        #game parameters
        total_time = 30 - 5*level
        cant_robots = 5*level
        cant_human = 10 + level
        min_human_to_kill = 8 + level
        max_robot_to_kill = 3
        stuff_speed = 1.2**level
        
        robot_carril1 = []
        for i in xrange(3):
            robot_rail[i] = pygame.sprite.Group()
            for cant in xrange(randint(1,cant_robots - sum(map(len, robot_carril[i].sprites())))):
                robot_rail[i].add(Robot((bottom_rail[i], 0), stuff_speed, LEFT, 10, img_size[i]))
                human_rail[i].add(Human((bottom_rail[i], 0), stuff_speed, LEFT, 10, img_size[i])) 
        robot_render = pygame.sprite.RenderUpdate()
        human_render = pygame.sprite.RenderUpdate()
        board = Board(self, 0, total_time, 3, min_human_to_kill)
        
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




