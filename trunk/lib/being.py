import sys
import getopt
import data
import pygame
from random import uniform
from pygame.locals import *

RIGHT = 1
LEFT = -1
ROBOT_IMAGES = 2
#para probarlo hacer click sobre el objeto que da vueltas por ahi!!! y da vueltas como zaino!!!
#TODO: *decidir que hacen cuadno se les dispara ( por ahora los humanos giran como el juego punch chimp)
#      *comentar el codigo 
#      * como carajo le agregamos la sangre????
#      *como destruimos un sprite para que una vez muerto no joda mas??
#      *donde y que le devolvemos al gil que dispara


class Being(pygame.sprite.Sprite):
    def __init__(self, pos, images, speed=1, direction=LEFT, speed_change=1):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect =  data.load_image(images[0])
        self.actual_img = 0
        self.images = [data.load_image(img)[0] for img in images]
        self.set_pos(pos)
        self.speed = speed
        self.speed_change = speed_change
        self.alive = True
        self.direction = direction
        self.last_img_change  = 0
        if direction == RIGHT:
            self.images = [pygame.transform.flip(img,1,0) for img in self.images]
            self.image = self.images[0]
        #tomo el screen y sus medidas
       
    def update(self,time_passed):
        if self.alive:
            if  self.speed_change < self.last_img_change:
                self.actual_img = (self.actual_img  + 1) % len(self.images)
                self.image = self.images[self.actual_img]
                self.last_img_change = 0
            self.last_img_change += 1
            self.rect.left = self.rect.left + self.direction*time_passed*self.speed
        else:
                pass

    def set_direction(self, direction):
        if self.direction != direction:
            self.direction = direction
            self.images = [pygame.transform.flip(img,1,0) for img in self.images]

    def set_pos(self,newpos):
        self.rect.bottom = newpos[1]
        self.rect.left = newpos[0]

 
class Robot(Being):
    def __init__(self, pos, speed=1, direction=LEFT, speed_change=1):
        images = ['human-'+'%02d' %(x) + '.png' for x in xrange(ROBOT_IMAGES)]
        Being.__init__(self, pos, images, speed, direction,speed_change)


class Human(Being):
    def __init__(self, pos, images, speed=1, direction=LEFT, speed_change=1):
        Being.__init__(self, pos, images, speed ,direction, speed_change)

class Alien(Being):
    def __init__(self, pos, images, speed=1, direction=LEFT, speed_change=1):
        Being.__init__(self, pos, images, speed, direction, speed_change)



def load_being(being, bodypart):
    return being+'-'+str(int(round(uniform(0,0))))+str(int(round(uniform(0,0))))+'.png'

        
def main():
    # ver http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml
    ##########################################################################################
    # Esta clase es simplemente Fist de punch chimp un poco modificada
    #para poder probar que le pasa a being cuando le pegas.
    class Fist(pygame.sprite.Sprite):
        """moves a clenched fist on the screen, following the mouse"""
        def __init__(self):
            pygame.sprite.Sprite.__init__(self) #call Sprite initializer
            #self.image = pygame.Surface([15, 15])
            #self.image.fill((255,0,255))
            self.image, self.rect = data.load_image('crosshair.png')

            # Make our top-left corner the passed-in location.
            self.rect = self.image.get_rect()
            self.punching = 0

        def update(self, *args):
            "move the fist based on the mouse position"
            pos = pygame.mouse.get_pos()
            self.rect.left, self.rect.bottom = pos[0] - self.rect.width/2, pos[1] + self.rect.height/2
            if self.punching:
                self.rect.move_ip(5, 10)
    
######NO USAMOS ESTA FUNCION, YA QUE SE USA UNA DEFINIDA POR BEING!!! PARA QUE CALCULE A TODOS LOS SPRITES DE LA CASE BEING
        def punch(self, target):
            "returns true if the fist collides with the target"
            if not self.punching:
                self.punching = 1
                hitbox = self.rect.inflate(-5, -5)
                return hitbox.colliderect(target.rect)
        def unpunch(self):
            "called to pull the fist back"
            self.punching = 0
   #fin clase chip #####################################################################
        
        
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    pygame.display.update()
    carril = (0,600)
    being = Robot( carril, 0.4, RIGHT, 7)
    direction = "right"
    area = screen.get_rect()
    all = pygame.sprite.RenderUpdates()
    robots = pygame.sprite.Group()
    all.add(being)
    robots.add(being)
    fist = Fist()
    all.add(fist)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    while pygame.event.poll().type != KEYDOWN:
        screen.fill([0, 0, 0]) # blank the screen.
        # Save time by only calling this once
        time = pygame.time.get_ticks() 
        if pygame.mouse.get_pressed()[0]:
        #for event in pygame.event.get():
            #if event.type == MOUSEBUTTONDOWN:
                shoted = pygame.sprite.spritecollide(fist, robots, True)
                if shoted:
                   all.remove(shoted)
                   print "pummm"
            #elif event.type == MOUSEBUTTONUP:
             #   fist.unpunch()
        time_passed = clock.tick(30)
        all.update(time_passed)
        #fist.update()
        
        #se fija si llego al borde de la pantalla, en tal caso tira una moneda y vuelve a largar
        #el sprite por la izquierda o la derecha segun la moneda
        #old_direction = direction
        if (being.rect.left >= area.width and being.direction == RIGHT) or (being.rect.left + being.rect.width <= 0 and being.direction == LEFT):
            prob = int(round(uniform(1,2)))
            if prob == 1:
                being.set_pos((0,600))
                being.set_direction(RIGHT)
            else:
                being.set_pos((800,600))
                being.set_direction(LEFT)
                
       # screen.blit(being.image, being.rect)
        all.draw(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()

