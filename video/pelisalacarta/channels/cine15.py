# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cine15
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

CHANNELNAME = "cine15"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[cine15.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[cine15.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Películas - Novedades"            ,"http://www.cine15.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "peliscat"   , category , "Películas - Lista por categorías" ,"http://www.cine15.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "search"     , category , "Buscar"                           ,"","","")

	if config.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	xbmc.output("[cine15.py] search")

	keyboard = xbmc.Keyboard('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://www.cine15.com/?s="+tecleado+"&x=0&y=0"
			listvideos(params,searchUrl,category)

def performsearch(texto):
	xbmc.output("[cine15.py] performsearch")
	url = "http://www.cine15.com/?s="+texto+"&x=0&y=0"

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="videoitem">[^<]+'
	patronvideos += '<div class="ratings">[^<]+'
	patronvideos += '<div id="post-ratings[^>]+><img[^>]+><img[^>]+><img[^>]+><img[^>]+><img[^>]+></div>[^<]+'
	patronvideos += '<div id="post-ratings[^>]+><img[^>]+>&nbsp;Loading ...</div>[^<]+'
	patronvideos += '</div>[^<]+'
	patronvideos += '<div class="comments">[^<]+</div>[^<]+'
	patronvideos += '<div class="thumbnail">[^<]+'
	patronvideos += '<a href="([^"]+)" title="([^"]+)"><img style="background: url\(([^\)]+)\)" [^>]+></a>[^<]+'
	patronvideos += '</div>[^<]+'
	patronvideos += '<h2 class="itemtitle"><a[^>]+>[^<]+</a></h2>[^<]+'
	patronvideos += '<p class="itemdesc">([^<]+)</p>[^<]+'
	patronvideos += '<small class="gallerydate">([^<]+)</small>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	resultados = []

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = urlparse.urljoin(url,match[2])
		scrapedplot = match[3]

		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		resultados.append( [CHANNELNAME , "detail" , "buscador" , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot ] )
		
	return resultados

def peliscat(params,url,category):
	xbmc.output("[cine15.py] peliscat")

	# Descarga la página
	data = scrapertools.cachePage(url)

	# Extrae las entradas (carpetas)
	patronvideos  = '<li class="cat-item cat-item[^"]+"><a href="([^"]+)" title="[^"]+">([^<]+)</a>'
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
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listvideos(params,url,category):
	xbmc.output("[cine15.py] listvideos")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	'''
	<div class="home-post-wrap">
	<div class="home-post-wrap-top">
	<div class="comment-buble">
	<a href="http://www.cine15.com/pelicula/wyvern-2/#respond" title="Comentarios en Wyvern">0</a>                </div>
	<div class="date">
	<div id="post-ratings-12514" class="post-ratings"><img id="rating_12514_1" src="http://www.cine15.com/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.gif" alt="1 Star" title="1 Star" onmouseover="current_rating(12514, 1, '1 Star');" onmouseout="ratings_off(0, 0);" onclick="rate_post();" onkeypress="rate_post();" style="cursor: pointer; border: 0px;" /><img id="rating_12514_2" src="http://www.cine15.com/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.gif" alt="2 Stars" title="2 Stars" onmouseover="current_rating(12514, 2, '2 Stars');" onmouseout="ratings_off(0, 0);" onclick="rate_post();" onkeypress="rate_post();" style="cursor: pointer; border: 0px;" /><img id="rating_12514_3" src="http://www.cine15.com/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.gif" alt="3 Stars" title="3 Stars" onmouseover="current_rating(12514, 3, '3 Stars');" onmouseout="ratings_off(0, 0);" onclick="rate_post();" onkeypress="rate_post();" style="cursor: pointer; border: 0px;" /><img id="rating_12514_4" src="http://www.cine15.com/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.gif" alt="4 Stars" title="4 Stars" onmouseover="current_rating(12514, 4, '4 Stars');" onmouseout="ratings_off(0, 0);" onclick="rate_post();" onkeypress="rate_post();" style="cursor: pointer; border: 0px;" /><img id="rating_12514_5" src="http://www.cine15.com/wp-content/plugins/wp-postratings/images/stars_crystal/rating_off.gif" alt="5 Stars" title="5 Stars" onmouseover="current_rating(12514, 5, '5 Stars');" onmouseout="ratings_off(0, 0);" onclick="rate_post();" onkeypress="rate_post();" style="cursor: pointer; border: 0px;" /></div>
	<div id="post-ratings-12514-loading"  class="post-ratings-loading"><img src="http://www.cine15.com/wp-content/plugins/wp-postratings/images/loading.gif" width="16" height="16" alt="Loading ..." title="Loading ..." class="post-ratings-image" />&nbsp;Loading ...</div>
	</div>
	</div>
	<div class="thumbnail-div">
	<a href="http://www.cine15.com/pelicula/wyvern-2/" title="Wyvern">  <img src="http://www.cine15.com/wp-content/themes/cine2.0/timthumb.php?src=http://www.cine15.com/wp-content/uploads/2010/05/ipoc37.jpg&amp;h=225&amp;w=141&amp;q=80&amp;zc=1" alt=""  style="border: none;" />   </a>
	<div  id="play">
	<ul class="playimg">
	<li><a href="http://www.cine15.com/pelicula/wyvern-2/" class="boton"  ></a></li>
	</ul></div>
	<div class="post-info2">
	<h2><a href="http://www.cine15.com/pelicula/wyvern-2/" class="post-info-title" title="Permanent Link to Wyvern">
	Wyvern...                        </a></h2>
	<p class="itemdesc">Release Group: DOMiNO
	Release Name: Wyvern 2009 DVDRip  ...</p>
	<small class="gallerydate">Mayo 9, 2010</small>
	</div>
	</div>
	<img  class="footh" style="margin: 0px 0px 0px 0px; float: left;" /> </div>
	'''
	patronvideos  = '<div class="home-post-wrap">.*?<div class="thumbnail-div">[^<]+'
	patronvideos += '<a href="([^"]+)" title="([^"]+)">[^<]+<img src="http://www.cine15.com/wp-content/themes/cine2.0/timthumb.php.src=([^\&]+)\&amp'

	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		scrapedtitle = match[1]
		scrapedurl = urlparse.urljoin(url,match[0])
		scrapedthumbnail = urlparse.urljoin(url,match[2])
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente página
	patronvideos = "<span class='current'>[^<]+</span><a href='([^']+)' class='page'>"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Propiedades
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail(params,url,category):
	xbmc.output("[cine15.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# ------------------------------------------------------------------------------------
	# Busca los enlaces a videos no megavideo (playlist xml)
	# ------------------------------------------------------------------------------------
	patronvideos  = 'flashvars[^f]+file=([^\&]+)\&amp'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	
	if len(matches)>0:
		if ("xml" in matches[0]):
			data2 = scrapertools.cachePage(matches[0])
			xbmc.output("data2="+data2)
			patronvideos  = '<track>[^<]+'
			patronvideos += '<title>([^<]+)</title>[^<]+'
			patronvideos += '<location>([^<]+)</location>[^<]+'
			patronvideos += '</track>'
			matches = re.compile(patronvideos,re.DOTALL).findall(data2)
			scrapertools.printMatches(matches)

			for match in matches:
				scrapedtitle = match[0]
				scrapedurl = match[1].strip()
				scrapedthumbnail = thumbnail
				scrapedplot = plot
				if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

				# Añade al listado de XBMC
				xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , scrapedtitle + " [Directo]", scrapedurl , scrapedthumbnail, scrapedplot )
		else:
			# Añade al listado de XBMC
			xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " [Directo]", matches[0] , thumbnail, plot )
			
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

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[cine15.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
