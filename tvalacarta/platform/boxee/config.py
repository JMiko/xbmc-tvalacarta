# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración - xbmc
#------------------------------------------------------------
# tvalacarta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

print "[config.py] boxee config"

import os,re

import xbmc
import mc

def get_system_platform():
    return "boxee"
    
def open_settings():
    return

def get_setting(name):
    if name=="cache.dir":
        return get_temp_file("cache")
    elif name=="cache.mode":
        return "2"
    elif name=="debug":
        return "true"
    elif name=="thumbnail_type":
        return "0"
    elif name=="default_action":
        return "0"
    elif name=="download.enabled":
        return "false"
    elif name=="subtitulo":
        return "false"
    elif name=="player_type":
        return "0"
    else:
        return ""

def set_setting(name,value):
    return

def get_localized_string(code):
    cadenas = re.findall('<string id="%d">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        return cadenas[0]
    else:
        return "%d" % code
    
def get_library_path():
    return ""

def get_temp_file(filename):
    return os.path.join( mc.GetTempDir(), filename )

def get_runtime_path():
    app = mc.GetApp();
    return app.GetAppDir()

def get_data_path():
    return os.getcwd()

def get_boxee_plugin_path():
    return os.path.abspath(os.path.join(get_runtime_path(),"..","..","plugins","video","info.mimediacenter.tvalacarta"))

# Literales
TRANSLATION_FILE_PATH = os.path.join(get_runtime_path(),"resources","language","Spanish","strings.xml")
translationsfile = open(TRANSLATION_FILE_PATH,"r")
translations = translationsfile.read()
translationsfile.close()

print "[config.py] runtime path = "+get_runtime_path()
print "[config.py] data path = "+get_data_path()
print "[config.py] language file path "+TRANSLATION_FILE_PATH
print "[config.py] temp path = "+get_temp_file("test")
print "[config.py] plugin path = "+get_boxee_plugin_path()

if not os.path.exists( get_boxee_plugin_path() ):
    import shutil
    shutil.copytree( get_runtime_path() , get_boxee_plugin_path() )
