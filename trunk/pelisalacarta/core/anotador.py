# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# modulo anotador de peliculas:
# dado el nombre de una pelicula, devuelve la nota usando un fichero de notas
#------------------------------------------------------------

# El formato del fichro de notas es <nombre-pelicula>\t<nota>\n...

import os
import string

from core import config

_char_simple = "aeiou"
_char_lower  = "�����"
_char_trans_simple = string.maketrans(_char_lower, _char_simple)
def normalize(v):
    v = v.lower()
    return v.translate(_char_trans_simple)


db = dict()

def builddict():
    try:
        f = open( os.path.join( config.get_data_path() , "notas.tab" , "r" ) )
    
        for line in f:
            l = line.split("\t")
    
            if (len(l) > 1):
                db[normalize(l[0])] = l[1].rstrip('\n') # to lower case y quitar acentos
                # print(normalize(l[0]+":"+db[l[0]]))
    
        f.close()
    except:
        pass

def getscore(name):
    try:
        res = db[normalize(name)]
    except:
        res = ""
    return res

builddict()

#print(getscore("zodiac: la maldicion (2007)"))







