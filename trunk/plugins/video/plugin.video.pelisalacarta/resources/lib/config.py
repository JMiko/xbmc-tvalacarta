# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import xbmc
import xbmcplugin
import sys

def openSettings():
	
	# Nuevo XBMC
	try:
		import xbmcaddon
		__settings__ = xbmcaddon.Addon(id="plugin.video.pelisalacarta")
		__settings__.openSettings()
	# Antiguo XBMC
	except ImportError:
		xbmcplugin.openSettings( sys.argv[ 0 ] )

def getSetting(name):
	# Nuevo XBMC
	try:
		import xbmcaddon
		__settings__ = xbmcaddon.Addon(id="plugin.video.pelisalacarta")
		return __settings__.getSetting( name )
	# Antiguo XBMC
	except ImportError:
		value = xbmcplugin.getSetting(name)
		xbmc.output("[config.py] antiguo getSetting(%s)=%s" % (name,value))
		return value

def setSetting(name,value):
	# Nuevo XBMC
	try:
		import xbmcaddon
		__settings__ = xbmcaddon.Addon(id="plugin.video.pelisalacarta")
		__settings__.setSetting( name,value ) # this will return "foo" setting value
	# Antiguo XBMC
	except ImportError:
		xbmcplugin.setSetting("name",value)

def getLocalizedString(code):
	# Nuevo XBMC
	try:
		import xbmcaddon
		__settings__ = xbmcaddon.Addon(id="plugin.video.pelisalacarta")
		__language__ = __settings__.getLocalizedString
		__language__ = __settings__.getLocalizedString
		return __language__(code)
	# Antiguo XBMC
	except ImportError:
		return "no implementado"
