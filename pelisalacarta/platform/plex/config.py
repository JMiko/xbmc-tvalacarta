# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from PMS import Prefs
from PMS import Locale
import os

def get_system_platform():
    return "osx"
    
def open_settings():
    return

def get_platform():
    return "plex"

def get_setting(name):
    valor = Prefs.Get(name)
    if type(valor).__name__=="bool":
        if valor:
            valor = "true"
        else:
            valor = "false"

    if name=="cache.dir":
        return ""

    if name=="download.enabled":
        return "false"
    
    if name=="cookies.dir":
        return os.getcwd()
    
    if name=="quality_youtube":
        return "8"
    return valor

def set_setting(name,value):
    Prefs.Set(name,value)

def get_localized_string(code):
    from PMS import Log
    Log("code=%d" % code)
    dev = Locale.LocalString(str(code))
    Log("dev=%s" % dev)
    return dev

def get_library_path():
    # FIXME: Una forma rapida de lanzar un error en Plex :) 
    import noexiste
    return ""

def get_temp_file(filename):
    # FIXME: Una forma rapida de lanzar un error en Plex :) 
    import noexiste
    return ""

def get_runtime_path():
    return os.getcwd()

def get_data_path():
    return os.getcwd()
