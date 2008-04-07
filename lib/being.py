#clase-n-ss-tamno.png
import sys
import getopt
import data
import pygame
from random import uniform, choice
from pygame.locals import *
from shoter import Shoter

RIGHT = 1
LEFT = -1
ROBOT_IMAGES = 2
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
FRAMERATE = 30 # how often to check if playback has finished
soundfile='./../data/disparocorto.wav'
soundfile2='./../data/herido.wav'

secuences = {}

#para probarlo hacer click sobre el objeto que da vueltas por ahi!!! y da vueltas como zaino!!!
#TODO: *decidir que hacen cuadno se les dispara ( por ahora los humanos giran como el juego punch chimp)
#      *comentar el codigo 
#      * como carajo le agregamos la sangre????
#      *como destruimos un sprite para que una vez muerto no joda mas??
#      *donde y que le devolvemos al gil que dispara

def load_secuences():
    import re
    import os
    from data import data_dir
    
    global secuences
    
    secuences = {}
    #arreglar si piden size
    prog = re.compile(r'(?P<clase>mujer|hombre|robot|alien)-(?P<nro>\d)-(?P<nro_sec>\d{2})\.png')
    
    for f in os.listdir(data_dir):
        res = prog.match(f)
        if res:
            res = res.groupdict()
            clase, nro = res['clase'], res['nro']
            if not secuences.has_key(clase):
                secuences[clase] = {}
            
            if secuences[clase].has_key(nro):
                secuences[clase][nro] += 1
            else:
                secuences[clase][nro] = 1

class Being(pygame.sprite.Sprite):
    def __init__(self, pos, screen_width, images, speed=1, direction=LEFT, speed_change=1):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect =  data.load_image(images[0])
        self.actual_img = 0
        self.images = [data.load_image(img)[0] for img in images]
        self.set_pos(pos)
        self.screen_width = screen_width
        self.speed = speed
        self.speed_change = speed_change
        self.alive = True
        self.direction = direction
        self.last_img_change  = 0
        if direction == RIGHT:
            self.images = [pygame.transform.flip(img,1,0) for img in self.images]
            self.image = self.images[0]
        #tomo el screen y sus medidas
       
    def update(self,time_passed_seconds):
        if self.alive:
            if  self.speed_change < self.last_img_change:
                self.actual_img = (self.actual_img  + 1) % len(self.images)
                self.image = self.images[self.actual_img]
                self.last_img_change = 0
            self.last_img_change += 1
            
            #Si se llega a uno de los bordes se pega la vuelta
            if (self.screen_width + 50 < self.rect.left and self.direction == RIGHT) or \
               (self.rect.left + self.rect.width  + 50 < 0 and self.direction == LEFT):
               self.set_direction(-self.direction)
	    self.rect.left = self.rect.left + self.direction*time_passed_seconds*self.speed
        else:
                pass

    def set_direction(self, direction):
        if self.direction != direction:
            self.direction = direction
            self.images = [pygame.transform.flip(img,1,0) for img in self.images]

    def set_pos(self,newpos):
        self.rect.bottom = newpos[1]
        self.rect.left = newpos[0]

#TODO:fix it, cuando tengamos las imagenes hay que actualizarlo
class Robot(Being):
    def __init__(self, pos, screen_width, speed=1, direction=LEFT, speed_change=1, size='small'):
        sec = choice(secuences['robot'].keys())
        images = ['robot-%s-%02d.png' %(sec, x) for x in xrange(secuences['robot'][sec])]
        Being.__init__(self, pos, screen_width, images, speed, direction,speed_change)


class Human(Being):
    def __init__(self, pos, screen_width, speed=1, direction=LEFT, speed_change=1, size='small'):
        sex  = choice(['hombre', 'mujer'])
        sec = choice(secuences[sex].keys())
        images = ['%s-%s-%02d.png' %(sex, sec, x) for x in xrange(secuences[sex][sec])]

        Being.__init__(self, pos, screen_width, images, speed ,direction, speed_change)

class Alien(Being):
    def __init__(self, pos, screen_width, speed=1, direction=LEFT, speed_change=1, size='small'):
        sec = choice(secuences['alien'].keys())
        images = ['alien-%s-%02d.png' %(sec, x) for x in xrange(secuences['alien'][sec])]

        Being.__init__(self, pos, screen_width, images, speed, direction, speed_change)



def load_being(being, bodypart):
    return being+'-'+str(int(round(uniform(0,0))))+str(int(round(uniform(0,0))))+'.png'

 
def main():
    pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    sound = pygame.mixer.Sound(soundfile)
    sound2 = pygame.mixer.Sound(soundfile2)

    pygame.display.update()
    carril = (0,600)
    
    being = Robot( carril, 800, 240, RIGHT, 7, 'large')
    area = screen.get_rect()
    
    robots = pygame.sprite.Group()
    shoter = pygame.sprite.Group(Shoter())

    robots.add(being)
    
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    
    screen.fill([0, 0, 0])
    background = pygame.Surface([800, 600])
    background.fill([0, 0, 0])
    while pygame.event.poll().type != KEYDOWN:
        # Save time by only calling this once
         
        if pygame.mouse.get_pressed()[0]:
                sound.play() 
                shoted = pygame.sprite.spritecollide(shoter.sprites()[0], robots, True)
                if shoted:
                   robots.remove(shoted)
                   print "pummm"
                   sound2.play()
            #elif event.type == MOUSEBUTTONUP:
             #   fist.unpunch()
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0
        robots.update(time_passed_seconds)
        shoter.update()
        #fist.update()
        
        #se fija si llego al borde de la pantalla, en tal caso tira una moneda y vuelve a largar
        #el sprite por la izquierda o la derecha segun la moneda
        #old_direction = direction
        #if (being.rect.left >= area.width and being.direction == RIGHT) or (being.rect.left + being.rect.width <= 0 and being.direction == LEFT):
            #prob = int(round(uniform(1,2)))
            #if prob == 1:
                #being.set_pos((0,600))
                #being.set_direction(RIGHT)
            #else:
                #being.set_pos((800,600))
                #being.set_direction(LEFT)
        rectlist = robots.draw(screen)
        shoter.draw(screen)

        pygame.display.update()

        robots.clear(screen, background)
        shoter.clear(screen, background)
if __name__ == "__main__":
    main()

