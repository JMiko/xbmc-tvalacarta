# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# Goear - XBMC Plugin
# Launcher
# http://blog.tvalacarta.info/plugin-xbmc/goear/
#------------------------------------------------------------

# Constantes
__plugin__  = "Goear"
__author__  = "tvalacarta & emilio"
__url__     = "http://blog.tvalacarta.info/plugin-xbmc/goear/"
__date__    = "04 Abril 2010"
__version__ = "1.0"

import urllib
import os
import sys
import xbmc
import goear

xbmc.output("[default.py] goear init...")

# Configura los directorios donde hay librer�as
librerias = xbmc.translatePath( os.path.join( os.getcwd(), 'resources', 'lib' ) )
sys.path.append (librerias)

# Programa principal

# Imprime en el log los par�metros de entrada
xbmc.output("[default.py] sys.argv=%s" % str(sys.argv))

# Crea el diccionario de parametros
params = dict()
if len(sys.argv)>=2 and len(sys.argv[2])>0:
	params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
xbmc.output("[default.py] params=%s" % str(params))

# Extrae la url de la p�gina
if (params.has_key("url")):
	url = urllib.unquote_plus( params.get("url") )
else:
	url=''
xbmc.output("[default.py] url="+url)

# Extrae la accion
if (params.has_key("action")):
	action = params.get("action")
else:
	action = ""
xbmc.output("[default.py] action="+action)

# Extrae la categoria
if (params.has_key("category")):
	category = params.get("category")
else:
	if params.has_key("channel"):
		category = params.get("channel")
	else:
		category = ""
xbmc.output("[default.py] category="+category)


# Accion por defecto - elegir canal
if ( action=="" ):
	goear.mainlist(params, url, category)
# Actualizar version
elif ( action=="update" ):
	import updater
	updater.update(params)
	goear.mainlist(params, url, category)
# El resto de acciones vienen en el par�metro "action", y el canal en el par�metro "channel"
else:
	exec "goear."+action+"(params, url, category)"
