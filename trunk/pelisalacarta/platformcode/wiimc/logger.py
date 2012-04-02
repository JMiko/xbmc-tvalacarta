# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# logger for wiimc
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger_object=logging.getLogger("wiimc")

logger_object.info("Using WiiMC logger")

def info(texto):
    print texto

def debug(texto):
    print texto

def error(texto):
    print texto
