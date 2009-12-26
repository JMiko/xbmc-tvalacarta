# -*- coding: iso-8859-1 -*-

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools

xbmc.output("[channelselector.py] init")

DEBUG = True
IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images' ) )

#57=DVD Thumbs
#xbmc.executebuiltin("Container.SetViewMode(57)")
#50=full list
#xbmc.executebuiltin("Container.SetViewMode(50)")
#51=list
#xbmc.executebuiltin("Container.SetViewMode(51)")
#53=icons
#xbmc.executebuiltin("Container.SetViewMode(53)")
#54=wide icons
#xbmc.executebuiltin("Container.SetViewMode(54)")

def listchannels(params,url,category):
	xbmc.output("[channelselector.py] listchannels")

	# Verifica actualizaciones solo en el primer nivel
	if xbmcplugin.getSetting("updatecheck2") == "true":
		xbmc.output("updatecheck=true")
		import updater
		updater.checkforupdates()
	else:
		xbmc.output("updatecheck=false")

	addfolder("Antena3","a3","mainlist")
	addfolder("ADNStream","adnstream","mainlist")
	addfolder("Barcelona TV","barcelonatv","mainlist")
	addfolder("Clan TV","clantv","mainlist")
	addfolder("EITB","eitb","mainlist")
	addfolder("Extremadura TV","extremaduratv","mainlist")
	addfolder("Hogarutil","hogarutil","mainlist")
	addfolder("Plus TV","plus","mainlist")
	addfolder("Andalucia TV","rtva","mainlist")
	addfolder("TVE","rtve","mainlist")
	addfolder("Mediateca TVE","rtvemediateca","mainlist")
	addfolder("Comunidad Valenciana","rtvv","mainlist")
	addfolder("Terra TV","terratv","mainlist")
	addfolder("Turbonick","turbonick","mainlist")
	addfolder("TV3","tv3","mainlist")
	addfolder("TVG","tvg","mainlist")
	addfolder("Mallorca TV","tvmallorca","mainlist")
	addfolder("Meristation","meristation","mainlist")
	addfolder("Favoritos","favoritos","mainlist")
	addfolder("Descargas","descargados","mainlist")
	addfolder("Configuración","configuracion","mainlist")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="Canales" )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def addfolder(nombre,channelname,accion):
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=os.path.join(IMAGES_PATH, channelname+".png"))
	itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , urllib.quote_plus(nombre) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)