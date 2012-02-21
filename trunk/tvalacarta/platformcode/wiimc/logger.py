# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# logger for wiimc
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

# TODO: (3.1) Log en fichero
import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger_object=logging.getLogger("wiimc")

 
logger_object.info("Using WiiMC logger")

def info(texto):
    logger_object.info(texto)

def debug(texto):
    logger_object.debug(texto)

def error(texto):
    logger_object.error(texto)
