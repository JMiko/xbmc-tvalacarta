# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Logger
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
from PMS import Log

def info(texto):
    try:
        texto = unicode(texto,"utf-8")
    except:
        try:
            texto = unicode(texto,"iso-8859-1")
        except:
            pass

    Log(texto)

def debug(texto):
    try:
        texto = unicode(texto,"utf-8")
    except:
        try:
            texto = unicode(texto,"iso-8859-1")
        except:
            pass

    Log(texto)

def error(texto):
    try:
        texto = unicode(texto,"utf-8")
    except:
        try:
            texto = unicode(texto,"iso-8859-1")
        except:
            pass

    Log(texto)
