# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Configuracion
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import xbmc
import xbmcplugin
import sys

def openSettings(name):
	
	# Nuevo XBMC
	try:
		import xbmcaddon
		__settings__ = xbmcaddon.Addon(id='pelisalacarta')
		__settings__.openSettings()
	# Antiguo XBMC
	except:
		xbmcplugin.openSettings( sys.argv[ 0 ] )

def getSetting(name):
	# Nuevo XBMC
	try:
		import xbmcaddon
		__settings__ = xbmcaddon.Addon(id='pelisalacarta')
		return __settings__.getSetting( name )
	# Antiguo XBMC
	except:
		value = xbmcplugin.getSetting(name)
		xbmc.output("[config.py] antiguo getSetting(%s)=%s" % (name,value))
		return value

def setSetting(name,value):
	# Nuevo XBMC
	try:
		import xbmcaddon
		__settings__ = xbmcaddon.Addon(id='pelisalacarta')
		__settings__.setSetting( name,value ) # this will return "foo" setting value
	# Antiguo XBMC
	except:
		config.setSetting("name",value)

def getLocalizedString(code):
	# Nuevo XBMC
	try:
		import xbmcaddon
		__settings__ = xbmcaddon.Addon(id='pelisalacarta')
		__language__ = __settings__.getLocalizedString
		__language__ = __settings__.getLocalizedString
		return __language__(code)
	# Antiguo XBMC
	except:
		return "no implementado"
