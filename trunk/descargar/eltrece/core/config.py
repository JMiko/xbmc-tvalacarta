# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Gestión de parámetros de configuración
#-------------------------------------------------------------------------------

import os,re

overrides = dict()

def get_platform():
    return ""

def get_system_platform():
    return ""
    
def open_settings():
    return

def get_setting(name):
    if name in overrides:
        dev = overrides[name]
    elif name=="cache.mode":
        dev = "2"
    elif name=="cookies.dir":
        dev = get_data_path()
    else:
        dev = ""
    return dev
    
def set_setting(name,value):
    overrides[name]=value

def get_localized_string(code):
    return ""

def get_library_path():
    return ""

def get_temp_file(filename):
    return os.path.join(get_data_path(),filename)

def get_data_path():
    data_path = os.path.join( os.path.expanduser("~") , ".descargar-eltrece" )
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    return data_path

def get_runtime_path():
    return os.getcwd()
