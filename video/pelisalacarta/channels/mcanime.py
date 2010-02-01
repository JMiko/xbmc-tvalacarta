# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para mcanime
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
import time
import xbmctools

CHANNELNAME = "mcanime"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[mcanime.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[mcanime.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "home"       , category , "Novedades"                             ,"http://www.mcanime.net/","","")
	xbmctools.addnewfolder( CHANNELNAME , "forum"      , category , "Foro anime en línea"                   ,"http://www.mcanime.net/foro/viewforum.php?f=113","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddnovedades", category , "Descarga directa - Novedades"          ,"http://www.mcanime.net/descarga_directa/anime","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddalpha"    , category , "Descarga directa - Listado alfabético" ,"http://www.mcanime.net/descarga_directa/anime","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddcat"      , category , "Descarga directa - Categorías"         ,"http://www.mcanime.net/descarga_directa/anime","","")
	xbmctools.addnewfolder( CHANNELNAME , "estrenos"   , category , "Enciclopedia - Estrenos"               ,"http://www.mcanime.net/enciclopedia/estrenos/anime","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def estrenos(params,url,category):
	xbmc.output("[mcanime.py] estrenos")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	'''
	<dl id="addRow9203" class="min row1">
	<dd class="thumb">	
	<img src="/images/anime/th_9203.jpg" width="75" height="100" alt="" />
	</dd>
	<dt><a href="/enciclopedia/anime/cobra_the_animation_rokunin_no_yuushi/9203">Cobra The Animation: Rokunin no Yuushi</a> <i>(Serie)</i></dt>
	<dd>Cobra es un conocido pirata espacial, pero decide cambiar su cara y borrar todas sus memorias. El ahora es un hombre normal, con un trabajo normal y una vida aburrida, pero comienza a recordar su verdadera identidad y sus aventuras comienzan de nuevo. <a href="/enciclopedia/anime/cobra_the_animation_rokunin_no_yuushi/9203">leer más.</a></dd>
	<dd class="small mgn"><a href="/descarga_directa/anime/cobra_the_animation_rokunin_no_yuushi/9203" class="srch_dd">Descargar&nbsp;&nbsp;<img width="14" height="14" src="/images/dds/download_icon.gif" alt="[DD]" /></a></dd>				</dl>
	'''
	patron = '<dl id="[^"]+" class="min row.">(.*?)</dl>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	
	for match in matches:
		data = match
		patron  = '<dd class="thumb">[^<]+'
		patron += '<img src="([^"]+)"[^>]+>[^<]+'
		patron += '</dd>[^<]+'
		patron += '<dt><a href="[^"]+">([^<]+)</a>\s*<i>([^<]+)</i>\s*</dt>[^<]+'
		matches2 = re.compile(patron,re.DOTALL).findall(data)
		if len(matches2)>0:
			scrapedtitle = matches2[0][1].strip() + " " + matches2[0][2].strip()
			scrapedthumbnail = urlparse.urljoin(url,matches2[0][0])
			scrapedplot = ""
			scrapedurl = ""
			if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		patron = '</dt>(.*?)<dd class="small mgn"><a href="([^"]+)"'
		matches2 = re.compile(patron,re.DOTALL).findall(data)
		if len(matches2)>0:
			try:
				scrapedplot = unicode( matches2[0][0].strip(), "utf-8" ).encode("iso-8859-1")
			except:
				scrapedplot = matches2[0][0].strip()
			scrapedplot = scrapertools.htmlclean(scrapedplot)
			scrapedplot = scrapedplot.replace("\n"," ")
			scrapedplot = scrapedplot.replace("\r"," ")
			scrapedplot = scrapedplot.replace("\r\n"," ")
			
			scrapedurl = urlparse.urljoin(url,matches2[0][1])

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "ddseriedetail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def home(params,url,category):
	xbmc.output("[mcanime.py] listvideos")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="release" style="background-image.url\(\'([^\']+)\'\)\;">[^<]+'
	patronvideos += '<h4>([^<]+)<a href="([^"]+)">([^<]+)</a> <span class="date">([^<]+)</span></h4>[^<]+'
	patronvideos += '<div class="rimg"><img src="([^"]+)"[^>]+></div>[^<]+'
	patronvideos += '<div class="rtext">(.*?)</div>[^<]+'
	patronvideos += '<div class="rfinfo">(.*?)</div>[^<]+'
	patronvideos += '<div class="rflinks">(.*?)</div>[^<]+'
	patronvideos += '<div class="rinfo">(.*?)</div>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		if match[0].endswith("anime.gif"):
			scrapedtitle = match[3].strip() + " " + match[1].strip() + " (" + match[4] + ")"
			scrapedurl = urlparse.urljoin(url,match[2])
			scrapedthumbnail = urlparse.urljoin(url,match[5])
			scrapedplot = scrapertools.htmlclean(match[6])
			scrapedextra = match[8]
			if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

			# Añade al listado de XBMC
			xbmctools.addnewfolderextra( CHANNELNAME , "homedetail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot , scrapedextra )

	# Extrae la marca de siguiente página
	patronvideos = '<span class="next"><a href="([^"]+)">Anteriores</a>...</span>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "home" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def homedetail(params,url,category):
	xbmc.output("[mcanime.py] homedetail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	extradata = urllib.unquote_plus( params.get("extradata") )

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(extradata)

	for video in listavideos:
		videotitle = video[0]
		url = video[1]
		server = video[2]
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddnovedades(params,url,category):
	xbmc.output("[mcanime.py] ddnovedades")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<ul class="dd_row">[^<]+'
	patronvideos += '<li class="dd_type dd_anime"><img[^>]+></li>[^<]+'
	patronvideos += '<li class="dd_update"><img[^>]+>([^<]+)</li>[^<]+'
	patronvideos += '<li class="dd_update"><a[^>]+>[^<]+</a></li>[^<]+'
	patronvideos += '<li class="dd_title">[^<]+'
	patronvideos += '<h5><a href="([^"]+)">([^<]+)</a></h5>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[2].strip() + " ("+match[0].strip()+")"
		scrapedurl = urlparse.urljoin(url,match[1])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "ddpostdetail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente página
	patronvideos = '<span class="current">[^<]+</span><a href="([^"]+)">[^<]+</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "ddnovedades" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddalpha(params,url,category):
	xbmc.output("[mcanime.py] ddcat")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<a href="(/descarga_directa/anime/lista/[^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "ddlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddcat(params,url,category):
	xbmc.output("[mcanime.py] ddcat")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<a href="(/descarga_directa/anime/genero/[^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "ddlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddlist(params,url,category):
	xbmc.output("[mcanime.py] ddcat")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<li class="dd_title"><h5><a href="([^"]+)">(.*?)</a>\s*<i>([^<]+)</i>\s*</h5></li>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Atributos
		scrapedtitle = match[1].strip().replace("<b>","").replace("</b>","")
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "ddseriedetail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddseriedetail(params,url,category):
	xbmc.output("[mcanime.py] ddseriedetail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Foto de la serie de la enciclopedia
	patron = '<img src="([^"]+)" width="300".*?class="title_pic" />'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		thumbnail = matches[0]
	xbmc.output("[mcanime.py] thumbnail="+thumbnail)

	# Argumento
	patron = '<h6>Sinopsis.*?</h6>(.*?)<h6>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		plot = matches[0]
		plot = plot.replace("\n"," ")
		plot = plot.replace("\r"," ")
		plot = plot.replace("\r\n"," ")
		plot = plot.strip()
		plot = scrapertools.htmlclean(matches[0])
	xbmc.output("[mcanime.py] plot="+plot)

	# Aportaciones de los usuarios
	patron  = '<h6 class="m">Por los Usuarios</h6>[^<]+'
	patron += '<div id="user_actions">(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	
	if len(matches)>0:
		data = matches[0]
		#xbmc.output("[mcanime.py] data="+data)
		patron = '<ul class="dd_row">[^<]+'
		patron += '<li class="dd_type"><img[^>]+></li>[^<]+'
		patron += '<li class="dd_update"> <img[^>]+>([^<]+)</li>[^<]+'
		patron += '<li class="dd_title">[^<]+'
		patron += '<h5><a href="([^"]+)">([^<]+)</a></h5>'
		matches = re.compile(patron,re.DOTALL).findall(data)

		for match in matches:
			# Atributos
			scrapedtitle = match[2].strip()+" ("+match[0].strip()+")"
			scrapedurl = urlparse.urljoin(url,match[1])
			scrapedthumbnail = thumbnail
			scrapedplot = plot
			if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

			# Añade al listado de XBMC
			xbmctools.addnewfolder( CHANNELNAME , "ddpostdetail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def ddpostdetail(params,url,category):
	xbmc.output("[mcanime.py] ddpostdetail")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" ).encode("iso-8859-1")
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Foto de la serie de la enciclopedia
	patron = '<img src="([^"]+)" width="300".*?class="title_pic" />'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		thumbnail = matches[0]
	
	# Argumento - texto del post
	patron = '<div id="download_detail">(.*?)</div>'
	matches = re.compile(patron,re.DOTALL).findall(data)
	if len(matches)>0:
		plot = scrapertools.htmlclean(matches[0])
		plot = plot.replace("\r\n"," ")
		plot = plot.replace("\r"," ")
		plot = plot.replace("\n"," ")
		plot = plot.strip()

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	i = 1

	for video in listavideos:
		try:
			fulltitle = unicode( title.strip() + " (%d) " + video[0], "utf-8" ).encode("iso-8859-1")
		except:
			fulltitle = title.strip() + " (%d) " + video[0]
		fulltitle = fulltitle % i
		i = i + 1
		url = video[1]
		server = video[2]
		#xbmc.output("videotitle="+urllib.quote_plus( videotitle ))
		#xbmc.output("plot="+urllib.quote_plus( plot ))
		#plot = ""
		#xbmc.output("title="+urllib.quote_plus( title ))

		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , fulltitle , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def forum(params,url,category):
	xbmc.output("[mcanime.py] forum")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# --------------------------------------------------------------------
	# Extrae las entradas del foro (series / pelis)
	# --------------------------------------------------------------------
	patronvideos  = '<ul class="topic_row">[^<]+<li class="topic_type"><img.*?'
	patronvideos += '<li class="topic_title"><h5><a href="([^"]+)">([^<]+)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Extrae
		try:
			scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0].replace("&amp;","&"))
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		xbmctools.logdebuginfo(DEBUG,scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "forumdetail" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# --------------------------------------------------------------------
	# Extrae la siguiente página
	# --------------------------------------------------------------------
	patronvideos  = '<a href="([^"]+)" class="next">(Siguiente &raquo;)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,match[0].replace("&amp;","&"))
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		xbmctools.logdebuginfo(DEBUG,scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot)
		
		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "forum" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def forumdetail(params,url,category):
	xbmc.output("[mcanime.py] forumdetail")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los mirrors, paginas, o capítulos de las series...
	# ------------------------------------------------------------------------------------
	patronvideos  = '([^"]+)" class="next">Siguiente'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	for match in matches:
		xbmc.output("Encontrada pagina siguiente")
		xbmctools.addnewfolder( CHANNELNAME , "list" , category , "Pagina siguiente" ,urlparse.urljoin(url,match).replace("&amp;","&"),"","")

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	# Saca el cuerpo del post
	#logFile.info("data="+data)
	#patronvideos  = '<div class="content">.*?<div class="poster">.*?</div>(.*?)</div>'
	patronvideos  = '<div class="content">(.*?)<div class="content">'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	datapost=""
	if len(matches)>0:
		datapost=matches[0]
	else:
		datapost = ""
	#logFile.info("dataPost="+dataPost)

	# Saca el thumbnail
	patronvideos  = '<img src="([^"]+)"'
	matches = re.compile(patronvideos,re.DOTALL).findall(datapost)
	thumbnailurl=""
	xbmc.output("thumbnails")
	for match in matches:
		xbmc.output(match)
	if len(matches)>0:
		thumbnailurl=matches[0]

	patronvideos  = '<img.*?>(.*?)<a'
	matches = re.compile(patronvideos,re.DOTALL).findall(datapost)
	descripcion = ""
	if len(matches)>0:
		descripcion = matches[0]
		descripcion = descripcion.replace("<br />","")
		descripcion = descripcion.replace("<br/>","")
		descripcion = descripcion.replace("\r","")
		descripcion = descripcion.replace("\n"," ")
		descripcion = re.sub("<[^>]+>"," ",descripcion)
	xbmc.output("descripcion="+descripcion)
	
	listavideos = servertools.findvideos(datapost)
	
	for video in listavideos:
		titulo = descripcion = re.sub("<[^>]+>","",video[0])
		url = video[1]
		thumbnail = thumbnailurl
		plot = descripcion
		server = video[2]
		xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , titulo , url , thumbnail , plot )

	# ------------------------------------------------------------------------------------

	# Cierra el directorio
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	xbmc.output("[mcanime.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

