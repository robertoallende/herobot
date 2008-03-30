# -*- coding: utf-8 -*-

FILESCORE='herobot.score'


class HighScores :
    
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


    def add_score ( self, score, name ) :
        """Agrega un nuevo record

        """
        import time
        import datetime

        #import pdb; pdb.set_trace()
        record   = {'score':score, 'date':time.mktime(datetime.datetime.now().timetuple()), 'name':name}
        rows = len ( self.records )
        insert   = False
        index    = 0
        while not insert and rows > index :
            filed = self.records[index]

            if record['score'] > filed['score'] :
                self.records.insert( index, record )
                insert = True

            index +=1

        #si llego al final de la lista y este es el peor puntaje
        if not insert :
            self.records.append( record )


