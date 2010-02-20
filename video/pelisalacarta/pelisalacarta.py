# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Main
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urllib
import os
import sys
import xbmc
import xbmctools
import xbmcgui
import urllib,urllib2

def run():
	xbmc.output("[pelisalacarta.py] run")
	
	# Imprime en el log los par�metros de entrada
	xbmc.output("[pelisalacarta.py] sys.argv=%s" % str(sys.argv))
	
	# Crea el diccionario de parametros
	params = dict()
	if len(sys.argv)>=2 and len(sys.argv[2])>0:
		params = dict(part.split('=') for part in sys.argv[ 2 ][ 1: ].split('&'))
	xbmc.output("[pelisalacarta.py] params=%s" % str(params))
	
	# Extrae la url de la p�gina
	if (params.has_key("url")):
		url = urllib.unquote_plus( params.get("url") )
	else:
		url=''
	xbmc.output("[pelisalacarta.py] url="+url)

	# Extrae la accion
	if (params.has_key("action")):
		action = params.get("action")
	else:
		action = "selectchannel"
	xbmc.output("[pelisalacarta.py] action="+action)

	# Extrae el server
	if (params.has_key("server")):
		server = params.get("server")
	else:
		server = ""
	xbmc.output("[pelisalacarta.py] server="+server)

	# Extrae la categoria
	if (params.has_key("category")):
		category = params.get("category")
	else:
		if params.has_key("channel"):
			category = params.get("channel")
		else:
			category = ""
	xbmc.output("[pelisalacarta.py] category="+category)

	#JUR - Gesti�n de Errores de Internet (Para que no casque el plugin 
	#      si no hay internet (que queda feo)
	try:
	# Accion por defecto - elegir canal
		if ( action=="selectchannel" ):
			import channelselector as plugin
			plugin.listchannels(params, url, category)
		# Actualizar version
		elif ( action=="update" ):
			import updater
			updater.update(params)
			import channelselector as plugin
			plugin.listchannels(params, url, category)
		# El resto de acciones vienen en el par�metro "action", y el canal en el par�metro "channel"
		elif (action=="strm"):
			xbmctools.playstrm(params, url, category)
		else:
			exec "import "+params.get("channel")+" as plugin"
			exec "plugin."+action+"(params, url, category)"
	except urllib2.URLError:
		xbmc.output("[pelisalacarta.py] Error de conexi�n a Internet - Interceptado")
		ventana_error = xbmcgui.Dialog()
		ok= ventana_error.ok ("Plugin Pelisalacarta", "No se ha podido acceder a internet", "Comprueba la conexi�n")