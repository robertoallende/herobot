import sys
import getopt
import data
import pygame
from random import uniform
from pygame.locals import *
#para probarlo hacer click sobre el objeto que da vueltas por ahi!!! y da vueltas como zaino!!!
#TODO: *animar los sprites,
#      *decidir que hacen cuadno se les dispara ( por ahora los humanos giran como el juego punch chimp)
#      *eleccion de imagenes de cuerpos pies y cabezas a azar
#      *agregar pies (pero estos giles se tiene que mover para dar la ilucion que caminan y no que levitan)
#      *comentar el codigo y arreglarlo un poco por que esta horrible!!
#      * y pensa!!!! que falta???
#      * como carajo le agregamos la sangre????
#      *como destruimos un sprite para que una vez muerto no joda mas??
#      *donde y que le devolvemos al gil que dispara


class Being:
    """ Clase madre que tiene como atributos tres sprites que serian la cabeza, cuerpo y piernas(no agregado)
        cada sprite provene de la clase bodypart 
        la idea de esta clase es que junte todos los sprites y le haga hacer todas su acciones en conjunto
        asi pareciera que es uno solo, parecido a un spritegroup pero sin algunas de sus limitaciones
    """
    def __init__(self,carril):
        #una interface, debe ser implementada por la clase hija
        #usar initbeing en la implementacion
        self.initBeing('body.png', 'head.png',carril)
        pass
    
    def update(self,direction):
        if not self.dizzy:
            self.rect = self.body.rect
            if direction == "right":
                self.move_right()
            else:
                self.move_left()
        else:
            self.kill()
    
    def setpos(self,newpos):
        self.body.setpos(newpos)
        self.head.setpos(self.headpos(newpos))
        self.rect = self.body.rect
        
    def initBeing(self,body_image,head_image,carril):
        self.body = Bodypart(carril,body_image)
        self.head = Bodypart((carril[0], carril[1] - self.body.rect.height), head_image)
        self.setpos(carril)
        self.size = (self.body.rect.height + self.head.rect.height, max(self.body.rect.width,self.head.rect.width))
        self.rect = self.body.rect
        self.dizzy = 0
        self.group = pygame.sprite.Group(self.body,self.head)
        
    def move_left(self):
        self.body.move_left()
        self.head.move_left()
    
    def move_right(self):
        self.body.move_right()
        self.head.move_right()
   
   
    def flip(self):
        self.body.image = pygame.transform.flip(self.body.image,1,0)
        self.head.image = pygame.transform.flip(self.head.image,1,0)
        
        
    def headpos(self, pos):
        return (pos[0] + self.body.rect.width/2 - self.head.rect.width/2,pos[1] - self.body.rect.height)
    
    def drawbeing(self):
        screen = pygame.display.get_surface()
        screen.blit(self.body.image, self.body.rect)
        screen.blit(self.head.image, self.head.rect)
        
    def is_hited(self,sprite):
        list = pygame.sprite.spritecollide(sprite, self.group, False)
        return not list == []
        
    def hited(self):
    #implementada por la clase hija, su accion depende de como reacciona al ser golpeado
        pass
    def kill(self):
        pass
        
    
class Bodypart(pygame.sprite.Sprite):
    def __init__(self, pos,image):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = data.load_image(image)
        self.setpos(pos)
        self.speed = 10
        #tomo el screen y sus medidas
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        
    def update(self,direction):
        pass
            
    def move_left(self):
        self.rect.left = self.rect.left -1
        
    def move_right(self):
        self.rect.left = self.rect.left +1
            
    def setpos(self,newpos):
        #self.rect.topleft= newpos
        self.rect.bottom = newpos[1]
        self.rect.left = newpos[0]

class Robot(Being):
    def __init__(self,carril, character = None):
        if not character:
            self.initBeing('body.png', 'head.png',carril)
    pass

class Human(Being):
    def __init__(self,carril, character = None):
        if not character:
            self.initBeing('body.png', 'head.png',carril)
    
    def hited(self):
        if not self.dizzy:
            self.dizzy = 1
            self.body.original = self.body.image
            self.head.original = self.head.image
            
    def kill(self):
        self._spin()
            
    def _spin(self):
        "spin the image"
        center_body = self.body.rect.center
        center_head = self.head.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.body.image = self.body.original
            self.head.image = self.head.original
        else:
            rotate = pygame.transform.rotate
            self.body.image = rotate(self.body.original, self.dizzy)
            self.head.image = rotate(self.head.original, self.dizzy)
        self.body.rect = self.body.image.get_rect(center=center_body)
        self.head.rect = self.head.image.get_rect(center=center_head)


        
def main():
    # ver http://www.sacredchao.net/~piman/writing/sprite-tutorial.shtml
    ##########################################################################################
    # Esta clase es simplemente Fist de punch chimp un poco modificada
    #para poder probar que le pasa a being cuando le pegas.
    class Fist(pygame.sprite.Sprite):
        """moves a clenched fist on the screen, following the mouse"""
        def __init__(self):
            pygame.sprite.Sprite.__init__(self) #call Sprite initializer
            self.image = pygame.Surface([15, 15])
            self.image.fill((255,0,255))

            # Make our top-left corner the passed-in location.
            self.rect = self.image.get_rect()
            self.punching = 0

        def update(self):
            "move the fist based on the mouse position"
            pos = pygame.mouse.get_pos()
            self.rect.midtop = pos
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
    being = Human(carril)
    direction = "right"
    area = screen.get_rect()
    angle = 30
    fist = Fist()
    while pygame.event.poll().type != KEYDOWN:
        screen.fill([0, 0, 0]) # blank the screen.
        # Save time by only calling this once
        time = pygame.time.get_ticks() 
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if being.is_hited(fist):
                    being.hited()
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()
        
        being.update(direction)
        fist.update()
        angle +=1
        #se fija si llego al borde de la pantalla, en tal caso tira una moneda y vuelve a largar
        #el sprite por la izquierda o la derecha segun la moneda
        old_direction = direction
        if (being.rect.left == area.width and direction == "right") or (being.rect.left + being.rect.width == 0 and direction == "left"):
            prob = int(round(uniform(1,2)))
            if prob == 1:
                being.setpos((0,600))
                direction = "right"
            else:
                being.setpos((800,600))
                direction = "left"
            if old_direction != direction:
                being.flip()
                
       # screen.blit(being.image, being.rect)
        being.drawbeing()
        pygame.display.update()

if __name__ == "__main__":
    main()

