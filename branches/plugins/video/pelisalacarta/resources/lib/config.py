# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import xbmc
import xbmcplugin
import sys
try:
	import xbmcaddon
	DHARMA = True
except ImportError:
	DHARMA = False

def openSettings():
	
	# Nuevo XBMC
	if DHARMA:
		__settings__ = xbmcaddon.Addon(id="plugin.video.pelisalacarta")
		__settings__.openSettings()
	# Antiguo XBMC
	else:
		xbmcplugin.openSettings( sys.argv[ 0 ] )

def getSetting(name):
	# Nuevo XBMC
	if DHARMA:
		__settings__ = xbmcaddon.Addon(id="plugin.video.pelisalacarta")
		return __settings__.getSetting( name )
	# Antiguo XBMC
	else:
		value = xbmcplugin.getSetting(name)
		xbmc.output("[config.py] antiguo getSetting(%s)=%s" % (name,value))
		return value

def setSetting(name,value):
	# Nuevo XBMC
	if DHARMA:
		__settings__ = xbmcaddon.Addon(id="plugin.video.pelisalacarta")
		__settings__.setSetting( name,value ) # this will return "foo" setting value
	# Antiguo XBMC
	else:
		xbmcplugin.setSetting("name",value)

def getLocalizedString(code):
	# Nuevo XBMC
	if DHARMA:
		__settings__ = xbmcaddon.Addon(id="plugin.video.pelisalacarta")
		__language__ = __settings__.getLocalizedString
		__language__ = __settings__.getLocalizedString
		return __language__(code)
	# Antiguo XBMC
	else:
		return "no implementado"
