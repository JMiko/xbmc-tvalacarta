# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para divxonline, por ErManitu
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

CHANNELNAME = "divxonline"

# Esto permite su ejecución en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[divxonline.py] init")

DEBUG = False

def mainlist(params,url,category):
    xbmc.output("[divxonline.py] mainlist")

    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Acción" , "http://www.divxonline.info/peliculas/50/accion-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Animación" , "http://www.divxonline.info/peliculas/53/animacion-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Anime" , "http://www.divxonline.info/peliculas/51/anime-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Aventura" , "http://www.divxonline.info/peliculas/52/aventura-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Bélicas" , "http://www.divxonline.info/peliculas/95/belicas-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Ciencia Ficción" , "http://www.divxonline.info/peliculas/55/ciencia-ficcion-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine Clásico" , "http://www.divxonline.info/peliculas/58/cine-clasico-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Cine español" , "http://www.divxonline.info/peliculas/57/cine-espa%C3%B1ol-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Clásicos Disney" , "http://www.divxonline.info/peliculas/59/clasicos-disney-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Comedias" , "http://www.divxonline.info/peliculas/60/comedias-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Documentales" , "http://www.divxonline.info/peliculas/54/documentales-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Drama" , "http://www.divxonline.info/peliculas/62/drama-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Infantil" , "http://www.divxonline.info/peliculas/63/infantil-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Musicales" , "http://www.divxonline.info/peliculas/64/musicales-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Suspense" , "http://www.divxonline.info/peliculas/65/suspense-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Terror" , "http://www.divxonline.info/peliculas/66/terror-megavideo/" , "", "" )
    xbmctools.addnewfolder( CHANNELNAME , "movielist" , CHANNELNAME , "Western" , "http://www.divxonline.info/peliculas/67/western-megavideo/" , "", "" )

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def movielist(params,url,category):
    xbmc.output("[divxonline.py] mainlist")

    # Descarga la página
    data = scrapertools.cachePage(url)
    #xbmc.output(data)

    # Obtiene todas las páginas de la categoría
    match0 = re.search('Ver página:(.*?)</p>',data)
    trozo = match0.group(1)
    xbmc.output(trozo)

    patronpaginas = '<a href="([^"]+)"'
    matches = re.compile(patronpaginas,re.DOTALL).findall(trozo)
    scrapertools.printMatches(matches)
    data = ''
    for match in matches:
	urlpage = urlparse.urljoin(url,match)
	xbmc.output(match)
	xbmc.output(urlpage)
	data += scrapertools.cachePage(urlpage)

    # Extrae las entradas (carpetas)
    patronvideos  = '<li><a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    for match in matches:
	# Titulo
	scrapedtitle = match[1]

	# URL
	scrapedurl = urlparse.urljoin(url,match[0]) # url de la ficha divxonline
	scrapedurl = scrapedurl.replace("pelicula","pelicula-divx") # url de la página de reproducción

	# Thumbnail
	#scrapedthumbnail = urlparse.urljoin(url,match[1])
	scrapedthumbnail = ""

	# procesa el resto
	scrapeddescription = ""

	# Depuracion
	if (DEBUG):
	    xbmc.output("scrapedtitle="+scrapedtitle)
	    xbmc.output("scrapedurl="+scrapedurl)
	    xbmc.output("scrapedthumbnail="+scrapedthumbnail)

	# Añade al listado de XBMC
	xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
    xbmc.output("[divxonline.py] detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    xbmc.output("[divxonline.py] title="+title)
    xbmc.output("[divxonline.py] thumbnail="+thumbnail)

    # url del frame con los videos
    data2 = scrapertools.cachePage(url) # descarga pagina de reproduccion
    match = re.search('</p><iframe src="(.*?)"',data2) # el link esta dentro de un iframe
    url = match.group(1)
    #xbmc.output(url)

    # Descarga la página
    data = scrapertools.cachePage(url)
    #xbmc.output(data)

    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)

    for video in listavideos:
        xbmctools.addvideo( CHANNELNAME , title+" - "+video[0] , video[1] , category , video[2] )
    # ------------------------------------------------------------------------------------

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
    xbmc.output("[divxonline.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]
    xbmc.output("[divxonline.py] thumbnail="+thumbnail)
    xbmc.output("[divxonline.py] server="+server)

    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

#mainlist(None,"","mainlist")
#detail(None,"http://impresionante.tv/ponyo.html","play")



