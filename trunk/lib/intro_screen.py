"""Intro Screen
"""
import sys
import getopt
import pygame
from string import split, join

#TODO: mejorar el efecto del texto, ver el fondo y otros FX, ver bien el tema de los parametros

SCREEN_SIZE = (800, 600)
#Parte string en frases de tamanio size(aunque no siempre)
def get_phrases(string, size):
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

#Esta clase implementa frases que van subiendo en la pantalla achicandose
#a medida que avanza
class Phrase(pygame.sprite.Sprite):
	def __init__(self, text, font, color, initial_pos, velocity):
		pygame.sprite.Sprite.__init__(self)
		self.text = text
		self.velocity = velocity
		self.render_text = font.render(text, True, color)
		self.image = self.render_text
		self.rect = list(initial_pos)
		self.width = self.render_text.get_width()
		self.height = self.render_text.get_height()
		self.alive = True
		
	def __str__(self):
		return self.text
	
	def update(self, time_passed):
		self.rect[1] -= time_passed*self.velocity

		#esta en la pantalla asi que hay que dibujarlo
		if 0 < self.rect[1]+self.height and self.rect[1] < SCREEN_SIZE[1]:
			self.width *= 0.994
			self.height *= 0.994
			self.rect[0] = (SCREEN_SIZE[0] - self.width)/2
			self.image = pygame.transform.scale(self.render_text, (int(self.width), int(self.height)))
		elif self.rect[1]+self.height <= 0:
			self.alive = False

#Deberia mostrar algo parecido a los titulos de star wars, pero falta tunearlo un poco con las velocidades
def presentation(text, font, screen):
	phrases = [Phrase(p, font, (255, 200, 0), SCREEN_SIZE, 0.05) for p in get_phrases(text, 30)]
	last_phrase = pygame.sprite.GroupSingle()
	screen_phrases = pygame.sprite.RenderUpdates()
	
	clock = pygame.time.Clock()
	last_phrase.add(phrases[0])
	screen_phrases.add(phrases.pop(0))
	while screen_phrases:
		if last_phrase:
			s  = last_phrase.sprite
			if phrases and s.rect[1]+s.height < SCREEN_SIZE[1] - 2:
				last_phrase.add(phrases[0])
				screen_phrases.add(phrases.pop(0))
		screen.fill((0,0,0))
		time_passed = clock.tick(30)
		screen_phrases.update(time_passed)
		screen_phrases.draw(screen)
		pygame.display.update()

phrase = 'It  is a period  of civil war. The Jedi Knights, once keepers of Peace and Justice, find themselves named Generals in the Republics Struggle against the Separtists. The Separtist army, under the leadership of the mysterious GENERAL GREIVOUS, seems to grow with each passing day. Meanwhile, the Supreme Chancellor PALPATINE continues to tighten his grip of power on the Republic, and becomes increasingly more isolated.Ordered by the JEDI COUNCIL to investigate the allegations made my COUNT DOOKU, ANAKIN SKYWALKER and OBI-WAN KENOBI find themselves in a deadly search for the Dark Lord of the Sith DARTH SIDIOUS, who must be defeated to stop the spread of Rebellion, and bring order back to the Galaxy...'

# metodo baston
def main():
	from pygame.locals import *
	from data import filepath

	font_filename = "GROOT___.TTF" #"Carnevalee Freakshow.ttf" #"pointy.ttf"  #"GROOT___.TTF"
	pygame.init()
	#font = pygame.font.SysFont("arial", 100)
	font = pygame.font.Font( filepath( font_filename ), 100)
	screen = pygame.display.set_mode(SCREEN_SIZE)
	presentation(phrase, font, screen)
	screen.update()
		
if __name__ == "__main__":
	main()

