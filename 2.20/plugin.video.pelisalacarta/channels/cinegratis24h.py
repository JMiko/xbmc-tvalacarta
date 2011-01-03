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
import xmltoplaylist
import config
import logger

CHANNELNAME = "cinegratis24h"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[cinegratis24h.py] init")

DEBUG = True

def mainlist(params,url,category):
	logger.info("[cinegratis24h.py] mainlist")

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ultimas Pel�culas Subidas"    ,"http://www.cinegratis24h.com/search?max-results=50","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Estrenos","http://www.cinegratis24h.net/index.php?module=estrenos","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Series","http://www.cinegratis24h.net/index.php?module=series","","")
	xbmctools.addnewfolder( CHANNELNAME , "ListadoTotal" , category , "Listado Completo"        ,"http://www.cinegratis24h.com/","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Buscar","http://www.cinegratis24h.net/index.php?module=documentales","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def ListadoTotal(params,url,category):
	logger.info("[peliculas24h.py] ListadoTotal")

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# Patron de las entradas
	patron = "<a dir='ltr' href='([^']+)'>(.*?)</a>"
	matches = re.compile(patron,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	# A�ade las entradas encontradas
	for match in matches:
		# Atributos
		scrapedtitle = match[1]
		scrapedurl = match[0]
		scrapedthumbnail = ""
		scrapedplot = ""
		if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

		# A�ade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Asigna el t�tulo, desactiva la ordenaci�n, y cierra el directorio
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )
        

def listvideos(params,url,category):
	logger.info("[cinegratis24h.py] listvideos")

	if url=="":
		url = "http://www.cinegratis24h.com/"
                
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)


	# Extrae las entradas (carpetas)
	patronvideos  = "<h1 class='post-title entry-title'>[^<]+<a href='([^']+)'"  # URL
	patronvideos += ">([^<]+)</a>.*?"                                            # Titulo   
	patronvideos += '<a onblur="[^"]+" href="[^"]+".*?src="([^"]+).*?'           # TUMBNAIL               
	patronvideos += 'border=[^>]+>.*?<span[^>]+>(.*?)</span></div>'        # Argumento	
	#patronvideos += '</h1>[^<]+</div>.*?<div class=[^>]+>[^<]+'
	#patronvideos += '</div>[^<]+<div class=[^>]+>.*?href="[^"]+"><img '                    
	#patronvideos += 'style=.*?src="([^"]+)".*?alt=.*?bold.*?>(.*?)</div>'                  # IMAGEN , DESCRIPCION
	#patronvideos += '.*?flashvars="file=(.*?flv)\&amp'                                      # VIDEO FLV 
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)
	scrapedtitle = ""
	for match in matches:
		# Titulo
		
		scrapedtitle = match[1]
		# URL
		scrapedurl = match[0]
		# Thumbnail
		scrapedthumbnail = match[2]
         
		# Argumento
		scrapedplot = match[3]
		scrapedplot = re.sub("<[^>]+>"," ",scrapedplot)
		scrapedplot = scrapedplot.replace('&#8220;','"')
		scrapedplot = scrapedplot.replace('&#8221;','"')
		scrapedplot = scrapedplot.replace('&#8230;','...')
		scrapedplot = scrapedplot.replace("&nbsp;","")

		# Depuracion
		if (DEBUG):
			logger.info("scrapedtitle="+scrapedtitle)
			logger.info("scrapedurl="+scrapedurl)
			logger.info("scrapedthumbnail="+scrapedthumbnail)

		if not "adelante" in scrapedthumbnail:
			# A�ade al listado de XBMC
			xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente p�gina
	#patronvideos  = "<a class='leermas' href='([^']+)'"
	#matches = re.compile(patronvideos,re.DOTALL).findall(data)
	#scrapertools.printMatches(matches)

	#if len(matches)>0:
		else:
			scrapedtitle = "P�gina siguiente"
			scrapedurl = match[0]
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
	logger.info("[cinegratis24h.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)
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
		patronvideos = 'file=([^\&]+)\&'
		matches = re.compile(patronvideos,re.DOTALL).findall(data)
		
		if len(matches)>0:
			if ("xml" in matches[0]):
				xbmctools.addnewvideo( CHANNELNAME , "play" , category , "xml" , "Reproducir todas las partes a la vez... ", matches[0] , thumbnail , plot )
				#data = scrapertools.cachePage(matches[0])
				req = urllib2.Request(matches[0])
				try:
					response = urllib2.urlopen(req)
				except:
					xbmctools.alertnodisponible()
					return
				data=response.read()
				response.close()
				#logger.info("archivo xml :"+data)
				newpatron = '<title>([^<]+)</title>[^<]+<location>([^<]+)</location>'
				newmatches = re.compile(newpatron,re.DOTALL).findall(data)
				for match in newmatches:
					logger.info(" videos = "+match)
					if match[1].startwith("vid"):
						subtitle = match[0] + " (rtmpe) no funciona en xbmc"
					else:
						subtitle = match[0]             
				
					xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " - "+subtitle, match[1] , thumbnail , plot )
				 
			else:
				parte = 0
				tipo = " (FLV)"
				listdata = []
				for match in matches:
					logger.info(" matches = "+match)
					parte = parte + 1
					if match.endswith('mp4'):
						tipo = " (MP4)"
					xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " (%d) %s" %(parte,tipo), match , thumbnail , plot )
					listdata.append([title + " (%d) %s" %(parte,tipo),match])
				scrapedurl = xmltoplaylist.MakePlaylistFromList(listdata)
				if scrapedurl != "":
					xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , "Reproducir todas las partes a la vez...", scrapedurl , thumbnail , plot )
			
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	logger.info("[cinegratis24h.py] play")

	title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
	server = params["server"]
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def acentos(title):

        title = title.replace("Â�", "")
        title = title.replace("Ã©","�")
        title = title.replace("Ã¡","�")
        title = title.replace("Ã³","�")
        title = title.replace("Ãº","�")
        title = title.replace("Ã­","�")
        title = title.replace("Ã±","�")
        title = title.replace("â€", "")
        title = title.replace("â€œÂ�", "")
        title = title.replace("â€œ","")
        title = title.replace("é","�")
        title = title.replace("á","�")
        title = title.replace("ó","�")
        title = title.replace("ú","�")
        title = title.replace("í","�")
        title = title.replace("ñ","�")
        title = title.replace("Ã“","�")
        return(title)
        
        
        
