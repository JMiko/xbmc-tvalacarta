# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Gestión de parámetros de configuración - WiiMC
#-------------------------------------------------------------------------------
# tvalacarta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#-------------------------------------------------------------------------------
# Creado por: 
# Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#-------------------------------------------------------------------------------
# Historial de cambios:
# 18-12-2010 Implementa lector cadenas internacionales con strings.xml de xbmc
# 20-01-2010 Fichero de configuración en el directorio de usuario
#-------------------------------------------------------------------------------
import os,re
import ConfigParser

PLUGIN_NAME="tvalacarta"

import logging.config
import logging
logging.config.fileConfig("logging.conf")
logger=logging.getLogger("wiimc")

logger.info("wiimc config 3.3.2")

def get_system_platform():
    return "wiimc"
    
def open_settings():
    return

def get_setting(name):
    dev = ""
    try:
        if name in overrides:
            dev = overrides[name]
        else:
            dev = configfile.get("General",name)
    except:
        dev = ""
    
    # Las rutas por defecto devuelven el directorio de datos
    if dev=="" and name in ["LIBRARY_PATH","LIBRARY_BD","downloadpath","downloadlistpath","bookmarkpath"]:
        dev = get_data_path()

    return dev
    
def set_setting(name,value):
    #print "set_setting",name,value
    overrides[name]=value

def get_localized_string(code):
    cadenas = re.findall('<string id="%d">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        return cadenas[0]
    else:
        return "%d" % code
    
def get_library_path():
    return os.path.join(get_data_path(),"library")

def get_temp_file(filename):
    return os.path.join(get_data_path(),filename)

def get_data_path():
    return os.path.join( os.path.expanduser("~") , "."+PLUGIN_NAME )

def get_runtime_path():
    return os.getcwd()

# Directorio de usuario
if not os.path.exists(get_data_path()):
    os.mkdir(get_data_path())

# Fichero de configuración
configfilepath = os.path.join( get_data_path() , PLUGIN_NAME+'.conf')
if not os.path.exists(configfilepath):
    import shutil
    shutil.copyfile( os.path.join(get_runtime_path(),"resources","settings.conf") , configfilepath )

configfile = ConfigParser.ConfigParser()
configfile.read( configfilepath )

overrides = dict()

# Literales
TRANSLATION_FILE_PATH = os.path.join(get_runtime_path(),"resources","language","Spanish","strings.xml")
translationsfile = open(TRANSLATION_FILE_PATH,"r")
translations = translationsfile.read()
translationsfile.close()

logger.info("runtime path = "+get_runtime_path())
logger.info("data path = "+get_data_path())
logger.info("language file path "+TRANSLATION_FILE_PATH)
logger.info("config file "+configfilepath)
logger.info("temp path = "+get_temp_file("test"))
