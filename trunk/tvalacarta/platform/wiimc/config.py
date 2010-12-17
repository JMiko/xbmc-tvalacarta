# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os
import ConfigParser

DATA_PATH = os.getcwd()

configfile = ConfigParser.ConfigParser()
configfile.read('resources/pelisalacarta.conf')

def get_system_platform():
    return "wiimc"
    
def openSettings():
    return

def getSetting(name):
    try:
        return configfile.get("General",name)
    except:
        return ""

def setSetting(name,value):
    pass

def getLocalizedString(code):
    return code
    
def getPluginId():
    return "pelisalacarta"

def getLibraryPath():
    # FIXME: Una forma rapida de lanzar un error
    import noexiste
    return ""

def getTempFile(filename):
    # FIXME: Una forma rapida de lanzar un error 
    import noexiste
    return ""
