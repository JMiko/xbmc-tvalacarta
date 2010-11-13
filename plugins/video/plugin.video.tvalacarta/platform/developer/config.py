# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Gestión de parámetros de configuración - modo desarrollo
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

import os

DATA_PATH = os.getcwd()

# Un gestor de parámetros artesano para ejecución desde eclipse
opciones = dict()
opciones["debug"] ="true"

def get_system_platform():
	return "desktop"
	
def open_settings():
	return

def get_setting(name):
	return opciones[name]
	
def set_setting(name,value):
	opciones[name]=value

def get_localized_string(code):
	return code
	
def get_library_path():
	# FIXME: Una forma rápida de lanzar un error
	import noexiste
	return ""

def get_temp_file(filename):
	# FIXME: Una forma rápida de lanzar un error 
	import noexiste
	return ""
