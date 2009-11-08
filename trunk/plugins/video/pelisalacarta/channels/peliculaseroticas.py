# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculaseroticas
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

CHANNELNAME = "peliculaseroticas"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[peliculaseroticas.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[peliculaseroticas.py] mainlist")

	url = "http://www.peliculaseroticas.net/"

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = "<a href='([^']+)'.*?src='([^']+)'.*?<span class='caption'>(.*?)<"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
        c = 1
	for match in matches:
              if c == 8 : 
		# Titulo
		try:
			scrapedtitle = unicode( match[2] , "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[2] 

		# URL
		scrapedurl = urlparse.urljoin(url,match[0])
		
		# Thumbnail
		scrapedthumbnail = match[1]
		imagen = match[1]
		# procesa el resto
		scrapeddescription = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addthumbnailfolder( CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail, "detail" )
              else: c = c + 1
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[peliculaseroticas.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	thumnbail = thumbnail
	xbmc.output("[peliculaseroticas.py] title="+title)
	xbmc.output("[peliculaseroticas.py] thumbnail="+thumbnail)

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
        detalle = "<div class='post-body entry-content'>([^<]+).*?"
        matches = re.compile(detalle,re.DOTALL).findall(data)
        #matches += thumnbail
	scrapertools.printMatches(matches)
        thumbnail = thumnbail
        plot = unicode( matches[0], "utf-8" ).encode("iso-8859-1")
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
                
                titulo = title.replace("%28"," ")
                titulo = titulo.replace("%29"," ")
        #	xbmctools.addvideo( CHANNELNAME , video[0], video[1] , category ,         #plot )
                xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Megavideo" , titulo.strip().replace("(Megavideo)","").replace("+"," ") +" - "+video[0]  , video[1] ,thumbnail, plot )
	# ------------------------------------------------------------------------------------



        # Extrae los enlaces a los vídeos (Directo)
        patronvideos = "<div class='post-body entry-content'>.*?</span><a href=\"(.*?)\" target="
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        #xbmc.output(data)
        #xbmc.output("[peliculaseroticas.py] matches="+matches[0])  
        for match in matches:
            data = scrapertools.cachePage(matches[0])
            patronvideos = '<embed type="video/divx" src="([^"]+)" custommode='
            videosdirecto = re.compile(patronvideos,re.DOTALL).findall(data)
            #xbmc.output("[peliculaseroticas.py] videosdirecto="+videosdirecto[0])
            if len(videosdirecto)>0:
              xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title+" - Directo"  , videosdirecto[0] ,thumbnail, plot )
	# ------------------------------------------------------------------------------------   

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[peliculaseroticas.py] play")

	#title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	#thumbnail = xbmc.getInfoImage( "ListItem.Thumb" )
        title = urllib.unquote_plus( params.get("title") )
        thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = urllib.unquote_plus(params["server"])
        #xbmc.executebuiltin("XBMC.ActivateWindow(contextmenu)")
        #xbmc.executebuiltin("XBMC.ActivateWindow(movieinformation)")
	xbmc.output("[peliculaseroticas.py] thumbnail="+thumbnail)
	xbmc.output("[peliculaseroticas.py] server="+server)
	
        
        #xbmc.executebuiltin("XBMC.ReplaceWindow(contextmenu)")
        xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
#mainlist(None,"","mainlist")
#detail(None,"http://impresionante.tv/ponyo.html","play")
