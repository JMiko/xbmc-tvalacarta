# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para tva
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

try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[tva.py] init")

DEBUG = True
CHANNELNAME = "TV Azteca"
CHANNELCODE = "tva"

def mainlist(params,url,category):
	xbmc.output("[tva.py] mainlist")

	url = "http://www.tvazteca.com/barraprogramacion/index"

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae las categorias (carpetas)
	# --------------------------------------------------------
	#patron = '<li><span><a href="(secciones.asp[^"]+)">([^<]+)<'   url=\'([^\']+)\'/>'
	
	#http://www.tvazteca.com/capitulos
	#<a class="aproghover" href="/a-cada-quien-su-santo"></a> 
        #<img src="http://www.statictvazteca.com/imagenes/2010/12/6099.jpg" width="150" height="84" alt="A cada quien su santo"/> 
	
	patron = '<a class="aproghover" href="/([^"]+)"></a>([^"]+)<img src="([^"]+)" width="(\d+)" height="(\d+)" alt="([^"]+)"/>' 
	
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		xbmc.output(match[0])
		scrapedtitle = match[5]
		scrapedurl = "http://www.tvazteca.com/capitulos/" + match[0] + "/index"
		scrapedthumbnail = match[2]
		scrapedplot = ""
		scrapedProgramId = match[0]
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		#addvideo( scrapedtitle , scrapedurl , category )
		#addnewfolder( canal , accion , category , title , url , thumbnail , plot ):
		#xbmctools.addnewfolder( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
		xbmctools.addnewfolder2( CHANNELCODE , "videolist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot, scrapedProgramId )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def videolist(params,url,category):
	xbmc.output("[tva.py] videolist")

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los videos
	# --------------------------------------------------------
	#patron = '<div class="texto">.*?<a href="([^"]+)">([^<]+)(.*?)</div>.*?<img src="([^"]+)"'
	programId = params.get("programId")
	xbmc.output(programId)
	#patron='<a href="/capitulos/' + programId + '/([^"]+)"'
	#patron='<p class="fontSize20 colorGrisObscuro margin-B5">([^"]+)</p>([^"]+)<a href="/capitulos/' + programId + '([^"]+)"' + '<img src="([^"]+)"([^"]+)' 
	patron='<p class="fontSize20 colorGrisObscuro margin-B5">(.*?)</p>(.*?)<a href="/capitulos/' + programId + '([^"]+)"(.*?)' + '<img src="([^"]+)"' 
	xbmc.output(patron)
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		
		scrapedtitle = match[0]
		# TODO: Sacar la fecha de la descripcion
		#patronfechas = "<p>Emissi&oacute;: ([^<]+)<"
		#matchesfechas = re.compile(patronfechas,re.DOTALL).findall(match[2])
		#if len(matchesfechas)>0:
		#	scrapedtitle = scrapedtitle + " (" + matchesfechas[0] + ")"

		scrapedurl = 'http://www.tvazteca.com/capitulos/' + programId + match[2]
		#scrapedthumbnail = ""
		scrapedthumbnail = match[4]
		#scrapedthumbnail = urlparse.urljoin(url,match[3]).replace(" ","%20")
		
		scrapedplot = ""
		#scrapedplot = "%s" % match[2]
		#scrapedplot = scrapedplot.strip()
		#scrapedplot = scrapedplot.replace("</a>","")
		#scrapedplot = scrapedplot.replace("</p>","")
		#scrapedplot = scrapedplot.replace("<p>","")
		#scrapedplot = scrapertools.entityunescape(scrapedplot)
		scrapedProgramId = match[2]

		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		#addnewfolder( canal , accion , category , title , url , thumbnail , plot ):
		xbmctools.addnewfolder2( CHANNELCODE , "videolist2" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot, scrapedProgramId )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
	
def videolist2(params,url,category):
	xbmc.output("[tva.py] videolist2")

	# --------------------------------------------------------
	# Descarga la página
	# --------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------
	# Extrae los videos
	# --------------------------------------------------------
	#patron = '<div class="texto">.*?<a href="([^"]+)">([^<]+)(.*?)</div>.*?<img src="([^"]+)"'
	titulo = params.get("title")
	patron='urlToPlay=([^"]+)\'>'
	match = re.compile(patron,re.DOTALL).findall(data)
	
	if DEBUG:
		scrapertools.printMatches(match)

	
	xbmc.output(match[0])
	scrapedtitle = scrapertools.entityunescape(match[0])
	# TODO: Sacar la fecha de la descripcion
	#patronfechas = "<p>Emissi&oacute;: ([^<]+)<"
	#matchesfechas = re.compile(patronfechas,re.DOTALL).findall(match[2])
	#if len(matchesfechas)>0:
	#	scrapedtitle = scrapedtitle + " (" + matchesfechas[0] + ")"

	scrapedurl = match[0]
	scrapedthumbnail = ""
	scrapedplot = ""
	
	#scrapedplot = "%s" % match[2]
	#scrapedplot = scrapedplot.strip()
	#scrapedplot = scrapedplot.replace("</a>","")
	#scrapedplot = scrapedplot.replace("</p>","")
	#scrapedplot = scrapedplot.replace("<p>","")
	#scrapedplot = scrapertools.entityunescape(scrapedplot)

	if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

	# Añade al listado de XBMC
	#addvideo( scrapedtitle , scrapedurl , category )
	xbmctools.addnewvideo( CHANNELCODE , "play" , CHANNELNAME , "" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )
	#server = "Directo"
	#xbmctools.playvideo(CHANNELNAME,server,scrapedurl,CHANNELNAME,scrapedtitle,scrapedthumbnail,scrapedplot)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )	

def play(params,url,category):
	xbmc.output("[a3.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = "Directo"

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
