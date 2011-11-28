# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Gestión de parámetros de configuración - modo desarrollo
#-------------------------------------------------------------------------------
# tvalacarta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#-------------------------------------------------------------------------------
# Creado por: 
# Jesús (tvalacarta@gmail.com)
# Jurrabi (jurrabi@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#-------------------------------------------------------------------------------
# Historial de cambios:
# 18-12-2010 Implementa lector cadenas internacionales con strings.xml de xbmc
#-------------------------------------------------------------------------------

print "[config.py] Using DEVELOPER config 3.2"

import os,re
import ConfigParser

# Fichero de configuración global
CONFIG_FILE_PATH = os.path.join( os.getcwd(),'resources','settings.conf')
print "Config file path "+CONFIG_FILE_PATH

configfile = ConfigParser.SafeConfigParser()
configfile.read( CONFIG_FILE_PATH )

overrides = dict()

TRANSLATION_FILE_PATH = os.path.join(os.getcwd(),"resources","language","Spanish","strings.xml")
try:
    translationsfile = open(TRANSLATION_FILE_PATH,"r")
    translations = translationsfile.read()
    translationsfile.close()
except:
    translations = ""
print "Config file path "+TRANSLATION_FILE_PATH

def get_platform():
    # TODO: Debería ser windows, mac, linux, ...
    return "developer"

def get_system_platform():
    return "desktop"
    
def open_settings():
    return

def get_setting(name):
    try:
        if name in overrides:
            dev = overrides[name]
            #print "Overrides: ",name,"=",dev
        #elif name=="debug":
        #    return "true"
        else:
            dev=configfile.get("General",name)
            #print "Config file: ",name,"=",dev
        #print "get_setting",name,dev
        return dev
    except:
        #print "get_setting",name,"(vacío)"
        return ""
    
def set_setting(name,value):
    #print "set_setting",name,value
    overrides[name]=value

def get_localized_string(code):
    cadenas = re.findall('<string id="%d">([^<]+)<' % code,translations)
    if len(cadenas)>0:
        return cadenas[0]
    else:
        return "%d" % code
    
def get_library_path():
    # Una forma rápida de lanzar un error
    import noexiste
    return ""

def get_temp_file(filename):
    return os.path.join(get_data_path(),filename)

def get_data_path():
    data_path = os.path.join( os.path.expanduser("~") , ".developer" )
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    return data_path

def get_runtime_path():
    return os.getcwd()

print "get_data_path="+get_data_path()
print "get_runtime_path="+get_runtime_path()