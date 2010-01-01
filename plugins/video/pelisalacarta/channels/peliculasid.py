# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasid
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

CHANNELNAME = "peliculasid"

# Esto permite su ejecución en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
xbmc.output("[peliculasid.py] init")

DEBUG = True

def mainlist(params,url,category):
	xbmc.output("[peliculasid.py] mainlist")

	# Añade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ultimas Películas Subidas"    ,"http://www.peliculasid.com/","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Estrenos","http://www.peliculasid.net/index.php?module=estrenos","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Series","http://www.peliculasid.net/index.php?module=series","","")
	xbmctools.addnewfolder( CHANNELNAME , "listcategorias" , category , "Categorias"        ,"http://www.peliculasid.com/","","")
	#xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Buscar","http://www.peliculasid.net/index.php?module=documentales","","")

	if xbmcplugin.getSetting("singlechannel")=="true":
		xbmctools.addSingleChannelOptions(params,url,category)

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listcategorias(params,url,category):
        xbmc.output("[peliculas.py] listcategorias")

        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Acción"    ,"http://www.peliculasid.com/accion-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Animación"    ,"http://www.peliculasid.com/animacion-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Aventura"    ,"http://www.peliculasid.com/aventura-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Ciencia Ficción"    ,"http://www.peliculasid.com/ciencia_ficcion-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Cine Indio"    ,"http://www.peliculasid.com/cine_indio-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Comedia"    ,"http://www.peliculasid.com/comedia-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Crimen"    ,"http://www.peliculasid.com/crimen-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Documentales y mas"    ,"http://www.peliculasid.com/documentales-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Drama"    ,"http://www.peliculasid.com/drama-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Fantasia"    ,"http://www.peliculasid.com/fantasia-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Horror"    ,"http://www.peliculasid.com/horror-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Misterio"    ,"http://www.peliculasid.com/misterio-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Romance"    ,"http://www.peliculasid.com/romance-1.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , "Thriller"    ,"http://www.peliculasid.com/thriller-1.html","","")
        
        # Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
        

def listvideos(params,url,category):
	xbmc.output("[peliculasid.py] listvideos")

	if url=="":
		url = "http://www.peliculasid.com/"
                
	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)

	# Extrae las entradas (carpetas)
	patronvideos  = '<div class="boxgrid captionfull"><a href="([^"]+)" >'
	patronvideos += '<img src="([^"]+)" width=.*?'
	patronvideos += '<div class="cover boxcaption">.*?<h6>([^<]+)</h6>'

	#patronvideos += "<img src='(.*?)'"
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:
		# Titulo
		scrapedtitle = match[2]
		# URL
		scrapedurl = urlparse.urljoin(url,match[0])
		# Thumbnail
		scrapedthumbnail = match[1]
                scrapedthumbnail = scrapedthumbnail.replace(" ","")
		# Argumento
		scrapedplot = ""

		# Depuracion
		if (DEBUG):
			xbmc.output("scrapedtitle="+scrapedtitle)
			xbmc.output("scrapedurl="+scrapedurl)
			xbmc.output("scrapedthumbnail="+scrapedthumbnail)

		# Añade al listado de XBMC
		xbmctools.addnewfolder( CHANNELNAME , "detail" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )

	# Extrae la marca de siguiente página
	patronvideos  = '<div id="paginador">.*?<a href="([^"]+)"><b>Siguiente</b></a></div>'
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	if len(matches)>0:
		scrapedtitle = "Página siguiente"
		scrapedurl = urlparse.urljoin(url,matches[0])
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
	xbmc.output("[peliculasid.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )

	# Descarga la página
	data = scrapertools.cachePage(url)
	#xbmc.output(data)
        patrondescrip = '<li class="description">(.*?)</li>'
        matches = re.compile(patrondescrip,re.DOTALL).findall(data)
        if DEBUG:
          if len(matches)>0:
		descripcion = matches[0]
                descripcion = descripcion.replace('&#8220;','"')
                descripcion = descripcion.replace('&#8221;','"')
                descripcion = descripcion.replace('&#8230;','...')
                descripcion = descripcion.replace("&nbsp;","")
		descripcion = descripcion.replace("<br/>","")
		descripcion = descripcion.replace("\r","")
		descripcion = descripcion.replace("\n"," ")
                descripcion = descripcion.replace("\t"," ")
		descripcion = re.sub("<[^>]+>"," ",descripcion)
#                xbmc.output("descripcion="+descripcion)
                descripcion = acentos(descripcion)
#                xbmc.output("descripcion="+descripcion)
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
        patronvideos = 'flashvars" value="file=([^\&]+)\&amp'
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
                xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title, matches[0] , thumbnail , plot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=pluginhandle, category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=pluginhandle, sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=pluginhandle, succeeded=True )

def play(params,url,category):
	xbmc.output("[peliculasid.py] play")

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