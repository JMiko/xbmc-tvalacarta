# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tumejortv
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

CHANNELNAME = "tumejortv"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[tumejortv.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[tumejortv.py] mainlist")
	xbmctools.addnewfolder( CHANNELNAME , "newlist" , CHANNELNAME , "Novedades" , "http://www.tumejortv.com/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "moviecategorylist" , CHANNELNAME , "Películas - Por categorías" , "http://www.tumejortv.com/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "moviealphalist" , CHANNELNAME , "Películas - Por orden alfabético" , "http://www.tumejortv.com/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "serienewlist" , CHANNELNAME , "Series - Novedades" , "http://www.tumejortv.com/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "seriealllist" , CHANNELNAME , "Series - Todas" , "http://www.tumejortv.com/" , "", "" )
	xbmctools.addnewfolder( CHANNELNAME , "seriealphalist" , CHANNELNAME , "Series - Por orden alfabético" , "http://www.tumejortv.com/" , "", "" )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Listado de novedades de la pagina principal
def newlist(params,url,category):
	xbmc.output("[tumejortv.py] movielist")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	patron  = '<div class="item " style="clear:both;">[^<]+'
	patron += '<div class="covershot[^<]+'
	patron += '<a href="([^"]+)"[^<]+<img src="([^"]+)"[^<]+</a>[^<]+'
	patron += '</div>[^<]+'
	patron += '<div class="post-title">[^<]+'
	patron += '<h3><a[^<]+>(.*?)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[2]
		scrapedtitle = scrapedtitle.replace("<span class=\'smallTitle'>","(")
		scrapedtitle = scrapedtitle.replace("</span>",")")
		scrapedurl = match[0]
		scrapedthumbnail = match[1]
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae la página siguiente
	# ------------------------------------------------------
	patron = '<a href="([^"]+)" >&raquo;</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = match
		scrapedthumbnail = ""
		scrapeddescription = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "newlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Listado de películas de una categoria / letra
def shortlist(params,url,category):
	xbmc.output("[tumejortv.py] shortlist")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#<li><div class="movieTitle">Doraemon Y Los 7 Magos (2008) - DVD-RIP</div><div class="covershot"><a href="http://www.tumejortv.com/peliculas-online-es/infantiles/doraemon-y-los-7-magos-2008-dvd-rip-31-07-2009.html" title="Doraemon Y Los 7 Magos (2008) - DVD-RIP"><img src="http://imagenes.tumejortv.com//8098.jpg" alt="Doraemon Y Los 7 Magos (2008) - DVD-RIP"/></a></div></li>
	patron  = '<li><div class="movieTitle">[^<]+</div><div class="covershot">'
	patron += '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"[^>]+></a></div></li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = match[2]
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae la página siguiente
	# ------------------------------------------------------
	patron = '<a href="([^"]+)" >&raquo;</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = match
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "shortlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Listado de series de una letra
def shortlistserie(params,url,category):
	xbmc.output("[tumejortv.py] shortlistserie")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#<li><div class="covershot"><a href="http://www.tumejortv.com/series-tv-online/abducidos-taken" title="Abducidos (Taken)"><img src="http://imagenes.tumejortv.com/series/157.jpg" alt="Abducidos (Taken)"/></a></div></li>
	patron  = '<li><div class="covershot"><a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"[^>]+></a></div></li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = match[2]
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detailserie" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# ------------------------------------------------------
	# Extrae la página siguiente
	# ------------------------------------------------------
	patron = '<a href="([^"]+)" >&raquo;</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Pagina siguiente"
		scrapedurl = match
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "shortlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Listado de categorias de películas, de la caja derecha de la home
def moviecategorylist(params,url,category):
	
	xbmc.output("[tumejortv.py] moviecategorylist")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#<li class="cat-item cat-item-94"><a href="http://www.tumejortv.com/peliculas-online-es/accion" title="Ver todos los videos de Acción">Acción</a></li>
	patron  = '<li class="cat-item[^<]+<a href="(http\:\/\/www\.tumejortv\.com\/peliculas\-online\-es\/[^"]+)"[^>]+>([^<]+)</a></li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "shortlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Listado de letras iniciales de película, de la caja derecha de la home
def moviealphalist(params,url,category):
	
	xbmc.output("[tumejortv.py] moviealphalist")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#<a href="http://www.tumejortv.com/peliculas-es-con-letra-a" title="Pel&iacute;culas - Es con la letra a" class="listados_letras">a</a> - 
	patron  = '<a href="(http\:\/\/www\.tumejortv\.com\/peliculas-es-con-letra-[^"]+)".*?class="listados_letras">([^<]+)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "shortlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Listado de letras iniciales de series, de la caja derecha de la home
def seriealphalist(params,url,category):
	
	xbmc.output("[tumejortv.py] seriealphalist")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#<a href="http://www.tumejortv.com/series-con-letra-a" title="Series con la letra a" class="listados_letras">a</a>
	patron  = '<a href="(http\:\/\/www\.tumejortv\.com\/series-con-letra-[^"]+)".*?class="listados_letras">([^<]+)</a>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "shortlistserie" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Listado de series actualizadas, de la caja derecha de la home
def serienewlist(params,url,category):
	
	xbmc.output("[tumejortv.py] serienewlist")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#<span><a href="http://www.tumejortv.com/series-tv-online/ranma-%c2%bd/ranma-%c2%bd-temporada-1" title="Ranma ½"><img src="http://imagenes.tumejortv.com//series/948.jpg" alt="Ranma ½"  /></a></span>
	patron  = '<span><a href="([^"]+)" title="([^"]+)"><img src="([^"]+)".*?</span>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = match[2]
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detailserie" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Listado de todas las series, de la caja derecha de la home
def seriealllist(params,url,category):
	
	xbmc.output("[tumejortv.py] seriealllist")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	# Extrae las películas
	# ------------------------------------------------------
	#<li class="cat-item cat-item-136"><a href="http://www.tumejortv.com/series-tv-online/24" title="Ver todos los videos de 24">24</a></li>
	patron  = '<li class="cat-item[^<]+<a href="(http\:\/\/www\.tumejortv\.com\/series\-tv\-online\/[^"]+)"[^>]+>([^<]+)</a></li>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		if DEBUG:
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)
			xbmc.output("scrapedplot="+scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detailserie" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Detalle de un vídeo (peli o capitulo de serie), con los enlaces
def detail(params,url,category):
	xbmc.output("[tumejortv.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = ""

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	listavideos = servertools.findvideos(data)
	
	for video in listavideos:
		xbmctools.addnewvideo( CHANNELNAME , "play" , CHANNELNAME , video[2] , title + " (" + video[2] + ")" , video[1] , thumbnail, plot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

# Detalle de una serie, con sus capítulos
def detailserie(params,url,category):
	xbmc.output("[tumejortv.py] detailserie")

	# ------------------------------------------------------
	# Descarga la página
	# ------------------------------------------------------
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------
	#<ul class="linksListados">
	#<li><a href="http://www.tumejortv.com/series-tv-online/babylon-5/babylon-5-temporada-1/capitulo-122-15-15-04-2009.html">Babylon 5, Babylon 5 Temporada 1, Capitulo 122</a></li>
	patron  = '<ul class="linksListados">(.*?)</ul>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if DEBUG:
		scrapertools.printMatches(matches)

	for match in matches:
		patron2 = '<li><a href="([^"]+)">([^<]+)</a></li>'
		matches2 = re.compile(patron2,re.DOTALL).findall(match)
		if DEBUG:
			scrapertools.printMatches(matches2)

		for match2 in matches2:
			scrapedtitle = match2[1]
			scrapedurl = match2[0]
			scrapedthumbnail = ""
			scrapedplot = ""

			# Depuracion
			if DEBUG:
				xbmc.output("scrapedtitle="+scrapedtitle)
				xbmc.output("scrapedurl="+scrapedurl)
				xbmc.output("scrapedthumbnail="+scrapedthumbnail)
				xbmc.output("scrapedplot="+scrapedplot)

			# Añade al listado de XBMC
			xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

# Reproducir un vídeo
def play(params,url,category):
	xbmc.output("[tumejortv.py] play")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	server = urllib.unquote_plus( params.get("server") )

	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
