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

PLATFORM = ""

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
    import mc
    PLATFORM="boxee"
except:
    try:
        import xbmcaddon
        PLATFORM = "xbmcdharma"
    except ImportError:
        # XBMC
        try:
            import xbmc
            PLATFORM = "xbmc"
        except ImportError:
            print "Platform=DEVELOPER"
            # Eclipse
            PLATFORM = "developer"

def force_platform(platform):
    global PLATFORM
    
    PLATFORM = platform
    # En PLATFORM debería estar el módulo a importar
    exec "import platform."+PLATFORM+".config as platformconfig"

def get_platform():
    return PLATFORM

def get_system_platform():
    exec "import platform."+PLATFORM+".config as platformconfig"
    return platformconfig.get_system_platform()

def open_settings():
    exec "import platform."+PLATFORM+".config as platformconfig"
    return platformconfig.open_settings()

def get_setting(name):
    exec "import platform."+PLATFORM+".config as platformconfig"
    # La cache recibe un valor por defecto la primera vez que se solicita

    dev=platformconfig.get_setting(name)

    if name=="download.enabled":
        try:
            from core import descargados
            dev="true"
        except:
            import sys
            for line in sys.exc_info():
                print line
            dev="false"
    
    elif name=="cookies.dir":
        dev=get_data_path()
    
    # TODO: De momento la cache está desactivada...
    elif name=="cache.mode":
        dev="2"
    
    elif name=="plugin.name" and dev=="":
        dev="tvalacarta"

    return dev

def set_setting(name,value):
    exec "import platform."+PLATFORM+".config as platformconfig"
    platformconfig.set_setting(name,value)

def get_localized_string(code):
    exec "import platform."+PLATFORM+".config as platformconfig"
    return platformconfig.get_localized_string(code)

def get_library_path():
    exec "import platform."+PLATFORM+".config as platformconfig"
    return platformconfig.get_library_path()

def get_temp_file(filename):
    exec "import platform."+PLATFORM+".config as platformconfig"
    return platformconfig.get_temp_file()

def get_runtime_path():
    exec "import platform."+PLATFORM+".config as platformconfig"
    return platformconfig.get_runtime_path()

def get_data_path():
    exec "import platform."+PLATFORM+".config as platformconfig"
    return platformconfig.get_data_path()
