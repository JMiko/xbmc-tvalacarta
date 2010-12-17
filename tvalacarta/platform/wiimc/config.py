# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os

import ConfigParser
configfile = ConfigParser.ConfigParser()
configfile.read('resources/pelisalacarta.conf')

from lib.elementtree import ElementTree as ET
translationstree = ET.parse( "resources/language/Spanish/strings.xml" )

DATA_PATH = os.getcwd()

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
    dev = translationstree.findtext( "//strings/string[@id='30025']" , "30025" )
    print dev
    return dev
    
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
