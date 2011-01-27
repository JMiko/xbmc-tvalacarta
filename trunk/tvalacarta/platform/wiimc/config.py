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

print "[config.py] wiimc config"

import os,re
import ConfigParser

def get_system_platform():
    return "wiimc"
    
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
    cadenas = re.findall('<string id="%d">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        return cadenas[0]
    else:
        return "%d" % code
    
def get_library_path():
    # FIXME: Una forma rápida de lanzar un error
    import noexiste
    return ""

def get_temp_file(filename):
    # FIXME: Una forma rápida de lanzar un error 
    import noexiste
    return ""

def get_data_path():
    return os.path.join( os.path.expanduser("~") , ".pelisalacarta" )

def get_runtime_path():
    return os.getcwd()

# Directorio de usuario
if not os.path.exists(get_data_path()):
    os.mkdir(get_data_path())

# Fichero de configuración
configfilepath = os.path.join( get_data_path() , 'pelisalacarta.conf')
if not os.path.exists(configfilepath):
    import shutil
    shutil.copyfile( os.path.join(get_runtime_path(),"resources","settings.conf") , configfilepath )

configfile = ConfigParser.ConfigParser()
configfile.read( configfilepath )

# Literales
TRANSLATION_FILE_PATH = os.path.join(get_runtime_path(),"resources","language","Spanish","strings.xml")
translationsfile = open(TRANSLATION_FILE_PATH,"r")
translations = translationsfile.read()
translationsfile.close()

print "[config.py] runtime path = "+get_runtime_path()
print "[config.py] data path = "+get_data_path()
print "[config.py] language file path "+TRANSLATION_FILE_PATH
print "[config.py] config file "+configfilepath
