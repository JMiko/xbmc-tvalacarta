# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración multiplataforma
#------------------------------------------------------------
# tvalacarta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
# Creado por: Jesús (tvalacarta@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

PLATFORM = "Non detected"
PLUGIN_ID = "plugin.video.tvalacarta"

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
    import xbmcaddon
    import xbmc
    PLATFORM = "xbmcdharma"
    PLUGIN_ID = "plugin.video.tvalacarta"
except ImportError:
    # XBMC
    try:
        import xbmc
        PLATFORM = "xbmc"
        PLUGIN_ID = "tvalacarta"
    except ImportError:
        print "Platform=DEVELOPER"
        # Eclipse
        PLATFORM = "developer"
        PLUGIN_ID = "tvalacarta"

# En PLATFORM debería estar el módulo a importar
exec "import platform."+PLATFORM+".config as platformconfig"

def get_platform():
    return PLATFORM

def get_system_platform():
    return platformconfig.get_system_platform()

def open_settings():
    return platformconfig.open_settings()

def get_setting(name):
    # La cache recibe un valor por defecto la primera vez que se solicita
    '''
    if name=="cache.dir" and dev=="":
        dev = xbmc.translatePath("special://temp/%s.cache" % PLUGIN_ID)
        if not os.path.exists(dev):
            os.mkdir(dev)
        set_setting(name,dev)
    '''

    if name=="download.enabled" and dev=="":
        try:
            from core import descargadoslist
            dev="true"
        except:
            dev="false"
    
    elif name=="plugin.name" and dev=="":
        dev="tvalacarta"
    
    elif name=="cookies.dir":
        dev=get_data_path()
    elif name=="cache.mode":
        dev="2"
    else:
        dev=platformconfig.get_setting(name)

    return dev

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

def get_runtime_path():
    return platformconfig.get_runtime_path()

def get_data_path():
    return platformconfig.get_data_path()
