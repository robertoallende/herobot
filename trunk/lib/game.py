import sys
import getopt
import pygame
from random import randint
from pygame.locals import *
from board import Board
from shoter import Shoter
from being import Robot, Human, Alien, LEFT, RIGHT
from shoter import Shoter
from intro_screen import presentation
from data import filepath

bottom_rail = [300, 420, 540]
img_size = ['small', 'medium', 'large']

class Game:
    def __init__(self, screen_width, screen_height, screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # esto no lo deberia definir board
        self.board_width = board_heigth =  576
        self.board_width = board_width = 800
        
        self.board_height = screen_height - 24
        self.board_width = screen_width
        self.font_size = 24
        self.screen = screen


    def run_intro(self):
        # TODO: ver donde meter los fonts
        font = pygame.font.Font( filepath("GROOT___.TTF"), 100)
        presentation(phrase, font, self.screen)

    #Genera los personajes antes de comenzar un nivel
    def generate_stuff(self):
        self.robot_rail = []
        self.human_rail = []
        
        #Tiempo de arribo de los personajes
        self.robot_arrival = []
        self.human_arrival = []
        self.robot_last_arrival = []
        self.human_last_arrival = []
        
        cant_robots_gen = 0
        cant_humans_gen = 0
        for i in xrange(3):
            self.robot_rail.append(pygame.sprite.Group())
            self.human_rail.append(pygame.sprite.Group())
            
            #Genero los personajes de todo el nivel, revisar pues el ultimo rail deberia ser lo que queda y no un random
            for cant in xrange(randint(0,self.cant_robots - cant_robots_gen)):
                self.robot_rail[i].add(Robot((0, bottom_rail[i]), self.board_width, \
                                  self.stuff_speed, LEFT, 10, img_size[i]))
            
            cant_gen = len(self.robot_rail[i].sprites())
            cant_robots_gen += cant_gen
            if cant_gen:
                self.robot_arrival.append(int(self.total_time*0.8/cant_gen))
            else:
                self.robot_arrival.append(self.total_time)
            self.robot_last_arrival.append(0)

            for cant in xrange(randint(0, self.cant_human - cant_humans_gen)):
                self.human_rail[i].add(Human((0, bottom_rail[i]), self.board_width, \
                                  self.stuff_speed, LEFT, 10, img_size[i]))
            self.human_last_arrival.append(0)

            cant_gen = len(self.human_rail[i].sprites())
            cant_humans_gen += cant_gen
            if cant_gen:
                self.human_arrival.append(int(self.total_time*0.8/cant_gen))
            else:
                self.human_arrival.append(self.total_time)

        # Los personajes que estan en la pantalla
        self.robot_render = pygame.sprite.RenderUpdates()
        self.human_render = pygame.sprite.RenderUpdates()

        #TODO: revisar parametros
        self.board = Board(self, 0, self.total_time, 3, self.min_human_to_kill)

    #TODO: revisar, no es adecuado el metodo
    def stuff_arrival(self, time_passed):
        for i in range(3):
            self.robot_last_arrival[i] += time_passed
            if self.robot_arrival[i] < self.robot_last_arrival[i] and self.robot_rail[i]:
                    robot = self.robot_rail[i].sprites()[0]
                    self.robot_render.add(robot)
                    self.robot_rail[i].remove(robot)
                    self.robot_last_arrival[i] = 0

            self.human_last_arrival[i] += time_passed
            if self.human_arrival[i] < self.human_last_arrival[i] and self.human_rail[i]:
                    human = self.human_rail[i].sprites()[0]
                    self.human_render.add(human)
                    self.human_rail[i].remove(human)
                    self.human_last_arrival[i] = 0

    #completar con las actualizaciones de board y demás yerbas
    def shot(self):
        if pygame.mouse.get_pressed()[0]:
                robot_shoted = pygame.sprite.spritecollide(self.shoter.sprites()[0], self.robot_render, True)
                if robot_shoted:
                   self.robot_render.remove(robot_shoted)
                   print "pummm", len(robot_shoted)

                human_shoted = pygame.sprite.spritecollide(self.shoter.sprites()[0], self.human_render, True)
                if human_shoted:
                   self.human_render.remove(human_shoted)
                   print "Uno menos...", len(human_shoted)

    def run_level(self, level):
        load_fonts()
        self.board = Board(self)
        clock = pygame.time.Clock()
        self.shoter = pygame.sprite.RenderUpdates(Shoter())

        #game parameters
        self.total_time = 3000 - 5*level
        self.cant_robots = 5*level
        self.cant_human = 1 + level
        self.min_human_to_kill = 8 + level
        self.max_robot_to_kill = 3
        self.stuff_speed = 0.4 * (1.2**level)

        self.generate_stuff()
        #self.stuff_arrival()
        while( pygame.event.poll().type != KEYDOWN  ):
            time_passed = clock.tick(30)
            time_passed_seconds = time_passed / 1000.0
            
            # TODO: fijarse si hay que ingresar personajes a la pantalla
            # fijarse si se disparo a alguien ver parametros
            
            self.board.update(time_passed_seconds, 1, 0)
            self.human_render.update(time_passed)
            self.robot_render.update(time_passed)
            self.shoter.update()
            self.stuff_arrival(time_passed)

            self.shot()
            #falta ver si se termino el nivel
            rectlist = self.board.draw()
            rectlist += self.human_render.draw(self.screen)
            rectlist += self.robot_render.draw(self.screen)
            rectlist += self.shoter.draw(self.screen)
            
            pygame.display.update(rectlist)

            self.board.clear()
            self.human_render.clear(self.screen, self.board.background)
            self.robot_render.clear(self.screen, self.board.background)
            self.shoter.clear(self.screen, self.board.background)

phrase = 'It  is a period  of civil war. The Jedi Knights, once keepers of Peace and Justice, find themselves named Generals in the Republics Struggle against the Separtists. The Separtist army, under the leadership of the mysterious GENERAL GREIVOUS, seems to grow with each passing day. Meanwhile, the Supreme Chancellor PALPATINE continues to tighten his grip of power on the Republic, and becomes increasingly more isolated.Ordered by the JEDI COUNCIL to investigate the allegations made my COUNT DOOKU, ANAKIN SKYWALKER and OBI-WAN KENOBI find themselves in a deadly search for the Dark Lord of the Sith DARTH SIDIOUS, who must be defeated to stop the spread of Rebellion, and bring order back to the Galaxy...'

def main():
    pygame.init()
    screen = pygame.display.set_mode( [ 800, 600] )
    pygame.mouse.set_visible(False)
    g = Game(800,600,screen)
    #g.run_intro()

    g.run_level(1)


def load_fonts():
    global launch_timer_font,active_marbles_font,popup_font,info_font, panel_font
    font_size = 24

    pygame.font.init()
    panel_font = pygame.font.Font(None, font_size)


if __name__ == "__main__":
    main()




