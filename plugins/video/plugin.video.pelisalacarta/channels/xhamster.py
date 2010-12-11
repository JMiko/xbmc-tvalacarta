# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para xhamster
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

CHANNELNAME = "xhamster"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[xhamster.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[xhamster.py] mainlist")
	
	itemlist = getmainlist(params,url,category)
	xbmctools.renderItems(itemlist, params, url, category)

def getmainlist(params,url,category):
	logger.info("[xhamster.py] getmainlist")

	itemlist = []
	itemlist.append( Item( channel=CHANNELNAME , title="Novedades" , action="novedades" , url="http://www.xhamster.com/" , folder=True ) )
	
	return itemlist

def novedades(params,url,category):
	logger.info("[xhamster.py] novedades")

	itemlist = getnovedades(params,url,category)
	xbmctools.renderItems(itemlist, params, url, category)

def getnovedades(params,url,category):
	logger.info("[xhamster.py] getnovedades")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	# seccion novedades
	'''
<a href="/movies/496069/the_cheerleader.html" class="hRotator">
<img src="http://st5.xhamster.com/t/069/2_496069.jpg" height="120" width="160">
<img class="hSprite" src="http://static.xhamster.com/images/spacer.gif" sprite="http://st5.xhamster.com/t/069/s_496069.jpg" id="496069" onmouseover="hRotator.start2(this);" height="120" width="160">
</a>
      <div class="moduleFeaturedTitle">
        <a href="/movies/496069/the_cheerleader.html">The Cheerleader</a>
      </div>
      <div class="moduleFeaturedDetails">Runtime: 35m51s<br><span style="color: Green;">'''

	#patronvideos  = '<p style="text-align: center;">.*?'
	patronvideos = '<a href="(/movies/[^"]+.html)"[^>]*?>[^<]*?'
	patronvideos += '<img src=\'([^\']+.xhamster.com[^\']+)\'[^>]+>[^<]*?'
	patronvideos += '<img[^<]*?>[^<]*?</a>[^<]*?'
	patronvideos += '<div[^<]*?>[^<]*?'
	patronvideos += '<a href="/movies/[^"]+.html"[^>]*?>([^<]+)</a>[^<]*?'
	patronvideos += '</div[^<]*?>[^<]*?'
	patronvideos += '<div[^<]*?>Runtime: ([^<]+)<'


	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		# Titulo
		scrapedtitle = match[2] + " [" + match[3] + "]"
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = match[1].replace(" ", "%20")
		scrapedplot = scrapertools.htmlclean(match[2].strip())
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		itemlist.append( Item(channel=CHANNELNAME, action="detail", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	#<A HREF="/new/2.html">Next</A><
	patronvideos  = '<a href="\/(new\/[^\.]+\.html)"[^>]*?>Next[^<]*?<\/a>'
	matches = re.compile(patronvideos,re.DOTALL | re.IGNORECASE).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedurl = urlparse.urljoin(url,matches[0])
		logger.info("[xhamster.py] " + scrapedurl)
		itemlist.append( Item(channel=CHANNELNAME, action="novedades", title="!Página siguiente" , url=scrapedurl , folder=True) )

	return itemlist

def detail(params,url,category):
	logger.info("[xhamster.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	if len(listavideos)>0:
		video = listavideos[0]
		videotitle = video[0]
		url = "http://xhamster.com/flv2/" + video[1]
		server = video[2]
		logger.info("[xhamster.py] play")
		xbmctools.playvideo4(CHANNELNAME,server,url,category,title,thumbnail,plot)
	# ------------------------------------------------------------------------------------

	# Cierra el directorio
	#xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	#xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	#xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )