import sys
import getopt
import pygame
from random import randint
from pygame.locals import *
from board import Board
from shoter import Shoter
from being import Robot, Human, Alien, LEFT, RIGHT, load_secuences
from shoter import Shoter
from intro_screen import presentation, Phrase
from data import filepath
from score import showScores, Score

FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
FRAMERATE = 30 # how often to check if playback has finished

soundfile=filepath('disparocorto.wav')
soundfile2=filepath('herido.wav') 
soundfile3=filepath('robot_negative.wav')
soundfile_game=filepath('intro.wav')
soundfile_intro=filepath('intro_screen.wav')
soundfile_score=filepath('score.wav')
soundfile_alien=filepath('alien.wav')

bottom_rail = [300, 420, 540]
img_size = ['small', 'medium', 'large']
# Level Generator
levels = []
levels = []
for i in xrange(1,100):
    d = {}
    d['total_time'] = 30 #- 5*i 
    d['cant_robots'] = 40
    d['cant_human'] = (100-i)/4 + i + 5
    d['min_human_to_kill']=  5 + i
    d['human_speed'] =  180 * (1.05**i)
    d['robot_speed'] =  120 * (1.03**i)
    d['alien_speed'] = 100
    levels.append(d)

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

        self.max_robot_to_kill =  10

        self.robot_shoted = 0
        self.human_shoted = 0
        self.alien_shoted = 0
        self.score = 0
        self.robot_shoted_sound = 0
        
        self.intro_sound = 0
        self.game_sound = 0
        self.score_sound = 0
        self.alien_sound = 0

        load_secuences()#Muy importante esto

    def run_intro(self):
        # TODO: ver donde meter los fonts
        if self.intro_sound:
        	self.intro_sound.play(-1)
        font = pygame.font.Font( filepath("HEMIHEAD.TTF"), 100)
        presentation(phrase, font, self.screen)
        if self.intro_sound:
        	self.intro_sound.stop() 
        

    def setup_sound(self):
        """ Initialize sound files
        """
        try:
            pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
        except pygame.error, exc:
            print >> sys.stderr, "I'm sorry buddy, get a sound card: %s", exc

        try:
            self.shot_sound = pygame.mixer.Sound(soundfile)
            self.human_shoted_sound = pygame.mixer.Sound(soundfile2)
            self.robot_shoted_sound = pygame.mixer.Sound(soundfile3)
            self.intro_sound = pygame.mixer.Sound(soundfile_intro)
            self.game_sound = pygame.mixer.Sound(soundfile_game)
            self.score_sound = pygame.mixer.Sound(soundfile_score)
            self.alien_sound = pygame.mixer.Sound(soundfile_alien)
        except pygame.error, exc:
            self.shot_sound = None
            self.human_shoted_sound = None
            self.robot_shoted_sound = None
            self.intro_sound = None
            self.game_sound = None
            self.score_sound = None
            self.alien_sound = None

            print >> sys.stderr, "I'm sorry buddy, get a sound card: %s", exc


    #Genera los personajes antes de comenzar un nivel
    def generate_stuff(self):
        self.robot_rail = []
        self.human_rail = []
        self.alien_rail = []
        
        #Tiempo de arribo de los personajes
        self.robot_arrival = []
        self.human_arrival = []
        self.alien_arrival = []
        self.robot_last_arrival = []
        self.human_last_arrival = []
        self.alien_last_arrival = []
        
        cant_robots_gen = 0
        cant_humans_gen = 0
        for i in xrange(3):
            self.robot_rail.append(pygame.sprite.Group())
            self.human_rail.append(pygame.sprite.Group())
            self.alien_rail.append(pygame.sprite.Group())
            
            #Genero los personajes de todo el nivel, revisar pues el ultimo rail deberia ser lo que queda y no un random
            for cant in xrange(randint(0,self.cant_robots - cant_robots_gen)):
                if randint(0,1):
                    direction = LEFT
                    pos = (self.screen_width+70, bottom_rail[i])
                else:
                    direction = RIGHT
                    pos = (-70, bottom_rail[i])
                self.robot_rail[i].add(Robot(pos, self.board_width, \
                                  self.robot_speed, direction, 10, img_size[i]))
            
            cant_gen = len(self.robot_rail[i].sprites())
            cant_robots_gen += cant_gen
            if cant_gen:
                self.robot_arrival.append(self.total_time* 0.8/cant_gen)
            else:
                self.robot_arrival.append(self.total_time)
            self.robot_last_arrival.append(self.total_time)

            for cant in xrange(randint(0, self.cant_human - cant_humans_gen)):
                if randint(0,1):
                    direction = LEFT
                    pos = (self.screen_width-70, bottom_rail[i])
                else:
                    direction = RIGHT
                    pos = (-70, bottom_rail[i])
                self.human_rail[i].add(Human(pos, self.board_width, \
                                  self.human_speed, direction, 10, img_size[i]))
            self.human_last_arrival.append(self.total_time)

            cant_gen = len(self.human_rail[i].sprites())
            cant_humans_gen += cant_gen

            if cant_gen:
                self.human_arrival.append(self.total_time*0.8/cant_gen)
            else:
                self.human_arrival.append(self.total_time)

            #Aliens
            if randint(0,1):
                direction = LEFT
                pos = (self.screen_width-70, bottom_rail[i])
            else:
                direction = RIGHT
                pos = (-70, bottom_rail[i])
            self.alien_rail[i].add(Alien(pos, self.board_width, \
                                  self.alien_speed, direction, 10, img_size[i]))
            self.alien_arrival.append(randint(1, self.total_time-3))
            self.alien_last_arrival.append(0)
        # Los personajes que estan en la pantalla
        self.robot_render = pygame.sprite.RenderUpdates()
        self.human_render = pygame.sprite.RenderUpdates()
        self.alien_render = pygame.sprite.RenderUpdates()
        self.text_render = pygame.sprite.RenderUpdates()

        if hasattr(self, 'board'):
            score = self.board.score
        else:
            score = 0
        self.board = Board(self, score, self.total_time, self.max_robot_to_kill+1, \
                           self.min_human_to_kill, self.cant_human, self.level)

    #TODO: revisar, no es adecuado el metodo
    def stuff_arrival(self, time_passed_seconds):
        for i in range(3):
            
            #Si no hay robots para ingresar al juego lo genero
            if not self.robot_rail[i].sprites():
                if randint(0,1):
                    direction = LEFT
                    pos = (self.screen_width-70, bottom_rail[i])
                else:
                    direction = RIGHT
                    pos = (-70, bottom_rail[i])
                self.robot_rail[i].add(Robot(pos, self.board_width, \
                                       self.human_speed, direction, 10, img_size[i]))

            self.robot_last_arrival[i] += time_passed_seconds
            if not self.robot_render or self.robot_arrival[i] < self.robot_last_arrival[i]:
                    robot = self.robot_rail[i].sprites()[0]
                    self.robot_render.add(robot)
                    self.robot_rail[i].remove(robot)
                    self.robot_last_arrival[i] = 0


            self.alien_last_arrival[i] += time_passed_seconds
            if self.alien_rail[i].sprites() and self.alien_arrival[i] < self.alien_last_arrival[i]:
                    alien = self.alien_rail[i].sprites()[0]
                    self.alien_render.add(alien)
                    self.alien_rail[i].remove(alien)
                    self.alien_last_arrival[i] = 0

            #Si no hay humanos para ingreasar genero uno nuevo
            if not self.human_rail[i].sprites():
                if randint(0,1):
                    direction = LEFT
                    pos = (self.screen_width-70, bottom_rail[i])
                else:
                    direction = RIGHT
                    pos = (-70, bottom_rail[i])

                self.human_rail[i].add(Human(pos, self.board_width, \
                                       self.human_speed, direction, 10, img_size[i]))

            self.human_last_arrival[i] += time_passed_seconds
            if not self.human_render or self.human_arrival[i] < self.human_last_arrival[i]:
                    human = self.human_rail[i].sprites()[0]
                    self.human_render.add(human)
                    self.human_rail[i].remove(human)
                    self.human_last_arrival[i] = 0

    #completar con las actualizaciones de board y demas yerbas
    def shot(self):
        if pygame.mouse.get_pressed()[0]:
                if self.shot_sound:
                    self.shot_sound.play()
                robot_shoted = pygame.sprite.spritecollide(self.shoter.sprites()[0].target, self.robot_render, True)
                if robot_shoted:
                   if self.robot_shoted_sound:
                       self.robot_shoted_sound.play()
                   self.robot_render.remove(robot_shoted)
                   self.robot_shoted += 1

                human_shoted = pygame.sprite.spritecollide(self.shoter.sprites()[0].target, self.human_render, True)
                if human_shoted:
                   if self.human_shoted_sound:
                       self.human_shoted_sound.play()
                   self.human_render.remove(human_shoted)
                   self.human_shoted += 1

                alien_shoted = pygame.sprite.spritecollide(self.shoter.sprites()[0].target, self.alien_render, True)
                if alien_shoted:
                   if self.alien_sound:
                       self.alien_sound.play()
                   self.alien_render.remove(alien_shoted)
                   self.alien_shoted += 1


    def run_level(self, level):
    	if self.game_sound:
    	    self.game_sound.play(-1)

        clock = pygame.time.Clock()
        self.shoter = pygame.sprite.RenderUpdates(Shoter())

        #game parameters
        self.total_time = levels[level]['total_time']
        self.cant_robots = levels[level]['cant_robots']
        self.cant_human = levels[level]['cant_human']
        self.min_human_to_kill = levels[level]['min_human_to_kill']
        self.human_speed = levels[level]['human_speed']
        self.robot_speed = levels[level]['robot_speed']
        self.alien_speed = levels[level]['alien_speed']

        self.level = level

        self.generate_stuff()

        show_menu = False

        #ver que hacer con los fonts grrrrrrrr..........
        font = pygame.font.Font( filepath("HEMIHEAD.TTF"), 100)
        self.text_render.add(Phrase('Level %d' %(self.level), font, (255, 200, 0), (200, 200), 0.04))
        pause = False
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    exit()
                if e.type == KEYDOWN and pygame.key.get_pressed()[K_ESCAPE]:
                	if self.game_sound:
                		self.game_sound.stop()
                	show_menu = True
                elif e.type == KEYDOWN and pygame.key.get_pressed()[K_p]:
                    pause = not pause

            if show_menu:
                break
            time_passed = clock.tick(30)
            time_passed_seconds = time_passed / 1000.0
            
            # TODO: fijarse si hay que ingresar personajes a la pantalla
            # fijarse si se disparo a alguien ver parametros
            if not pause:
                self.board.update(time_passed_seconds, self.human_shoted, self.robot_shoted, self.alien_shoted)
                self.human_shoted = 0
                self.robot_shoted = 0
                self.alien_shoted = 0

                self.human_render.update(time_passed_seconds)
                self.robot_render.update(time_passed_seconds)
                self.alien_render.update(time_passed_seconds)
                self.text_render.update(time_passed)
                self.stuff_arrival(time_passed_seconds)
            self.shoter.update()

            if not pause:
                self.shot()
            #falta ver si se termino el nivel
            rectlist = self.board.draw()
            rectlist += self.human_render.draw(self.screen)
            rectlist += self.robot_render.draw(self.screen)
            rectlist += self.alien_render.draw(self.screen)
            rectlist += self.text_render.draw(self.screen)
            rectlist += self.shoter.draw(self.screen)
            
            pygame.display.update(rectlist)

            self.board.clear()
            self.human_render.clear(self.screen, self.board.background)
            self.robot_render.clear(self.screen, self.board.background)
            self.robot_render.clear(self.screen, self.board.background)
            self.text_render.clear(self.screen, self.board.background)
            self.shoter.clear(self.screen, self.board.background)

            if self.board.end():
                break

        #end of the level or end of the game
        reason = self.board.end_reason()
        if reason == 'killed too many robots':
            #print 'perdiste ' + reason

            if self.game_sound:
    	        self.game_sound.stop()
            if self.score_sound:
            	self.score_sound.play()

            showScores( self.screen, self.board.score, reason )

            if self.score_sound:
            	self.score_sound.stop()

        reason = self.board.end_reason()
        
        if reason == 'alien killed':
            #print 'perdiste ' + reason

            if self.game_sound:
    	        self.game_sound.stop()
            if self.score_sound:
            	self.score_sound.play()

            showScores( self.screen, self.board.score, reason )

            if self.score_sound:
            	self.score_sound.stop()

        if reason == 'not killed enough humans':
            #print 'perdiste ' + reason

            if self.game_sound:
    	        self.game_sound.stop()
            if self.score_sound:
            	self.score_sound.play()

            showScores( self.screen, self.board.score, reason )

            if self.score_sound:
            	self.score_sound.stop()

        if reason == 'end level':
            if self.game_sound:
                self.game_sound.stop()
            self.max_robot_to_kill = self.board.lives
            self.run_level((level + 1)%100)

phrase = 'Once again, the robots turn against humans to rule the Earth. This time there is no Neo, no Spooner, the humans have no chance. This fight is not about survival, It is just about money because Viky will give you a buck for each human you kill, and you are too greedy and alcoholic to let them live... but be careful, don not shot robots, Viki does not like it. Neither kill aliens, they are stronger than you think. May the force be with you, or not...'

def main():
        
    pygame.init()
    screen = pygame.display.set_mode( [ 800, 600] )

    pygame.mouse.set_visible(False)
    #try:
     #   game_sound = pygame.mixer.Sound(soundfile_game)
    
    #except pygame.error, exc:
     #   game_sound = None
      #  print >> sys.stderr, "I'm sorry buddy, get a sound card: %s", exc

    #if game_sound:
    	#game_sound.play(-1)
    	 
    g = Game( 800, 600, screen)
    g.setup_sound()

    g.run_level(1)
    
    #if game_sound:
    #	game_sound.stop()

def load_fonts():
    global launch_timer_font,active_marbles_font,popup_font,info_font, panel_font
    font_size = 24

    pygame.font.init()
    panel_font = pygame.font.Font(None, font_size)


def text_end_level(level, reason):
    text

if __name__ == "__main__":
    main()

