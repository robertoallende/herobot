# -*- coding: utf-8 -*-

FILESCORE='herobot.score'
import sys
import getopt
import pygame
from pygame.locals import *
from random import choice


class Score :
    
    def __init__( self ):
        self.records   = []
        self._filename = FILESCORE
        
        import pickle

        try:
            filehandler   = open( FILESCORE, 'rb' )
            obj           = pickle.load( filehandler )
            self.records  = obj.records
            filehandler.close()

        except IOError:
            pass


    def save ( self ) :
        """Guarda el objeto Score en un <filename>
        """
        import pickle

        try:
            filehandler = open( self._filename, 'wb' )
            pickle.dump( self, filehandler )
            filehandler.close()
        except:
            print "file <<"+ self._filename + ">> not found"


    def get_position( self, score ):
        """ regresa la posicion donde se va a insertar el nuevo score
            
            podria ser mejor, pero hlqp
        """
        rows  = len ( self.records )
        found = False
        index = 0
        while not found and rows > index :
            filed = self.records[index]

            if score > filed['score'] :
                found = True
            else :
                index += 1

        return index


    def sortScore( self, record1, record2 ):
        if record1['score'] != record2['score']:
            return cmp(record2['score'], record1['score'])
        else:
            return cmp(record1['date'], record2['date'])


    def add ( self, name, score ) :
        """Agrega un nuevo record

           Agrega la posicion donde fue insertado el score
        """
        import time
        import datetime
        record = {'score':score, 'date':time.mktime(datetime.datetime.now().timetuple()), 'name':name}
        self.records.append(record)
        self.records = sorted(self.records, cmp=self.sortScore)


    def get_best ( self ) :
        score = self.records[0]
        score['position'] = 1
        return score


    # mejorar hacer de nuevo
    def get_records_arround ( self, score, quantity ):
        from copy import deepcopy
        quantity  -= 1 
        position   = self.get_position ( score )
        long       = len( self.records )
        top        = position + quantity / 2 + quantity % 2
        bottom     = position - quantity / 2

        if bottom <= 0 :
            pos_bottom = 0
        else:
            pos_bottom = bottom

        if top >= long :
            pos_top = long
        else:
            pos_top = top

        #deberia mejorarlo pero bueno....
        if bottom < 0 and long - top >= -(bottom - position) :
            pos_top += -(bottom)
        elif bottom < 0 and long - top > 0 :
            pos_top += long - top

        if top > long and  bottom - (top - long) >= 0:
            pos_bottom -= top - long
        elif top > long :
            pos_bottom  = 0


        part_bottom = deepcopy( self.records[ pos_bottom : position ] )
        part_top    = deepcopy( self.records[ position : pos_top ] )

        idx = 0
        for i in range(pos_bottom, position) :
            part_bottom[idx]['position'] = i + 1
            idx += 1

        idx = 0
        for i in range(position, pos_top) :
            part_top[idx]['position'] = i + 2
            idx += 1

        return [part_bottom,part_top]


class HighScore(pygame.sprite.Sprite):
    
    def __init__( self, font, text, color, initial_pos ):
        pygame.sprite.Sprite.__init__(self)
        self.text        = text
        self.render_text = font.render(text, True, color)
        self.image       = self.render_text
        self.rect        = list(initial_pos)
        self.width       = self.render_text.get_width()
        self.height      = self.render_text.get_height()
        self.alive       = True


    def __str__(self):
        return self.text


    def update( self, font, text, color ):
        self.text        = text
        self.color       = color
        self.render_text = font.render(text, True, color)
        self.image       = self.render_text
        #self.rect        = list(initial_pos)
        self.width       = self.render_text.get_width()
        self.height      = self.render_text.get_height()
        self.alive       = True


def showScores( screen, score, reason_game_end ):

    from data import load_image, filepath

    gameScore = Score()

    FONT_NAME   = 'HEMIHEAD.TTF'
    FONT_SIZE   = 24
    font        = pygame.font.Font( filepath(FONT_NAME), FONT_SIZE)
    
    backgrounds = ['badgimp.png', 'venger.png']

    SCREEN_SIZE = (800,600)
    background, a = load_image( choice (backgrounds) )
    screen.blit(background, (0, 0))


    INITIAL_POS  = (130,110)
    TITLE_POS    = (80,110)
    RECORD_POS_X = 560
    color       = (20,  60, 240)
    colorUp      = (255,  0,   0)
    QUANTITY     = 10

    nickName        = []
    NIKNAME_MAX_LEN = 18

    
    # Nickname     * * * * * * * * *  Score
    # nueces.....  * * * * * * * * *  $0000000000
    TEXT_FORMAT   = '%(position)-3i - %(name)-'+ str(NIKNAME_MAX_LEN + 20) +'s '
    RECORD_FORMAT = '$%(score)-12d '
    INTERLINE     =  1.4


    listScores    = gameScore.get_records_arround(score, QUANTITY )
    position      = gameScore.get_position(score) + 1
    text_position = INITIAL_POS

    scoresSprites  = pygame.sprite.RenderUpdates()
    recordsSprites = pygame.sprite.RenderUpdates()
    scoreNewSprite = pygame.sprite.RenderUpdates()


    font.set_bold(True)

    hsc  = HighScore( font, "Game Over: "+reason_game_end, color, TITLE_POS )
    scoresSprites.add( hsc )
    text_position = ( text_position[0] , text_position[1] + hsc.height * 2 )

    text = "..:: Nickname ::.."
    hsc  = HighScore( font, text, color, text_position )
    scoresSprites.add( hsc )

    record = "..:: Score ::.."
    score_position = (RECORD_POS_X - 20, text_position[1])
    recordsSprites.add( HighScore( font, record, color, score_position ) )

    font.set_bold(False)

    text_position  = ( text_position[0] , text_position[1] + hsc.height * INTERLINE )
    score_position = (RECORD_POS_X, text_position[1])


    for item in listScores[0]:
        text  = TEXT_FORMAT % item
        hsc   = HighScore( font, text, color, text_position )
        scoresSprites.add( hsc )
        record = RECORD_FORMAT % item
        recordsSprites.add( HighScore( font, record, color, score_position ) )
        text_position  = ( text_position[0] , text_position[1] + hsc.height * INTERLINE )
        score_position = (RECORD_POS_X, text_position[1])


    item = { 'position':position, 'name':u'Insert your Nickname here', 'score':score}
    text = TEXT_FORMAT % item
    hsc = HighScore( font, text, colorUp, text_position )
    scoreNewSprite.add( hsc )
    record = RECORD_FORMAT % { 'score':score }
    recordsSprites.add( HighScore( font, record, colorUp, score_position ) )
    text_position  = ( text_position[0] , text_position[1] + hsc.height * INTERLINE )
    score_position = (RECORD_POS_X, text_position[1])

    for item in listScores[1]:
        text = TEXT_FORMAT % item
        hsc  = HighScore( font, text, color, text_position )
        scoresSprites.add( hsc )
        record = RECORD_FORMAT % item
        recordsSprites.add( HighScore( font, record, color, score_position ) )
        text_position  = ( text_position[0] , text_position[1] + hsc.height * INTERLINE )
        score_position = (RECORD_POS_X, text_position[1])

    scoresSprites.draw(screen)
    recordsSprites.draw(screen)
    scoreNewSprite.draw(screen)
    pygame.display.update()


    Enter = False
    while not Enter :
        event = pygame.event.wait()

        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:

            if event.key == K_RETURN and len(nickName) > 0:
                gameScore.add( u''.join(nickName), score )
                gameScore.save()
                Enter = True

            elif event.key in [K_DELETE, K_BACKSPACE]:
                if len(nickName) >= 1 :
                 nickName.pop()

            elif len(nickName) <= NIKNAME_MAX_LEN - 1:
                nickName.append(event.unicode)

            item   = { 'position':position, 'name':u''.join(nickName), 'score':score}
            text   = TEXT_FORMAT % item
            record = RECORD_FORMAT % item
            scoreNewSprite.clear( screen, background )
            scoreNewSprite.update( font, text, colorUp )
            recordsSprites.update( font, record, colorUp )
            scoreNewSprite.draw( screen )
            pygame.display.update()

            #print "key: %i, name %s, nickName %s" % (event.key, pygame.key.name(event.key), nickName )



########################################################################
# metodo baston·
def main():


    SCREEN_SIZE = (800,600)
    SCORE       = 106
    REASON_GAME_END = "You Louse becose nobody can't kill to wally"

    pygame.init()
    screen = pygame.display.set_mode( SCREEN_SIZE )

    #background, a = load_image( background_image_filename )

    showScores( screen, SCORE, REASON_GAME_END )
    print ">>>>>>>>>>>> Salio <<<<<<<<<<<<<<<<<<<"
    while pygame.event.poll().type != KEYDOWN: pygame.time.delay(10)

########################################################################


if __name__ == "__main__":
    main()

