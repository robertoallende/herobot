import data
import pygame

    # Esta clase es simplemente Fist de punch chimp un poco modificada
    #para poder probar que le pasa a being cuando le pegas.
class Shoter(pygame.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        #self.image = pygame.Surface([15, 15])
        #self.image.fill((255,0,255))
        self.image, self.rect = data.load_image('crosshair.png')

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()

    def update(self, *args):
        "move the fist based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.left, self.rect.bottom = pos[0] - self.rect.width/2, pos[1] + self.rect.height/2

