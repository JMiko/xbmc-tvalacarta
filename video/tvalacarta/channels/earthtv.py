# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal EARTH TV en YouTube
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
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
import youtube

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[earthtv.py] init")

DEBUG = True
CHANNELNAME = "Earth TV"
CHANNELCODE = "earthtv"

def mainlist(params,url,category):
	xbmc.output("[earthtv.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELCODE , "novedades" , CHANNELNAME , "Novedades" , "" , "" , "" )
	
	itemlist = youtube.getplaylists("earthTV",1,10)
	for item in itemlist:
		xbmctools.addnewfolder( CHANNELCODE , "playlist" , CHANNELNAME , item.title , item.url , item.thumbnail , item.plot )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def novedades(params,url,category):
	xbmc.output("[earthtv.py] novedades")
	itemlist = youtube.getuploads("earthTV",1,10)
	videos(params,url,category,itemlist)

def playlist(params,url,category):
	xbmc.output("[earthtv.py] playlist")
	itemlist = youtube.getplaylistvideos(url,1,10)
	videos(params,url,category,itemlist)

def videos(params,url,category,itemlist):
	xbmc.output("[earthtv.py] videos")

	for item in itemlist:
		xbmctools.addnewvideo( CHANNELCODE , "play" , category , "Directo" , item.title , item.url , item.thumbnail , item.plot )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[earthtv.py] play")

	# Extrae el ID
	id = youtube.Extract_id(url)
	xbmc.output("[earthtv.py] id="+id)
	
	# Descarga la página
	data = scrapertools.cachePage(url)
	
	# Obtiene la URL
	url = youtube.geturls(id,data)
	print url
	
	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
