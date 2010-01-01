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
		xbmc.output("updatecheck2=true")
		import updater
		updater.checkforupdates()
	else:
		xbmc.output("updatecheck2=false")

	addfolder("Cinetube","cinetube","mainlist")
	addfolder("Peliculasyonkis","peliculasyonkis","mainlist")
	addfolder("Divx Online","divxonline","mainlist") # added by ermanitu
	addfolder("Cinegratis","cinegratis","mainlist")
	addfolder("tumejortv.com","tumejortv","mainlist")
	addfolder("Seriesyonkis","seriesyonkis","mainlist")
	addfolder("Seriespepito","seriespepito","mainlist")
	addfolder("seriesonline.us","seriesonline","mainlist")
	addfolder("Newcineonline","newcineonline","mainlist")
	addfolder("PeliculasHD","peliculashd","mainlist")
	addfolder("Pelis24","pelis24","mainlist")
	#addfolder("Pelis-Sevillista56","sevillista","mainlist")
	addfolder("Veocine","veocine","mainlist")
	addfolder("DeLaTV","delatv","mainlist")
	#addfolder("Wuapi","wuapisite","mainlist")
	addfolder("Pintadibujos","pintadibujos","mainlist")
	addfolder("Yotix.tv","yotix","mainlist")
	addfolder("Frozen Layer","frozenlayer","mainlist")
	addfolder("MCAnime","mcanime","mainlist")
	addfolder("Stagevu","stagevusite","mainlist")
	addfolder("tu.tv","tutvsite","mainlist")
	addfolder("Animeid","animeid","mainlist")
	addfolder("Peliculasid","peliculasid","mainlist")
	addfolder("Ovasid","ovasid","mainlist")
	addfolder("Kochikame","kochikame","mainlist")
	addfolder("SesionVIP","sesionvip","mainlist")
	addfolder("PeliculasEroticas","peliculaseroticas","mainlist")
	addfolder("Descarga Cine Clásico","descargacineclasico","mainlist")
	addfolder("Documaniatv","documaniatv","mainlist")
	addfolder("Documentalesyonkis","documentalesyonkis","mainlist")
	addfolder("Documentalesatonline","documentalesatonline","mainlist")
	addfolder("ecartelera (Trailers)","ecarteleratrailers","mainlist")
	addfolder("Configuracion","configuracion","mainlist")
	addfolder("Descargas","descargados","mainlist")
	addfolder("Favoritos","favoritos","mainlist")

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
