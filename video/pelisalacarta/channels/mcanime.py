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

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

xbmc.output("[mcanime.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[mcanime.py] mainlist")

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "home"       , category , "Novedades"                             ,"http://www.mcanime.net/","","")
	xbmctools.addnewfolder( CHANNELNAME , "onlineforum", category , "Foro anime en l�nea"                   ,"http://www.mcanime.net/foro/viewforum.php?f=113","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddnovedades", category , "Descarga directa - Novedades"          ,"http://www.mcanime.net/descarga_directa/anime","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddalpha"    , category , "Descarga directa - Listado alfab�tico" ,"http://www.mcanime.net/descarga_directa/anime","","")
	xbmctools.addnewfolder( CHANNELNAME , "ddcat"      , category , "Descarga directa - Categor�as"         ,"http://www.mcanime.net/descarga_directa/anime","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def home(params,url,category):
	xbmc.output("[cine15.py] listvideos")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="release" style="background-image.url\(\'http.//images.mcanime.net/images/anime/icons/anime.gif\'\)\;">[^<]+'
	patronvideos += '<h4>[RAW] <a href="/fansubs/raws/anime/to_aru_kagaku_no_railgun/episodio_15/61434">To Aru Kagaku no Railgun Ep. 15</a> <span class="date">~ hace 2 hrs. 26 mins.</span></h4>[^<]+'
	patronvideos += '<div class="rimg"><img src="http://images.mcanime.net/images/default_anime_img.gif" width="82" height="54" alt="[Sin imagen]" /></div>[^<]+'
	patronvideos += '<div class="rtext">Bueno ahora es turno de To Aru Kagaku no Railgun ahora queda esperar versiones en ingles y espa&ntilde;ol respectivamente</div>[^<]+'
	patronvideos += '<div class="rfinfo">[^<]+'
	patronvideos += '<span class="pad">[AVI - 206MB]</span>[^<]+'
	patronvideos += '</div>[^<]+'
	patronvideos += '<div class="rflinks">[^<]+'
	patronvideos += '<span class="pad">[^<]+'
	patronvideos += '<a href="http://www.filefactory.com/file/a2aeccf/n/To_Aru_Kagaku_no_Railgun_15_RAW.avi" target="_blank"><img src="http://images.mcanime.net/images/hosters/filefactory.gif" width="16" height="16" alt="[]" title="FileFactory" /></a>[^<]+'
	patronvideos += '<a href="http://www.megaupload.com/?d=GHFTLSKY" target="_blank"><img src="http://images.mcanime.net/images/hosters/megaupload.gif" width="16" height="16" alt="[]" title="Megaupload" /></a>[^<]+'
	patronvideos += '<a href="http://www.megavideo.com/?d=GHFTLSKY" target="_blank"><img src="http://images.mcanime.net/images/hosters/megavideo.gif" width="16" height="16" alt="[]" title="Megavideo" /></a>[^<]+'
	patronvideos += '</span>[^<]+'
	patronvideos += '</div>[^<]+'
	patronvideos += '<div class="rinfo">[^<]+'
	patronvideos += '<span>Audios: <img src="http://images.mcanime.net//images/flags/jp.png" width="16" height="11" alt="Jap�n" title="Jap�n" /></span>[^<]+'
	patronvideos += '<span>Subtitulos: <img src="http://images.mcanime.net//images/flags/jp.png" width="16" height="11" alt="[JP]" title="Jap�n" /></span>[^<]+'
	patronvideos += '<span>|</span>[^<]+'
	patronvideos += '<span>Comentarios: <a href="/fansubs/raws/anime/to_aru_kagaku_no_railgun/episodio_15/61434#comentarios" class="c">4</a></span>[^<]+'
	patronvideos += '<span>|</span>[^<]+'
	patronvideos += '<span>@<a href="/fansubs/raws/1" class="f">RAWS</a></span>[^<]+'
	patronvideos += '</div>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = urlparse.urljoin(url,match[2])
		scrapedplot = match[3]
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente p�gina
	patronvideos = '<a href="([^"]+)"[^>]*>\&raquo\;</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "P�gina siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddalpha(params,url,category):
	xbmc.output("[mcanime.py] ddcat")

	# Descarga la p�gina
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

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ddcat(params,url,category):
	xbmc.output("[mcanime.py] ddcat")

	# Descarga la p�gina
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

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def onlineforum(params,url,category):
	xbmc.output("[mcanime.py] novedades")

	# Descarga la p�gina
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

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# --------------------------------------------------------------------
	# Extrae la siguiente p�gina
	# --------------------------------------------------------------------
	patronvideos  = '<a href="([^"]+)" class="next">(Siguiente &raquo;)</a>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = "P�gina siguiente"
		scrapedurl = urlparse.urljoin(url,match[0].replace("&amp;","&"))
		scrapedthumbnail = ""
		scrapedplot = ""

		# Depuracion
		xbmctools.logdebuginfo(DEBUG,scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot)
		
		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "mainlist" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )


def detail(params,url,category):
	xbmc.output("[mcanime.py] detail")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los mirrors, paginas, o cap�tulos de las series...
	# ------------------------------------------------------------------------------------
	patronvideos  = '([^"]+)" class="next">Siguiente'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	for match in matches:
		xbmc.output("Encontrada pagina siguiente")
		addfolder("Pagina siguiente",urlparse.urljoin(url,match).replace("&amp;","&"),"list")

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
		addthumbnailvideo( titulo , video[1] , thumbnailurl , descripcion , category , video[2] )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
	xbmc.output("[mcanime.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	xbmc.output("[mcanime.py] thumbnail="+thumbnail)
	xbmc.output("[mcanime.py] server="+server)
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def addfolder(nombre,url,accion):
	xbmc.output('[mcanime.py] addfolder( "'+nombre+'" , "' + url + '" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png")
	listitem.setInfo( "video", { "Title" : nombre, "Date" : str(int(time.clock()*100000000)) } )
	itemurl = '%s?channel=mcanime&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus(nombre) , urllib.quote_plus(url) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)

def addthumbnailfolder( scrapedtitle , scrapedurl , scrapedthumbnail , accion ):
	xbmc.output('[mcanime.py] addthumbnailfolder( "'+scrapedtitle+'" , "' + scrapedurl + '" , "'+scrapedthumbnail+'" , "'+accion+'")"')
	listitem = xbmcgui.ListItem( scrapedtitle, iconImage="DefaultFolder.png", thumbnailImage=scrapedthumbnail )
	listitem.setInfo( "video", { "Title" : nombre, "Date" : str(int(time.clock()*100000000)) } )
	itemurl = '%s?channel=mcanime&action=%s&category=%s&url=%s' % ( sys.argv[ 0 ] , accion , urllib.quote_plus( scrapedtitle ) , urllib.quote_plus( scrapedurl ) )
	xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=True)

def addvideo(nombre,url,category,server):
	xbmc.output('[mcanime.py] addvideo( "'+nombre+'" , "' + url + '" , "'+server+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png" )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : nombre } )
	itemurl = '%s?channel=mcanime&action=play&category=%s&url=%s&server=%s' % ( sys.argv[ 0 ] , category , url , server )
	xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=itemurl, listitem=listitem, isFolder=False)

def addthumbnailvideo(nombre,url,thumbnail,descripcion,category,server):
	xbmc.output('[mcanime.py] addvideo( "'+nombre+'" , "' + url + '" , "'+thumbnail+'" , "'+server+'")"')
	listitem = xbmcgui.ListItem( nombre, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
	listitem.setInfo( "video", { "Title" : nombre, "Plot" : descripcion } )
	itemurl = '%s?channel=mcanime&action=play&category=%s&url=%s&server=%s' % ( sys.argv[ 0 ] , category , url , server )
	xbmcplugin.addDirectoryItem( handle=int(sys.argv[ 1 ]), url=itemurl, listitem=listitem, isFolder=False)
