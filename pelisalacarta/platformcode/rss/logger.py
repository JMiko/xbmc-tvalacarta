# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# logger for wiimc
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

# TODO: (3.1) Log en fichero
print "Using RSS logger"

def info(texto):
    if "[scrapertools.py]" in texto: pass
    else: print texto

def debug(texto):
    if "[scrapertools.py]" in texto: pass
    else: print texto

def error(texto):
    if "[scrapertools.py]" in texto: pass
    else: print texto
