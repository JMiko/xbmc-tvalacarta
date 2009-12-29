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
            
        if url == "":
	  url = "http://www.peliculaseroticas.net/"

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="polaroid[^>]+><a href="([^"]+)">'
        patronvideos += '<img src="([^"]+)"/>'
        patronvideos += '</a>([^<]+)<'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
        #c = 1
	for match in matches:
              #if c == 8 : 
		# Titulo
                
		try:
			scrapedtitle = unicode( match[2] , "utf-8" ).encode("iso-8859-1")
		except:
			scrapedtitle = match[2] 
                scrapedtitle = scrapedtitle.replace('&#191;','¿')
		# URL
		scrapedurl = urlparse.urljoin(url,match[0])
		
		# Thumbnail
		scrapedthumbnail = match[1]
                scrapedthumbnail = scrapedthumbnail.replace(" ","")
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

        # Extrae la marca de siguiente página

               
	patronvideos  = "<a class='blog-pager-older-link' href='([^']+)"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0 and url != matches:
		scrapedtitle = "Más Películas"
		scrapedurl = urlparse.urljoin(url,matches[0])
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "mainlist" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )        

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

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
        plot = plot.replace('&#8220;','"')
        plot = plot.replace('&#8221;','"')
        plot = plot.replace('&#8230;','...')
        plot = plot.replace("&nbsp;","")
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)

	for video in listavideos:
                
                titulo = title.replace("%28"," ")
                titulo = titulo.replace("%29"," ")
                server = video[2]
        #	xbmctools.addvideo( CHANNELNAME , video[0], video[1] , category ,         #plot )
                xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , titulo.strip().replace("(Megavideo)","").replace("+"," ") +" - "+video[0]  , video[1] ,thumbnail, plot )
	# ------------------------------------------------------------------------------------



       # Extrae los enlaces a los vídeos (Directo)

         # Extrae los videos para el servidor mystream.to

        patronvideos = '(http://www.mystream.to/.*?)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        #xbmc.output(data)
        #xbmc.output("[peliculaseroticas.py] matches="+matches[0])  
        if len(matches)>0:
            data = scrapertools.cachePage(matches[0])
            patronvideos = 'flashvars" value="file=(.*?)"'
            videosdirecto = re.compile(patronvideos,re.DOTALL).findall(data)
            #xbmc.output("[peliculaseroticas.py] videosdirecto="+videosdirecto[0])
            if len(videosdirecto)>0:
              xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title+" - Directo con mystream.to"  , videosdirecto[0] ,thumbnail, plot )
       
        patronvideos = "<div class='post-body entry-content'>.*?</span><a href=\"(.*?)\" target="
        matches = re.compile(patronvideos,re.DOTALL).findall(data) 
        if len(matches)>0: 
        # extrae los videos para servidor movshare
              data = scrapertools.cachePage(matches[0])
              patronvideos ='param name="src" value="http://stream.movshare.net/(.*?).avi'   
              videosdirecto = re.compile(patronvideos,re.DOTALL).findall(data)
            #xbmc.output("[peliculaseroticas.py] videosdirecto="+videosdirecto[0])
              if len(videosdirecto)>0:
                 import movshare
                 mediaurl = "http://www.movshare.net/video/" + videosdirecto[0]
                 xbmc.output("[peliculaseroticas.py] mediaurl = "+ mediaurl)
                 mediaurl = movshare.getvideo(mediaurl)
                 xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title+" - Video en movshare"  , mediaurl ,thumbnail, plot )



             # extrae los videos para servidor stagevu
              patronvideos ="http://stagevu.com/.*?uid=(.*?)'"   
              videosdirecto = re.compile(patronvideos,re.DOTALL).findall(data)
            #xbmc.output("[peliculaseroticas.py] videosdirecto="+videosdirecto[0])
              if len(videosdirecto)>0:
                 import stagevu
                 mediaurl = "http://stagevu.com/video/" + videosdirecto[0]
                 xbmc.output("[peliculaseroticas.py] mediaurl = "+ mediaurl)
                 mediaurl = stagevu.Stagevu(mediaurl)
                 xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title+" - Video en stagevu"  , mediaurl ,thumbnail, plot ) 
                
	# --------------------------------------------------------------------------------             

        # extrae los videos para servidor myspacecdn      
  
        data = scrapertools.cachePage(url)
        patronvideos = 'flashvars.*?file=(.*?.flv).*?'
        videosdirecto = re.compile(patronvideos,re.DOTALL).findall(data)
        #xbmc.output("[peliculaseroticas.py] videosdirecto="+videosdirecto[0])
        if len(videosdirecto)>0:
              xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title+" - Video en myspacecdn"  , videosdirecto[0] ,thumbnail, plot )
	# --------------------------------------------------------------------------------
        
        # extrae los videos para del servidor adnstream.com
          
        patronvideos = '<a href=\"http://www.adnstream.tv/video/(.*?)/.*?"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        #xbmc.output("[peliculaseroticas.py] matches="+matches[0])
        if len(matches)>0:
              mediaurl = "http://www.adnstream.tv/get_playlist.php?lista=video&param="+matches[0]+"&c=463"
              xbmc.output(" mediaurl -------"+mediaurl)
              data = scrapertools.cachePage(mediaurl)
              #xbmc.output("[peliculaseroticas.py] data="+data)
              patronvideos = '</description>.*?<enclosure type="video/x-flv" url="(.*?)"'
              matchvideo = re.compile(patronvideos,re.DOTALL).findall(data)
              if len(matchvideo)>0:
                 xbmc.output("[peliculaseroticas.py] videoflv = "+ matchvideo[0])
                 xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title+" - Video en adnstream.tv"  , matchvideo[0] ,thumbnail, plot )
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
