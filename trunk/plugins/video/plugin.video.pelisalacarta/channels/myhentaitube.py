# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para myhentaitube
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
import config
from item import Item
import logger

CHANNELNAME = "myhentaitube"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[myhentaitube.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[myhentaitube.py] mainlist")
	
	itemlist = getmainlist(params,url,category)
	xbmctools.renderItems(itemlist, params, url, category)

def getmainlist(params,url,category):
	logger.info("[myhentaitube.py] getmainlist")

	itemlist = []
	itemlist.append( Item( channel=CHANNELNAME , title="Novedades" , action="novedades" , url="http://myhentaitube.com/" , folder=True ) )
	
	return itemlist

def novedades(params,url,category):
	logger.info("[myhentaitube.py] novedades")

	itemlist = getnovedades(params,url,category)
	xbmctools.renderItems(itemlist, params, url, category)

def getnovedades(params,url,category):
	logger.info("[myhentaitube.py] getnovedades")

	# ------------------------------------------------------
	# Descarga la p�gina
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	# seccion novedades
	'''
		<a href="/index.php?option=com_content&amp;view=article&amp;id=29:ai-shimai-hentai-movie-anime-&amp;catid=1:movies&amp;Itemid=2">
		<img src="/images/stories/ai_shimai_dvd copy.gif" border="0" />
		</a>
	'''

	#patronvideos  = '<p style="text-align: center;">.*?'
	patronvideos = '<a href="(/index.php[^"]+view=article[^"]+id=[^:]([^"]+)catid=1+[^"]+)">[^<]*?'
	patronvideos += '<img src="([^"]+)".*?</a>'


	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = urlparse.urljoin(url,match[2]).replace(" ", "%20")
		scrapedplot = scrapertools.htmlclean(match[1].strip())
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		itemlist.append( Item(channel=CHANNELNAME, action="capitulos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	patronvideos  = '<a href="(\/index.php\?pageNum[^"]+)">[^<]+</a></span>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedurl = urlparse.urljoin(url,matches[0])
		itemlist.append( Item(channel=CHANNELNAME, action="novedades", title="!P�gina siguiente" , url=scrapedurl , folder=True) )

	return itemlist

def capitulos(params,url,category):
	logger.info("[myhentaitube.py] capitulos")
	
	itemlist = getcapitulos(params,url,category)
	xbmctools.renderItems(itemlist, params, url, category)

def getcapitulos(params,url,category):
	logger.info("[myhentaitube.py] getcapitulos")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# ------------------------------------------------------------------------------------
	# Descarga la p�gina
	# ------------------------------------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)
	
	# ------------------------------------------------------------------------------------
	# Busca el argumento
	# ------------------------------------------------------------------------------------
	patronvideos  = '<div class="ficha_des">(.*?)</div>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		plot = scrapertools.htmlclean(matches[0])
		logger.info("plot actualizado en detalle");
	else:
		logger.info("plot no actualizado en detalle");
	
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los mirrors, o a los cap�tulos de las series...
	# ------------------------------------------------------------------------------------
	'''
	<h3 style="text-align: center;">
	<a href="/index.php?option=com_content&amp;view=article&amp;id=8&amp;Itemid=2">CAPITULO 1
	</a></h3>
	'''
	patronvideos = '<a href="(/index.php[^"]+view=article[^"]+id=[^"]+)">([^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	itemlist = []
	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = thumbnail
		scrapedplot = plot
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		itemlist.append( Item(channel=CHANNELNAME, action="detail", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

	return itemlist

def detail(params,url,category):
	logger.info("[myhentaitube.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	logger.info("[myhentaitube.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]

	xbmctools.playvideo4(CHANNELNAME,server,url,category,title,thumbnail,plot)