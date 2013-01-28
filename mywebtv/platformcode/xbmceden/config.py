# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración para XBMC Eden

print "[config.py] xbmceden config"

import sys
import os

import xbmcaddon
import xbmc

PLUGIN_NAME = "mywebtv"
__settings__ = xbmcaddon.Addon(id="plugin.video."+PLUGIN_NAME)
__language__ = __settings__.getLocalizedString

def force_platform(platform_name):
    return

def get_platform():
    return "xbmceden"

def get_library_support():
    return True

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
    dev = __settings__.getSetting( name )

    if name=="download.enabled":
        try:
            from core import descargas
            dev="true"
        except:
            #import sys
            #for line in sys.exc_info():
            #    print line
            dev="false"
    
    elif name=="cookies.dir":
        dev=get_data_path()
    
    # TODO: (3.1) De momento la cache está desactivada...
    elif name=="cache.mode":
        dev="2"
    
    return dev

def set_setting(name,value):
    __settings__.setSetting( name,value )

def save_settings():
    return

def get_localized_string(code):
    dev = __language__(code)

    try:
        dev = dev.encode("utf-8")
    except:
        pass
    
    return dev

def get_library_path():
    if get_system_platform() == "xbox":
        return xbmc.translatePath(os.path.join(get_runtime_path(),"library"))
    else:
        return xbmc.translatePath("special://profile/addon_data/plugin.video."+PLUGIN_NAME+"/library")

def get_temp_file(filename):
    return xbmc.translatePath( os.path.join( "special://temp/", filename ))

def get_runtime_path():
    return xbmc.translatePath( __settings__.getAddonInfo('Path') )

def get_data_path():
    dev = xbmc.translatePath( __settings__.getAddonInfo('Profile') )
    
    # Parche para XBMC4XBOX
    if not os.path.exists(dev):
        os.makedirs(dev)
    
    return dev

def get_cookie_data():
    import os
    ficherocookies = os.path.join( get_data_path(), 'cookies.dat' )

    cookiedatafile = open(ficherocookies,'r')
    cookiedata = cookiedatafile.read()
    cookiedatafile.close();

    return cookiedata

# Test if all the required directories are created
def verify_directories_created():
    import logger
    import os
    logger.info("verify_directories_created")

    # Force bookmark path if empty
    bookmark_path = get_setting("bookmarkpath")
    if bookmark_path=="":
        bookmark_path = os.path.join( get_data_path() , "bookmarks")
        set_setting("bookmarkpath" , bookmark_path)

    # Create data_path if not exists
    if not os.path.exists(get_data_path()):
        logger.debug("Creating data_path "+get_data_path())
        try:
            os.mkdir(get_data_path())
        except:
            pass

    # Create bookmark_path if not exists
    if not bookmark_path.lower().startswith("smb") and not os.path.exists(bookmark_path):
        logger.debug("Creating bookmark_path "+bookmark_path)
        try:
            os.mkdir(bookmark_path)
        except:
            pass

print "[config.py] runtime path = "+get_runtime_path()
print "[config.py] data path = "+get_data_path()
print "[config.py] temp path = "+get_temp_file("test")
