# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración - xbmc dharma
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

import sys
import os

import xbmcaddon
import xbmc

PLUGIN_ID = "plugin.video.tvalacarta"

__settings__ = xbmcaddon.Addon(id=PLUGIN_ID)
__language__ = __settings__.getLocalizedString

def get_system_platform():
    """ fonction: pour recuperer la platform que xbmc tourne """
    platform = "unknown"
    if xbmc.getCondVisibility( "system.platform.linux" ):
        platform = "linux"
    elif xbmc.getCondVisibility( "system.platform.xbox" ):
        platform = "xbox"
    elif xbmc.getCondVisibility( "system.platform.windows" ):
        platform = "windows"
    elif xbmc.getCondVisibility( "system.platform.osx" ):
        platform = "osx"
    return platform
    
def open_settings():
    __settings__.openSettings()

def get_setting(name):
    return __settings__.getSetting( name )

def set_setting(name,value):
    __settings__.setSetting( name,value ) # this will return "foo" setting value

def get_localized_string(code):
    dev = __language__(code)

    try:
        dev = dev.encode ("utf-8") #This only aplies to unicode strings. The rest stay as they are.
    except:
        pass
    
    return dev

def get_library_path():
    return xbmc.translatePath("special://profile/addon_data/%s/library" % PLUGIN_ID)

def get_temp_file(filename):
    return xbmc.translatePath( os.path.join( "special://temp/", filename ))
