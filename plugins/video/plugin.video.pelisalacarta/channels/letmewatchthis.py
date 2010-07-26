# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para letmewatchthis
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

CHANNELNAME = "letmewatchthis"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[letmewatchthis.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[letmewatchthis.py] mainlist")
	
	itemlist = getmainlist(params,url,category)
	xbmctools.renderItems(itemlist, params, url, category)

def peliculas(params,url,category):
	logger.info("[letmewatchthis.py] peliculas")

	itemlist = getpeliculas(params,url,category)
	xbmctools.renderItems(itemlist, params, url, category)

def series(params,url,category):
	logger.info("[letmewatchthis.py] series")

	itemlist = getseries(params,url,category)
	xbmctools.renderItems(itemlist, params, url, category)

def getmainlist(params,url,category):
	logger.info("[letmewatchthis.py] getmainlist")

	itemlist = []
	itemlist.append( Item(channel=CHANNELNAME, config.getLocalizedString("40001") , action="peliculas", url="http://www.letmewatchthis.es/" , folder=True) )
	itemlist.append( Item(channel=CHANNELNAME, config.getLocalizedString("40002") , action="series"   , url="http://www.letmewatchthis.com/?tv"  , folder=True) )
	
	return itemlist

def getpeliculas(params,url,category):
	logger.info("[letmewatchthis.py] getpeliculas")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	'''
	<div class="index_item index_item_ie"><a href="/watch-356059-Here-Come-the-Co-eds" title="Watch Here Come the Co-eds (1945) - 37 views"><img src="http://images.letmewatchthis.com/thumbs/356059_Here_Come_the_Co_eds_1945.jpg" border="0" alt="Watch Here Come the Co-eds"><h2>Here Come the Co-.. (1945)</h2></a><div class="index_ratings">
	<div id="unit_long356059">
	<ul style="width: 100px;" class="unit-rating">
	<li style="width: 60px;" class="current-rating">Current rating.</li> <li class="r1-unit"></li>
	<li class="r2-unit"></li>
	<li class="r3-unit"></li>
	<li class="r4-unit"></li>
	<li class="r5-unit"></li>
	</ul>
	</div>
	</div><div class="item_categories"><a href="/?genre=Comedy">Comedy</a> <a href="/?genre=Musical">Musical</a> </div></div>
	'''
	patronvideos  = '<div class="index_item index_item_ie"><a href="/watch-356059-Here-Come-the-Co-eds" title="Watch Here Come the Co-eds (1945) - 37 views"><img src="http://images.letmewatchthis.com/thumbs/356059_Here_Come_the_Co_eds_1945.jpg"'

	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG: scrapertools.printMatches(matches)

	itemlist = []
	for match in matches:
		# Titulo
		scrapedtitle = match[2] + " [" + match[3] + "]"
		matchesconectores = re.compile('<img.*?alt="([^"]*)"',re.DOTALL).findall(match[4])
		conectores = ""
		for matchconector in matchesconectores:
			logger.info("matchconector="+matchconector)
			if matchconector=="":
				matchconector = "megavideo"
			conectores = conectores + matchconector + "/"
		if len(matchesconectores)>0:
			scrapedtitle = scrapedtitle + " (" + conectores[:-1] + ")"

		# Convierte desde UTF-8 y quita entidades HTML
		try:
			scrapedtitle = unicode( scrapedtitle, "utf-8" ).encode("iso-8859-1")
		except:
			pass
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)

		# procesa el resto
		scrapedplot = ""

		scrapedurl = urlparse.urljoin("http://www.letmewatchthis.es/",match[1])
		scrapedthumbnail = match[0]
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		itemlist.append( Item(channel=CHANNELNAME, action="listmirrors", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	#<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
	patronvideos  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedurl = urlparse.urljoin(url,matches[0])
		itemlist.append( Item(channel=CHANNELNAME, action="listpeliconcaratula", title="!Página siguiente" , url=scrapedurl , folder=True) )

	return itemlist

def listpelisincaratula(params,url,category):
	logger.info("[letmewatchthis.py] listpelisincaratula")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	'''
	<!--SERIE-->
	<div class="pelicula_bar_border">
	<div class="pelicula_bar series iframe3">
	<ul class="tabs-nav" id="video-1687">
	<li><span style="cursor:pointer;" class="peli_ico_1 bold" onclick="location.href='/peliculas/drama/ver-pelicula-belleza-robada.html'">Belleza robada </a></span></li>
	<li><a class="peli_ico_3" style="margin-left:10px;" href="/peliculas/drama/ver-pelicula-belleza-robada.html"><span>&nbsp;Ver ficha</span></a></li>
	</ul>
	</div>
	<div id="p_ver1" class="peli_bg1" style="display:none;">
	&nbsp;
	</div>
	</div>
	'''
	'''
	<!--SERIE-->
	<div class="pelicula_bar_border">
	<div class="pelicula_bar series iframe3">
	<ul class="tabs-nav" id="video-1692">
	<li><span style="cursor:pointer;" class="peli_ico_1 bold" onclick="location.href='/peliculas/terror/ver-pelicula-bendicion-mortal.html'">Bendici&oacute;n mortal </a></span></li>
	<li><a class="peli_ico_3" style="margin-left:10px;" href="/peliculas/terror/ver-pelicula-bendicion-mortal.html"><span>&nbsp;Ver ficha</span></a></li>
	</ul>
	</div>
	<div id="p_ver1" class="peli_bg1" style="display:none;">
	&nbsp;
	</div>
	</div>
	'''
	patronvideos  = '<!--SERIE-->[^<]+'
	patronvideos += '<div class="pelicula_bar_border">[^<]+'
	patronvideos += '<div class="pelicula_bar series iframe3">[^<]+'
	patronvideos += '<ul class="tabs-nav" id="([^"]+)">[^<]+'
	patronvideos += '<li><span[^>]+>([^<]+)</a></span></li>[^<]+'
	patronvideos += '<li><a.*?href="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		scrapedplot = ""
		scrapedurl = urlparse.urljoin("http://www.letmewatchthis.es/",match[2])
		scrapedthumbnail = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	#<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
	patronvideos  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		xbmctools.addnewfolder( CHANNELNAME , "listpelisincaratula" , category , "!Página siguiente" , urlparse.urljoin(url,matches[0]) , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabetico(params, url, category):
	logger.info("[letmewatchthis.py] listalfabetico")
	
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "0-9"  ,"http://www.letmewatchthis.es/peliculas/0-9/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "A"  ,"http://www.letmewatchthis.es/peliculas/A/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "B"  ,"http://www.letmewatchthis.es/peliculas/B/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "C"  ,"http://www.letmewatchthis.es/peliculas/C/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "D"  ,"http://www.letmewatchthis.es/peliculas/D/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "E"  ,"http://www.letmewatchthis.es/peliculas/E/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "F"  ,"http://www.letmewatchthis.es/peliculas/F/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "G"  ,"http://www.letmewatchthis.es/peliculas/G/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "H"  ,"http://www.letmewatchthis.es/peliculas/H/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "I"  ,"http://www.letmewatchthis.es/peliculas/I/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "J"  ,"http://www.letmewatchthis.es/peliculas/J/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "K"  ,"http://www.letmewatchthis.es/peliculas/K/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "L"  ,"http://www.letmewatchthis.es/peliculas/L/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "M"  ,"http://www.letmewatchthis.es/peliculas/M/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "N"  ,"http://www.letmewatchthis.es/peliculas/N/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "O"  ,"http://www.letmewatchthis.es/peliculas/O/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "P"  ,"http://www.letmewatchthis.es/peliculas/P/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "Q"  ,"http://www.letmewatchthis.es/peliculas/Q/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "R"  ,"http://www.letmewatchthis.es/peliculas/R/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "S"  ,"http://www.letmewatchthis.es/peliculas/S/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "T"  ,"http://www.letmewatchthis.es/peliculas/T/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "U"  ,"http://www.letmewatchthis.es/peliculas/U/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "V"  ,"http://www.letmewatchthis.es/peliculas/V/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "W"  ,"http://www.letmewatchthis.es/peliculas/W/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "X"  ,"http://www.letmewatchthis.es/peliculas/X/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "Y"  ,"http://www.letmewatchthis.es/peliculas/Y/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listpeliconcaratula" , category , "Z"  ,"http://www.letmewatchthis.es/peliculas/Z/","","")

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabeticoseries(params, url, category):

	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "0-9"  ,"http://www.letmewatchthis.es/series/0-9/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "A"  ,"http://www.letmewatchthis.es/series/A/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "B"  ,"http://www.letmewatchthis.es/series/B/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "C"  ,"http://www.letmewatchthis.es/series/C/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "D"  ,"http://www.letmewatchthis.es/series/D/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "E"  ,"http://www.letmewatchthis.es/series/E/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "F"  ,"http://www.letmewatchthis.es/series/F/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "G"  ,"http://www.letmewatchthis.es/series/G/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "H"  ,"http://www.letmewatchthis.es/series/H/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "I"  ,"http://www.letmewatchthis.es/series/I/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "J"  ,"http://www.letmewatchthis.es/series/J/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "K"  ,"http://www.letmewatchthis.es/series/K/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "L"  ,"http://www.letmewatchthis.es/series/L/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "M"  ,"http://www.letmewatchthis.es/series/M/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "N"  ,"http://www.letmewatchthis.es/series/N/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "O"  ,"http://www.letmewatchthis.es/series/O/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "P"  ,"http://www.letmewatchthis.es/series/P/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "Q"  ,"http://www.letmewatchthis.es/series/Q/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "R"  ,"http://www.letmewatchthis.es/series/R/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "S"  ,"http://www.letmewatchthis.es/series/S/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "T"  ,"http://www.letmewatchthis.es/series/T/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "U"  ,"http://www.letmewatchthis.es/series/U/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "V"  ,"http://www.letmewatchthis.es/series/V/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "W"  ,"http://www.letmewatchthis.es/series/W/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "X"  ,"http://www.letmewatchthis.es/series/X/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "Y"  ,"http://www.letmewatchthis.es/series/Y/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "Z"  ,"http://www.letmewatchthis.es/series/Z/","","")

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listtemporadacaratula(params,url,category):
	logger.info("[letmewatchthis.py] listtemporadacaratula")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	'''
	<li>
	<a href="/series/the-middleman/temporada-1/"><img src="http://caratulas.letmewatchthis.es/series/233.jpg" alt="peli" /></a>
	<p><span class="rosa"></span></p><div class="icos_lg"><img src="http://caratulas.letmewatchthis.es/img/cont/sub.png" alt="sub" /><img src="http://caratulas.letmewatchthis.es/img/cont/megavideo.png" alt="" /> </div>                                        <p class="tit_ficha">The middleman </p>
	<p class="tem_fich">1a Temporada</p>
	</li>
	'''
	'''
	<li>
	<a href="/series/cranford-de-e-gaskell/"><img src="http://caratulas.letmewatchthis.es/series/64.jpg" alt="peli" /></a>
	<p><span class="rosa"></span></p><div class="icos_lg"><img src="http://caratulas.letmewatchthis.es/img/cont/sub.png" alt="sub" /><img src="http://caratulas.letmewatchthis.es/img/cont/megavideo.png" alt="" /><img src="http://caratulas.letmewatchthis.es/img/cont/ddirecta.png" alt="descarga directa" /> </div>                                        <p class="tit_ficha">Cranford, de E. Gaskell </p>
	</li>
	'''
	patronvideos  = '<li>[^<]+'
	patronvideos += '<a href="([^"]+)"><img src="([^"]+)"[^>]+></a>[^<]+'
	patronvideos += '<p><span class="rosa"></span></p><div class="icos_lg">(.*?)</div>[^<]+'
	patronvideos += '<p class="tit_ficha">([^<]+)</p>[^<]+'
	patronvideos += '<p class="tem_fich">([^<]+)</p>[^<]+'
	patronvideos += '</li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[3].strip() + " - " + match[4].strip()
		matchesconectores = re.compile('<img.*?alt="([^"]*)"',re.DOTALL).findall(match[2])
		conectores = ""
		for matchconector in matchesconectores:
			logger.info("matchconector="+matchconector)
			if matchconector=="":
				matchconector = "megavideo"
			conectores = conectores + matchconector + "/"
		if len(matchesconectores)>0:
			scrapedtitle = scrapedtitle + " (" + conectores[:-1] + ")"

		# Convierte desde UTF-8 y quita entidades HTML
		try:
			scrapedtitle = unicode( scrapedtitle, "utf-8" ).encode("iso-8859-1")
		except:
			pass
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)


		# procesa el resto
		scrapedplot = ""

		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = match[1]
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	#<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
	patronvideos  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		xbmctools.addnewfolder( CHANNELNAME , "listtemporadacaratula" , category , "!Página siguiente" , urlparse.urljoin(url,matches[0]) , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listserieconcaratula(params,url,category):
	logger.info("[letmewatchthis.py] listserieconcaratula")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	'''
	<li>
	<a href="/series/the-middleman/temporada-1/"><img src="http://caratulas.letmewatchthis.es/series/233.jpg" alt="peli" /></a>
	<p><span class="rosa"></span></p><div class="icos_lg"><img src="http://caratulas.letmewatchthis.es/img/cont/sub.png" alt="sub" /><img src="http://caratulas.letmewatchthis.es/img/cont/megavideo.png" alt="" /> </div>                                        <p class="tit_ficha">The middleman </p>
	<p class="tem_fich">1a Temporada</p>
	</li>
	'''
	'''
	<li>
	<a href="/series/cranford-de-e-gaskell/"><img src="http://caratulas.letmewatchthis.es/series/64.jpg" alt="peli" /></a>
	<p><span class="rosa"></span></p><div class="icos_lg"><img src="http://caratulas.letmewatchthis.es/img/cont/sub.png" alt="sub" /><img src="http://caratulas.letmewatchthis.es/img/cont/megavideo.png" alt="" /><img src="http://caratulas.letmewatchthis.es/img/cont/ddirecta.png" alt="descarga directa" /> </div>                                        <p class="tit_ficha">Cranford, de E. Gaskell </p>
	</li>
	'''
	patronvideos  = '<li>[^<]+'
	patronvideos += '<a href="([^"]+)"><img src="([^"]+)"[^>]+></a>[^<]+'
	patronvideos += '<p><span class="rosa"></span></p><div class="icos_lg">(.*?)</div>[^<]+'
	patronvideos += '<p class="tit_ficha">([^<]+)</p>[^<]+'
	patronvideos += '</li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[3].strip()
		matchesconectores = re.compile('<img.*?alt="([^"]*)"',re.DOTALL).findall(match[2])
		conectores = ""
		for matchconector in matchesconectores:
			logger.info("matchconector="+matchconector)
			if matchconector=="":
				matchconector = "megavideo"
			conectores = conectores + matchconector + "/"
		if len(matchesconectores)>0:
			scrapedtitle = scrapedtitle + " (" + conectores[:-1] + ")"

		# Convierte desde UTF-8 y quita entidades HTML
		try:
			scrapedtitle = unicode( scrapedtitle, "utf-8" ).encode("iso-8859-1")
		except:
			pass
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)


		# procesa el resto
		scrapedplot = ""

		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = match[1]
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	#<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
	patronvideos  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		xbmctools.addnewfolder( CHANNELNAME , "listserieconcaratula" , category , "!Página siguiente" , urlparse.urljoin(url,matches[0]) , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listseriesincaratula(params,url,category):
	logger.info("[letmewatchthis.py] listseriesincaratula")
	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# ------------------------------------------------------
	# Extrae las entradas
	# ------------------------------------------------------
	'''
	<!--SERIE-->
	<div class="pelicula_bar_border">
	<div class="pelicula_bar series iframe3">
	<ul class="tabs-nav" id="video-1687">
	<li><span style="cursor:pointer;" class="peli_ico_1 bold" onclick="location.href='/peliculas/drama/ver-pelicula-belleza-robada.html'">Belleza robada </a></span></li>
	<li><a class="peli_ico_3" style="margin-left:10px;" href="/peliculas/drama/ver-pelicula-belleza-robada.html"><span>&nbsp;Ver ficha</span></a></li>
	</ul>
	</div>
	<div id="p_ver1" class="peli_bg1" style="display:none;">
	&nbsp;
	</div>
	</div>
	'''
	'''
	<!--SERIE-->
	<div class="pelicula_bar_border">
	<div class="pelicula_bar series iframe3">
	<ul class="tabs-nav" id="video-1692">
	<li><span style="cursor:pointer;" class="peli_ico_1 bold" onclick="location.href='/peliculas/terror/ver-pelicula-bendicion-mortal.html'">Bendici&oacute;n mortal </a></span></li>
	<li><a class="peli_ico_3" style="margin-left:10px;" href="/peliculas/terror/ver-pelicula-bendicion-mortal.html"><span>&nbsp;Ver ficha</span></a></li>
	</ul>
	</div>
	<div id="p_ver1" class="peli_bg1" style="display:none;">
	&nbsp;
	</div>
	</div>
	'''
	patronvideos  = '<!--SERIE-->[^<]+'
	patronvideos += '<div class="pelicula_bar_border">[^<]+'
	patronvideos += '<div class="pelicula_bar series iframe3">[^<]+'
	patronvideos += '<ul class="tabs-nav" id="([^"]+)">[^<]+'
	patronvideos += '<li><span[^>]+>([^<]+)</a></span></li>[^<]+'
	patronvideos += '<li><a.*?href="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]
		scrapedtitle = scrapertools.entityunescape(scrapedtitle)
		scrapedplot = ""
		scrapedurl = urlparse.urljoin(url,match[2])
		scrapedthumbnail = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listmirrors" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae el paginador
	# ------------------------------------------------------
	#<li class="navs"><a class="pag_next" href="/peliculas-todas/2.html"></a></li>
	patronvideos  = '<li class="navs"><a class="pag_next" href="([^"]+)"></a></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		xbmctools.addnewfolder( CHANNELNAME , "listseriesincaratula" , category , "!Página siguiente" , urlparse.urljoin(url,matches[0]) , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabeticodocumentales(params, url, category):
	addfolder("0-9","http://www.letmewatchthis.es/subindices/idocumentalesnumero.html","list")
	addfolder("A","http://www.letmewatchthis.es/subindices/idocumentalesa.html","list")
	addfolder("B","http://www.letmewatchthis.es/subindices/idocumentalesb.html","list")
	addfolder("C","http://www.letmewatchthis.es/subindices/idocumentalesc.html","list")
	addfolder("D","http://www.letmewatchthis.es/subindices/idocumentalesd.html","list")
	addfolder("E","http://www.letmewatchthis.es/subindices/idocumentalese.html","list")
	addfolder("F","http://www.letmewatchthis.es/subindices/idocumentalesf.html","list")
	addfolder("G","http://www.letmewatchthis.es/subindices/idocumentalesg.html","list")
	addfolder("H","http://www.letmewatchthis.es/subindices/idocumentalesh.html","list")
	addfolder("I","http://www.letmewatchthis.es/subindices/idocumentalesi.html","list")
	addfolder("J","http://www.letmewatchthis.es/subindices/idocumentalesj.html","list")
	addfolder("K","http://www.letmewatchthis.es/subindices/idocumentalesk.html","list")
	addfolder("L","http://www.letmewatchthis.es/subindices/idocumentalesl.html","list")
	addfolder("M","http://www.letmewatchthis.es/subindices/idocumentalesm.html","list")
	addfolder("N","http://www.letmewatchthis.es/subindices/idocumentalesn.html","list")
	addfolder("O","http://www.letmewatchthis.es/subindices/idocumentaleso.html","list")
	addfolder("P","http://www.letmewatchthis.es/subindices/idocumentalesp.html","list")
	addfolder("Q","http://www.letmewatchthis.es/subindices/idocumentalesq.html","list")
	addfolder("R","http://www.letmewatchthis.es/subindices/idocumentalesr.html","list")
	addfolder("S","http://www.letmewatchthis.es/subindices/idocumentaless.html","list")
	addfolder("T","http://www.letmewatchthis.es/subindices/idocumentalest.html","list")
	addfolder("U","http://www.letmewatchthis.es/subindices/idocumentalesu.html","list")
	addfolder("V","http://www.letmewatchthis.es/subindices/idocumentalesv.html","list")
	addfolder("W","http://www.letmewatchthis.es/subindices/idocumentalesw.html","list")
	addfolder("X","http://www.letmewatchthis.es/subindices/idocumentalesx.html","list")
	addfolder("Y","http://www.letmewatchthis.es/subindices/idocumentalesy.html","list")
	addfolder("Z","http://www.letmewatchthis.es/subindices/idocumentalesz.html","list")

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listmirrors(params,url,category):
	logger.info("[letmewatchthis.py] listmirrors")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	#plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	plot = urllib.unquote_plus( params.get("plot") )

	# ------------------------------------------------------------------------------------
	# Descarga la página
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
	# Busca el thumbnail
	# ------------------------------------------------------------------------------------
	patronvideos  = '<div class="ficha_img pelicula_img">[^<]+'
	patronvideos += '<img src="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	if len(matches)>0:
		thumbnail = matches[0]
		logger.info("thumb actualizado en detalle");
	else:
		logger.info("thumb no actualizado en detalle");

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los mirrors, o a los capítulos de las series...
	# ------------------------------------------------------------------------------------
	#	url = "http://www.letmewatchthis.es/inc/mostrar_contenido.php?sec=pelis_ficha&zona=online&id=video-4637"
	#patronvideos  = '<div class="ver_des_peli iframe2">[^<]+'
	#patronvideos += '<ul class="tabs-nav" id="([^"]+)">'
	#matches = re.compile(patronvideos,re.DOTALL).findall(data)
	#data = scrapertools.cachePage("http://www.letmewatchthis.es/inc/mostrar_contenido.php?sec=pelis_ficha&zona=online&id="+matches[0])
	
	'''
	<div id="ficha_ver_peli">
	<div class="v_online">
	<h2>Ver online <span>El destino de Nunik</span></h2>
	<div class="opstions_pelicula_list">
	<div class="tit_opts" style="cursor:pointer;" onclick="location.href='http://www.letmewatchthis.es/peliculas/drama/el-destino-de-nunik_espanol-dvd-rip-megavideo-6026.html'">
	<p>Mirror 1: Megavideo</p>
	<p><span>CALIDAD: DVD-RIP | IDIOMA: ESPA&Ntilde;OL</span></p>
	<p class="v_ico"><img src="http://caratulas.letmewatchthis.es/img/cont/megavideo.png" alt="Megavideo" /></p>
	</div>
	<div class="tit_opts" style="cursor:pointer;" onclick="location.href='http://www.letmewatchthis.es/peliculas/drama/el-destino-de-nunik_espanol-dvd-rip-megavideo-6027.html'">
	<p>Mirror 2: Megavideo</p>
	<p><span>CALIDAD: DVD-RIP | IDIOMA: ESPA&Ntilde;OL</span></p>
	<p class="v_ico"><img src="http://caratulas.letmewatchthis.es/img/cont/megavideo.png" alt="Megavideo" /></p>
	</div>
	</div>
	</div>
	</div> 
	'''
	'''
	<div class="v_online">
	<h2>Ver online <span>Cantajuego 6</span></h2>
	<div class="opstions_pelicula_list"><div class="tit_opts"><a href="/peliculas/animacion-e-infantil/cantajuego-6_espanol-dvd-rip-megavideo-73371.html">
	<p>Mirror 1: Megavideo</p>
	<p><span>CALIDAD: DVD-RIP | IDIOMA: ESPA&Ntilde;OL</span></p>
	<p class="v_ico"><img src="http://caratulas.letmewatchthis.es/img/cont/megavideo.png" alt="Megavideo" /></p>
	</a></div>				</div>
	</div>
	</div><br/><div id="ficha_desc_peli">
	<div class="v_online">
	<h2 class="ico_fuego">Descargar <span>Cantajuego 6</span></h2>
	<div class="opstions_pelicula_list"><div class="tit_opts"><a href="/peliculas/animacion-e-infantil/descargar-cantajuego-6_espanol-dvd-rip-megaupload-73372.html" target="_blank">
	<p>Mirror 1: Megaupload </p>
	<p><span>CALIDAD: DVD-RIP | IDIOMA: ESPA&Ntilde;OL </span></p>
	<p class="v_ico"><img src="http://caratulas.letmewatchthis.es/img/cont/megaupload.png" alt="Megaupload" /></p>
	</a></div>
	</div>
	</div>
	</div>
	'''
	patronvideos  = '<div class="tit_opts"><a href="([^"]+)">[^<]+'
	patronvideos += '<p>([^<]+)</p>[^<]+'
	patronvideos += '<p><span>([^<]+)</span>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	
	for match in matches:
		logger.info("Encontrado iframe mirrors "+match[0])
		# Lee el iframe
		mirror = urlparse.urljoin(url,match[0].replace(" ","%20"))
		req = urllib2.Request(mirror)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		data=response.read()
		response.close()
		
		listavideos = servertools.findvideos(data)
		
		for video in listavideos:
			videotitle = video[0]
			scrapedurl = video[1]
			server = video[2]
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip()+" "+match[1]+" "+match[2]+" "+videotitle , scrapedurl , thumbnail , plot )

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------

	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	logger.info("[letmewatchthis.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def addfolder(nombre,url,accion):
	logger.info('[letmewatchthis.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	itemurl = '%s?channel=letmewatchthis&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus(nombre) , url )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)

def addvideo(nombre,url,category,server):
	logger.info('[letmewatchthis.py] addvideo( "'+nombre+'" , "' + url + '" , "'+server+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=letmewatchthis&action=play&category=%s&url=%s&server=%s' % ( sys.argv[ 0 ] , category , url , server )
	xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	logger.info('[letmewatchthis.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	itemurl = '%s?channel=letmewatchthis&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)
