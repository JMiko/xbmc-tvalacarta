# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# mywebtv - XBMC Plugin
# Canal Tivion
# http://blog.tvalacarta.info/plugin-xbmc/mywebtv/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import scrapertools
import binascii
import xbmctools
import tivionchannels

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[tivion.py] init")

DEBUG = True
CHANNELNAME = "Tivion"
CHANNELCODE = "tivion"

def mainlist(params,url,category):
	xbmc.output("[tivion.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELCODE , "paises" , CHANNELNAME , "Todos los canales por paises" , "" , "" , "" )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def paises(params,url,category):
	xbmc.output("[tivion.py] paises")

	dictionarypaises = {}
	channels = tivionchannels.CHANNEL
	
	for channel in channels:
		if not dictionarypaises.has_key(channel[1]):
			xbmctools.addnewfolder( CHANNELCODE , "videos" , CHANNELNAME , channel[1] , channel[1] , "", "" )
			dictionarypaises[channel[1]] = True

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videos(params,url,category):
	xbmc.output("[tivion.py] videos")

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	channels = tivionchannels.CHANNEL
	
	for channel in channels:
		if url == channel[1]:
			xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , channel[3]+" "+channel[1] , channel[4] , "", channel[4] )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[tivion.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
