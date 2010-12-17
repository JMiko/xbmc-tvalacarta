# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración - modo desarrollo
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Creado por: 
# Jesús (tvalacarta@gmail.com)
# Jurrabi (jurrabi@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

print "Using DEVELOPER config"

import os
import ConfigParser

DATA_PATH = os.getcwd()
CONFIG_FILE_PATH = os.path.join(DATA_PATH,'settings.conf')
print "Config file path "+CONFIG_FILE_PATH

configfile = ConfigParser.SafeConfigParser()
configfile.read( CONFIG_FILE_PATH )

def get_system_platform():
    return "desktop"
    
def open_settings():
    return

def get_setting(name):
    try:
        return configfile.get("General",name)
    except:
        return ""
    
def set_setting(name,value):
    pass

def get_localized_string(code):
    return code
    
def get_library_path():
    # FIXME: Una forma rápida de lanzar un error
    import noexiste
    return ""

def get_temp_file(filename):
    # FIXME: Una forma rápida de lanzar un error 
    import noexiste
    return ""
