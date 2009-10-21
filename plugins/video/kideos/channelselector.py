# -*- coding: iso-8859-1 -*-

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import xbmctools

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

	CHANNELNAME = "kideoschannel"
	xbmctools.addnewfolder( CHANNELNAME , "ageslist" , CHANNELNAME , xbmc.getLocalizedString( 30501 ) , "" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "categorylist" , CHANNELNAME , xbmc.getLocalizedString( 30502 ) , "" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "userlist" , CHANNELNAME , xbmc.getLocalizedString( 30503 ) , "" , "", "" )
	xbmctools.addnewfolder( "configuracion" , "mainlist" , "configuracion" , xbmc.getLocalizedString( 30504 ) , "" , "", "" )
	xbmctools.addnewfolder( "descargados" , "mainlist" , "descargados" , xbmc.getLocalizedString( 30505 ) , "" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="Canales" )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
