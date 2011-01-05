# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para filmstreaming [it]
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse
import urllib2
import urllib
import re
import os
import sys
import binascii

import xbmc
import xbmcgui
import xbmcplugin

import xbmctools
import scrapertools
import servertools
import linkbucks
import config
import logger

CHANNELNAME = "italiafilm"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[italiafilm.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[italiafilm.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "searchmovie" , category , "Cerca Film","","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Anime" , "http://italia-film.com/anime-e-cartoon/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Telefilm" , "http://italia-film.com/telefilm/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Animazione" , "http://italia-film.com/film-animazione/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Avventura" , "http://italia-film.com/film-avventura/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Azione" , "http://italia-film.com/film-azione/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Comici" , "http://italia-film.com/film-comici/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Commedia" , "http://italia-film.com/film-commedia/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Drammatici" , "http://italia-film.com/film-drammatici/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Fantascienza" , "http://italia-film.com/film-fantascienza/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Fantasy" , "http://italia-film.com/film-fantasy/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Gangster" , "http://italia-film.com/film-gangster/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Guerra" , "http://italia-film.com/film-guerra/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Horror" , "http://italia-film.com/film-horror/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Musical" , "http://italia-film.com/film-musical/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Poliziesco" , "http://italia-film.com/film-poliziesco/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Romantici" , "http://italia-film.com/film-romantici/","","") 
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Erotici" , "http://italia-film.com/film-erotici/","","") 
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Storici" , "http://italia-film.com/film-storici/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Thriller" , "http://italia-film.com/film-thriller/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , "Film Western" , "http://italia-film.com/film-western/","","")

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
	
def searchmovie(params,url,category):
	xbmc.output("[cineblog01.py] searchmovie")

	keyboard = xbmc.Keyboard('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://italia-film.com/index.php?story={"+tecleado+"}&do=search&subaction=search"
			peliculas(params,searchUrl,category)

def peliculas(params,url,category):
	logger.info("[italiafilm.py] peliculas")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="notes">.*?<a href="([^"]+).*?<img.*?src="([^"]+)".*?title=\'([^\']+)'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	for match in matches:
		# Atributos
		scrapedtitle = match[2]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = urlparse.urljoin(url,match[1])
		scrapedplot = ""
		
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detalle" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae las entradas (carpetas)
	patronvideos  = '<a href="([^"]+)">Avanti&nbsp;&#8594;'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = "Pagina seguente"
		scrapedurl = urlparse.urljoin(url,match)
		scrapedthumbnail = ""
		scrapedplot = ""

		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "peliculas" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detalle(params,url,category):
	logger.info("[italiafilm.py] detalle")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	title = title.title()
	title = title.replace('Serie Tv', '', 1)
	title = title.replace('Streaming', '', 1)
	title = title.replace('Megavideo', '', 1)
	
	# Descarga la página
	data = scrapertools.cachePage(url)
	patronvideos  = '<td class="news">.*?<div id=[^>]+>([^<]+)'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	plot = matches[0]
	plot = plot.replace('&#224;', 'a\'')
	plot = plot.replace('&#232;', 'e\'')
	plot = plot.replace('&#233;', 'e\'')
	plot = plot.replace('&#236;', 'i\'')
	plot = plot.replace('&#242;', 'o\'')
	plot = plot.replace('&#249;', 'u\'')
   
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		out_file = open("test.txt","w")
		patronvideos  = url+'[^>]+>([^<]+)'
		matches = re.compile(patronvideos,re.DOTALL).findall(data)
		scrapertools.printMatches(matches)
		videotitle = matches[0]
		out_file.write(videotitle)
		out_file.close()
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle + " ["+server+"]" , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	logger.info("[italiafilm.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
