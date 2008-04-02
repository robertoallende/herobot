import sys
import getopt
import data
import pygame
from random import uniform
from pygame.locals import *
#para probarlo hacer click sobre el objeto que da vueltas por ahi!!! y da vueltas como zaino!!!
#TODO: *decidir que hacen cuadno se les dispara ( por ahora los humanos giran como el juego punch chimp)
#      *comentar el codigo 
#      * como carajo le agregamos la sangre????
#      *como destruimos un sprite para que una vez muerto no joda mas??
#      *donde y que le devolvemos al gil que dispara


class Bodypart(pygame.sprite.Sprite):
    def __init__(self, pos,image,imageb):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = data.load_image(image)
        self.imageb, self.rectb = data.load_image(imageb)
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
        self.rect.bottom = newpos[1]
        self.rect.left = newpos[0]
        
    def flip_images(self):
        self.image = pygame.transform.flip(self.image,1,0)
        self.imageb = pygame.transform.flip(self.imageb, 1,0)
        
    def draw(self):
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)
    
        
class AnimatedPart(Bodypart):
    def __init__(self,pos, image1,image2,image1b,image2b):
        Bodypart.__init__(self,pos,image1,image1b)
        self.image2, self.tirar = data.load_image(image2)
        self.image2b, self.tirarb = data.load_image(image2b)
        self.img_num = int(round(uniform(0,1)))
        
    def draw(self):
        screen = pygame.display.get_surface()
        if self.img_num == 1: screen.blit(self.image, self.rect); self.img_num = 1 - self.img_num
        elif self.img_num == 0: screen.blit(self.image2, self.rect); self.img_num = 1 - self.img_num
        else:  screen.blit(self.image2, self.rect)
        
    def flip_images(self):
        if self.img_num:
            self.image = pygame.transform.flip(self.image,1,0)
            self.imageb = pygame.transform.flip(self.imageb,1,0)
        else:
            self.image2 = pygame.transform.flip(self.image2,1,0)
            self.image2b = pygame.transform.flip(self.image2b,1,0)
    
    def killed_state(self):
        self.img_num = 2



class Being:
    """ Clase madre que tiene como atributos tres sprites que serian la cabeza, cuerpo y piernas(no agregado)
        cada sprite provene de la clase bodypart 
        la idea de esta clase es que junte todos los sprites y le haga hacer todas su acciones en conjunto
        asi pareciera que es uno solo, parecido a un spritegroup pero sin algunas de sus limitaciones
    """
    def __init__(self,kind,carril):
        body = load_being(kind,'body')
        bodyb = load_being(kind, 'bodyb')
        head = load_being(kind,'head')
        headb = load_being(kind,'headb')
        legc = load_being(kind, 'legsc')
        legcb = load_being(kind, 'legscb')
        lego = load_being(kind, 'legso')
        legob = load_being(kind, 'legsob')
        armc = load_being(kind, 'armsc')
        armcb = load_being(kind, 'armscb')
        armo = load_being(kind, 'armso')
        armob = load_being(kind, 'armsob')
        self.legs = AnimatedPart(carril, legc, lego,legcb,legob)
        self.body = Bodypart((carril[0], carril[1] - self.legs.rect.height),body,bodyb)
        self.head = Bodypart((carril[0], carril[1] - self.body.rect.height), head,headb)
        self.arms = AnimatedPart(carril,armc, armo,armcb,armob)
        self.setpos(carril)
        self.size = (self.body.rect.height + self.head.rect.height, max(self.body.rect.width,self.head.rect.width))
        self.rect = self.body.rect
        self.dizzy = 0
        self.group = pygame.sprite.Group(self.body,self.head,self.arms,self.legs)
    
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
        self.legs.setpos(newpos)
        self.body.setpos(self.bodypos(newpos))
        self.head.setpos(self.headpos(newpos))
        self.arms.setpos(self.armspos(newpos))
        self.rect = self.body.rect
        
    def move_left(self):
        self.legs.move_left()
        self.body.move_left()
        self.head.move_left()
        self.arms.move_left()
    
    def move_right(self):
        self.legs.move_right()
        self.body.move_right()
        self.head.move_right()
        self.arms.move_right()
   
   
    def flip(self):
        self.body.flip_images()
        self.head.flip_images()
        self.legs.flip_images()
        self.arms.flip_images()
        
        
        
    def headpos(self, pos):
        return (pos[0] + self.legs.rect.width/2 - self.head.rect.width/2,pos[1] - self.body.rect.height - self.legs.rect.height)
    
    def bodypos(self,pos):
        return (pos[0] + self.legs.rect.width/2 - self.body.rect.width/2, pos[1] - self.legs.rect.height)
    
    def armspos(self,pos):
        return (self.body.rect.left + self.arms.rect.width, self.body.rect.bottom - self.body.rect.height +self.arms.rect.height )
    
    def drawbeing(self):
        screen = pygame.display.get_surface()
        screen.blit(self.body.image, self.body.rect)
        screen.blit(self.head.image, self.head.rect)
        self.legs.draw()
        self.arms.draw()
        
    def is_hited(self,sprite):
        list = pygame.sprite.spritecollide(sprite, self.group, False)
        return not list == []
        
                
    def hited(self):
        if not self.dizzy:
            self.dizzy = 1
            self.legs.killed_state()
            self.arms.killed_state()
            self.body.original = self.body.image
            self.head.original = self.head.image
            self.legs.original = self.legs.image
            self.legs.original2 = self.legs.image2
            self.arms.original = self.arms.image
            self.arms.original2 =self.arms.image2
            
    def kill(self):
        self._spin()
            
    def _spin(self):
        "spin the image"
        center_body = self.body.rect.center
        center_head = self.head.rect.center
        self.dizzy += 1
        if self.dizzy >= 360:
            self.dizzy = 0
            ###############quitar esto########
            self.legs.img_num = 0
            self.arms.img_num = 0
            ################################
            self.body.image = self.body.original
            self.head.image = self.head.original
            self.legs.image = self.legs.original
            self.legs.image2 = self.legs.original2
            self.arms.image = self.arms.original
            self.arms.image2 = self.arms.original2
        else:
            self.body.image = self.body.imageb
            self.head.image = self.head.imageb
            self.legs.image = self.legs.imageb
            self.legs.image2 = self.legs.image2b
            self.arms.image = self.arms.imageb
            self.arms.image2 = self.arms.image2b
             
        self.body.rect = self.body.image.get_rect(center=center_body)
        self.head.rect = self.head.image.get_rect(center=center_head)
        
    
class Robot(Being):
    def __init__(self,carril, character = None):
        if not character:
            Being.__init__(self,'robot',carril)


class Human(Being):
    def __init__(self,carril, character = None):
        if not character:
            Being.__init__(self,'human',carril)

class Alien(Being):
    def __init__(self,carril, character = None):
        if not character:
            Being.__init__(self,'alien',carril)



def load_being(being, bodypart):
    return being+'-'+str(int(round(uniform(0,0))))+str(int(round(uniform(0,0))))+'-'+bodypart+'.png'

        
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

