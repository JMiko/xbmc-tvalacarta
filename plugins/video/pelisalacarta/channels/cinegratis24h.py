# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinegratis24h.com by Bandavi
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

CHANNELNAME = "cinegratis24h"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[cinegratis24h.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[cinegratis24h.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ultimas Películas Subidas"    ,"http://www.cinegratis24h.com/","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Estrenos","http://www.cinegratis24h.net/index.php?module=estrenos","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Series","http://www.cinegratis24h.net/index.php?module=series","","")
	xbmctools.addnewfolder( CHANNELNAME , "ListadoTotal" , category , "Listado Completo"        ,"http://www.cinegratis24h.com/","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Buscar","http://www.cinegratis24h.net/index.php?module=documentales","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ListadoTotal(params,url,category):
	xbmc.output("[peliculas24h.py] ListadoTotal")

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Patron de las entradas
	patron = "<a dir='ltr' href='([^']+)'>(.*?)</a>"
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# Añade las entradas encontradas
	for match in matches:
		# Atributos
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): xbmc.output("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el título, desactiva la ordenación, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
        

def listvideos(params,url,category):
	xbmc.output("[cinegratis24h.py] listvideos")

	if url=="":
		url = "http://www.cinegratis24h.com/"
                
	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)


	# Extrae las entradas (carpetas)
	patronvideos  = "<h1 class='post-title entry-title'>.*?<a href='([^']+)'"                # URL
	patronvideos += ">(.*?)</a>[^<]+"                                                        # TITULO
	patronvideos += '</h1>[^<]+</div>.*?<div class=[^>]+>[^<]+'
	patronvideos += '</div>[^<]+<div class=[^>]+>.*?href="[^"]+"><img '                    
	patronvideos += 'style=.*?src="([^"]+)".*?alt=.*?bold.*?>(.*?)</div>'                  # IMAGEN , DESCRIPCION
	#patronvideos += '.*?flashvars="file=(.*?flv)\&amp'                                      # VIDEO FLV 
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[1]
		# URL
		scrapedurl = match[0]
		# Thumbnail
		scrapedthumbnail = match[2]
                #scrapedthumbnail = scrapedthumbnail.replace(" ","")
		# Argumento
		scrapedplot = match[3]
		scrapedplot = re.sub("<[^>]+>"," ",scrapedplot)
		scrapedplot = scrapedplot.replace('&#8220;','"')
		scrapedplot = scrapedplot.replace('&#8221;','"')
		scrapedplot = scrapedplot.replace('&#8230;','...')
		scrapedplot = scrapedplot.replace("&nbsp;","")

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente página
	patronvideos  = "<a class='blog-pager-older-link' href='([^']+)' id="
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = matches[0]
		scrapedthumbnail = ""
		scrapedplot = ""
		xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def detail(params,url,category):
	xbmc.output("[cinegratis24h.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
        patrondescrip = '<a onblur=.*?src="([^"]+)" border.*?</a><.*?><.*?>(Sinopsis:<br />.*?)</div>'
        matches = re.compile(patrondescrip,re.DOTALL).findall(data)
        if DEBUG:
			if len(matches)>0:
				for match in matches:
					thumbnail = match[0]
					descripcion = match[1]
					descripcion = descripcion.replace('&#8220;','"')
					descripcion = descripcion.replace('&#8221;','"')
					descripcion = descripcion.replace('&#8230;','...')
					descripcion = descripcion.replace("&nbsp;","")
					descripcion = descripcion.replace("<br/>","")
					descripcion = descripcion.replace("\r","")
					descripcion = descripcion.replace("\n"," ")
					descripcion = descripcion.replace("\t"," ")
					descripcion = re.sub("<[^>]+>"," ",descripcion)
					descripcion = acentos(descripcion)
					try :
						plot = unicode( descripcion, "utf-8" ).encode("iso-8859-1")
					except:
						plot = descripcion
				                    
                   
          
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	#listavideos = servertools.findvideos(data)

	#for video in listavideos:
	#	videotitle = video[0]
	#	url = video[1]
	#	server = video[2]
	#	xbmctools.addnewvideo( CHANNELNAME , "play" , category , server , title.strip() + " - " + videotitle , url , thumbnail , plot )
	# ------------------------------------------------------------------------------------
        #--- Busca los videos Directos
        patronvideos = 'flashvars="file=([^\&]+)\&amp'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
        if len(matches)>0:
          if ("xml" in matches[0]):  
            #data = scrapertools.cachePage(matches[0])
            req = urllib2.Request(matches[0])
            try:
		response = urllib2.urlopen(req)
	    except:
                xbmctools.alertnodisponible()
                return
            data=response.read()
	    response.close()
            #xbmc.output("archivo xml :"+data)
            newpatron = '<location>(.*?)</location>'
            newmatches = re.compile(newpatron,re.DOTALL).findall(data)
            parte = 0
            for match in newmatches:
              if len(match)>0:
                parte = parte + 1
                xbmc.output(" videos = "+match)
                xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " parte "+str(parte), match , thumbnail , plot )
                 
          else:
                xbmc.output(" matches = "+matches[0])
                xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " (FLV)", matches[0] , thumbnail , plot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[cinegratis24h.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def acentos(title):

        title = title.replace("Ã‚Â", "")
        title = title.replace("ÃƒÂ©","é")
        title = title.replace("ÃƒÂ¡","á")
        title = title.replace("ÃƒÂ³","ó")
        title = title.replace("ÃƒÂº","ú")
        title = title.replace("ÃƒÂ­","í")
        title = title.replace("ÃƒÂ±","ñ")
        title = title.replace("Ã¢â‚¬Â", "")
        title = title.replace("Ã¢â‚¬Å“Ã‚Â", "")
        title = title.replace("Ã¢â‚¬Å“","")
        title = title.replace("Ã©","é")
        title = title.replace("Ã¡","á")
        title = title.replace("Ã³","ó")
        title = title.replace("Ãº","ú")
        title = title.replace("Ã­","í")
        title = title.replace("Ã±","ñ")
        title = title.replace("Ãƒâ€œ","Ó")
        return(title)
        
        
        