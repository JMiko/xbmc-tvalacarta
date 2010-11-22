# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración multiplataforma
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

import os

# TODO ¿Para que hacíamos esto?
PLATFORM = "Non detected"
PLUGIN_ID = "plugin.video.tvalacarta"
DHARMA = False
DATA_PATH = os.getcwd()

# Intenta averiguar la plataforma de entre una de las siguientes:

# boxee
# server (wiimc, dlna)
# xbmc
# xbmcdharma
# plex
# mediaportal
# windowsmediacenter
# developer

# XBMC Dharma
try:
    print "Testing xbmc dharma..."
    import xbmcaddon
    import xbmc
    PLATFORM = "xbmcdharma"
    PLUGIN_ID = "plugin.video.tvalacarta"
    DHARMA = True
    DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % PLUGIN_ID)
    __settings__ = xbmcaddon.Addon(id=PLUGIN_ID)
    __language__ = __settings__.getLocalizedString
except ImportError:
    # XBMC
    try:
        print "Testing xbmc..."
        import xbmc
        PLATFORM = "xbmc"
        PLUGIN_ID = "tvalacarta"
        DHARMA = False
        DATA_PATH = os.getcwd()
    except ImportError:
        print "Platform=DEVELOPER"
        # Eclipse
        PLATFORM = "developer"
        PLUGIN_ID = "tvalacarta"
        DHARMA = False
        DATA_PATH = os.getcwd()

# En PLATFORM debería estar el módulo a importar
exec "import platform."+PLATFORM+".config as platformconfig"

def get_platform():
    return PLATFORM

def get_system_platform():
    return platformconfig.get_system_platform()

def open_settings():
    return platformconfig.open_settings()

def get_setting(name):
    return platformconfig.get_setting(name)

def set_setting(name,value):
    platformconfig.set_setting(name,value)

def get_localized_string(code):
    return platformconfig.get_localized_string(code)

def get_plugin_id():
    return PLUGIN_ID

def get_library_path():
    return platformconfig.get_library_path()

def get_temp_file(filename):
    return platformconfig.get_temp_file()
