# -*- coding: iso-8859-1 -*-

import urllib
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

xbmc.output("[channelselector.py] init")

DEBUG = True
IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' ) )

def listchannels(params,url,category):
	xbmc.output("[channelselector.py] listchannels")

	# Verifica actualizaciones solo en el primer nivel
	if xbmcplugin.getSetting("updatecheck2") == "true":
		xbmc.output("updatecheck=true")
		import updater
		updater.checkforupdates()
	else:
		xbmc.output("updatecheck=false")

	addfolder("Tivion","tivion","mainlist")
	addfolder("Delicast","delicast","mainlist")
	addfolder("TheHaine","thehaine","mainlist")
	addfolder("Favoritos","favoritos","mainlist")
	addfolder("Configuración","configuracion","mainlist")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="Canales" )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def addfolder(nombre,channelname,accion):
	#listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=os.path.join(IMAGES_PATH, channelname+".png"))
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage="http://www.mimediacenter.info/xbmc/mywebtv/"+channelname+".png")
	itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , urllib.quote_plus(nombre) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
