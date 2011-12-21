# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import os

from PMS import Locale

def get_system_platform():
    return "osx"
    
def open_settings():
    return

def get_platform():
    return "plex"

def get_setting(name,channel=""):
    try:
        prefs = []
        from PMS import Log
        from PMS import Plugin
        Log("bundlepath="+Plugin.__bundlePath)
        #/Users/jesus/Library/Application Support/Plex Media Server/Plug-ins/pelisalacarta.bundle
        path = "%s/Contents/DefaultPrefs.json" % Plugin.__bundlePath
        if os.path.exists(path):
            f = open(path, "r")
            string = f.read()
            f.close()
            from PMS import JSON
            prefs = JSON.ObjectFromString(string)
    
        from PMS import Prefs
        Log("prefspath="+Prefs.__prefsPath)
        #/Users/jesus/Library/Application Support/Plex Media Server/Plug-in Support/Preferences/com.plexapp.plugins.pelisalacarta.xml
        path = Prefs.__prefsPath
        if os.path.exists(path):
            f = open(path, "r")
            from PMS import XML
            userPrefs = XML.ElementFromString(f.read())
            f.close()
            for userPref in userPrefs:
                for pref in prefs:
                    if pref["id"] == userPref.tag:
                        pref["value"] = userPref.text
        
        from PMS import Log
        valor = ""
        for pref in prefs:
            Log("pref="+str(pref))
            if pref["id"]==name:
                valor = pref["value"]
    except:
        valor=""

    if name=="cache.dir":
        return ""

    if name=="download.enabled":
        return "false"
    
    if name=="cookies.dir":
        return os.getcwd()
    
    if name=="quality_youtube":
        return "8"

    elif name=="cache.mode":
        return "2"

    return valor

def set_setting(name,value):
    return ""

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

def get_cookie_data():
    import os
    ficherocookies = os.path.join( get_data_path(), 'cookies.lwp' )

    cookiedatafile = open(ficherocookies,'r')
    cookiedata = cookiedatafile.read()
    cookiedatafile.close();

    return cookiedata
