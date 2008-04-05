"""Intro Screen
"""
import sys
import getopt
import pygame
from pygame.locals import *
from string import split, join

#TODO: mejorar el efecto del texto, ver el fondo y otros FX, ver bien el tema de los parametros

SCREEN_SIZE = (800, 600)
#Parte string en frases de tamanio size(aunque no siempre)
def get_phrases(string, size=30):
    words = split(string)
    result = []
    while words:
        actual_size = 0
        actual_word = []
        while words and actual_size+len(words[0]) < size:
            actual_size += len(words[0])+1
            actual_word.append(words.pop(0))
        actual_word = join(actual_word)
        if words:
            i = 1
            while len(actual_word) != size:
                actual_word = actual_word.replace(' '*i, ' '*(i+1),  size - len(actual_word))
                i += 1
        result.append(actual_word)
    return result

class Board:
    def __init__(self, game, pos):
        pass


def presentation(text, font, screen, speed=0.05):
    draw_text(get_phrases(text), font, screen, speed=0.05)

phrase = 'It  is a period  of civil war. The Jedi Knights, once keepers of Peace and Justice, find themselves named Generals in the Republics Struggle against the Separtists. The Separtist army, under the leadership of the mysterious GENERAL GREIVOUS, seems to grow with each passing day. Meanwhile, the Supreme Chancellor PALPATINE continues to tighten his grip of power on the Republic, and becomes increasingly more isolated.Ordered by the JEDI COUNCIL to investigate the allegations made my COUNT DOOKU, ANAKIN SKYWALKER and OBI-WAN KENOBI find themselves in a deadly search for the Dark Lord of the Sith DARTH SIDIOUS, who must be defeated to stop the spread of Rebellion, and bring order back to the Galaxy...'

###################################Refactoring#######################################
# Objecto que se comienza en initial_pos y se va elevando, obj debe 
# ser un sprite o un texto renderiado
class ObjectRaise(pygame.sprite.Sprite):
    def __init__(self, obj, initial_pos, speed, obj_reduce=True, obj_center=True):
        pygame.sprite.Sprite.__init__(self)
        self.obj = obj
        self.speed = speed
        #reemplazado por obj #self.render_text = font.render(text, True, color)
        self.image = self.obj
        self.rect = list(initial_pos)
        
        if hasattr(self.obj, 'width'):
            pass
        elif hasattr(self.obj, 'get_width'):
            self.width = self.obj.get_width()
            self.height = self.obj.get_height()
        else:
            raise Error #fijarse de dar un error apropiado
        self.obj_reduce = obj_reduce
        self.obj_center = obj_center
        self.alive = True
        
    def __str__(self):
        return self.obj
    
    def update(self, time_passed):
        self.rect[1] -= time_passed*self.speed

        #esta en la pantalla asi que hay que dibujarlo
        if 0 < self.rect[1]+self.height and self.rect[1] < SCREEN_SIZE[1]:
            if self.obj_reduce:
                self.width *= 0.994
                self.height *= 0.994
            if self.obj_center:
                self.rect[0] = (SCREEN_SIZE[0] - self.width)/2
            self.image = pygame.transform.scale(self.obj, (int(self.width), int(self.height)))
        elif self.rect[1]+self.height <= 0:
            for grp in self.groups():
                grp.remove(self)


class Phrase(ObjectRaise):
    def __init__(self, text, font, color, initial_pos, speed, text_reduce=True, text_center=True):
        self.text = text
        ObjectRaise.__init__(self, font.render(text, True, color), initial_pos, speed, text_reduce, text_center)


# Eleva un conjunto de Obj_raise
class SetRaise(pygame.sprite.Sprite): #Sprite or object???
    #initial pos es el pto del eje de las y donde "salen", los sprites
    def __init__(self, objs, initial_pos):
        self.objs = objs
        self.initial_pos = initial_pos
        self.last_obj = pygame.sprite.GroupSingle()
        self.screen_objs = pygame.sprite.RenderUpdates()
    
        if self.objs:
            self.last_obj.add(self.objs[0])
            self.screen_objs.add(self.objs.pop(0))
    
    def update(self, time_passed):
        if self.last_obj:
            obj  = self.last_obj.sprite
            if self.objs and obj.rect[1]+obj.height < self.initial_pos - 2: #cambiar esta parte
                self.last_obj.add(self.objs[0])
                self.screen_objs.add(self.objs.pop(0))
        self.screen_objs.update(time_passed)

    def draw(self, screen):
        return self.screen_objs.draw(screen)

    def clear(self, screen, background):
        self.screen_objs.clear(screen, background)


def draw_text(phrases, font, screen, speed=0.05):
    phrases = [Phrase(p, font, (255, 200, 0), (0, SCREEN_SIZE[1]), speed) for p in phrases]
    phrases = SetRaise(phrases, SCREEN_SIZE[1])
    clock = pygame.time.Clock()
    
    background = pygame.Surface(SCREEN_SIZE)
    background.fill([0, 0, 0])
    while pygame.event.poll().type != KEYDOWN:
        #screen.fill((0,0,0))
        time_passed = clock.tick(30)
        phrases.update(time_passed)
        rectlist = phrases.draw(screen)
        pygame.display.update(rectlist)
        phrases.clear(screen, background)
    

#####################################################################################
# metodo baston
def main():
    from pygame.locals import *
    from data import filepath

    font_filename = "HEMIHEAD.TTF" #"Carnevalee Freakshow.ttf" #"pointy.ttf"  #"GROOT___.TTF"
    pygame.init()
    #font = pygame.font.SysFont("arial", 100)
    font = pygame.font.Font( filepath( font_filename ), 100)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    presentation(phrase, font, screen)
        
if __name__ == "__main__":
    main()
