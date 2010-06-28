# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinegratis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import megavideo
import servertools
import binascii
import xbmctools

import cinegratis
import peliculasyonkis
import cine15
import seriesyonkis
import yotix
import peliculas21
import sesionvip
import documaniatv
import discoverymx
import stagevusite
import tutvsite
import tumejortv
import config
import cinetube

CHANNELNAME = "buscador"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[buscador.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[buscador.py] mainlist")

	keyboard = xbmc.Keyboard('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)<=0:
			return
	
	tecleado = tecleado.replace(" ", "+")
	
	# Lanza las búsquedas
	
	# Cinegratis
	matches = []
	try:
		matches.extend( cinetube.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( cinegratis.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( peliculasyonkis.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( tumejortv.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( cine15.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( peliculas21.performsearch(tecleado) )
	except:
		pass
	#matches.extend( sesionvip.performsearch(tecleado) )
	try:
		matches.extend( seriesyonkis.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( documaniatv.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( discoverymx.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( yotix.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( stagevusite.performsearch(tecleado) )
	except:
		pass
	try:
		matches.extend( tutvsite.performsearch(tecleado) )
	except:
		pass
	
	# Construye los resultados
	for match in matches:
		targetchannel = match[0]
		action = match[1]
		category = match[2]
		scrapedtitle = match[3]+" ["+targetchannel+"]"
		scrapedurl = match[4]
		scrapedthumbnail = match[5]
		scrapedplot = match[6]
		
		xbmctools.addnewfolder( targetchannel , action , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_TITLE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
