# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para dospuntocerovision by bandavi
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
import string
import trailertools
import youtube
import config
import logger

CHANNELNAME = "dospuntocerovision"

# Esto permite su ejecuci�n en modo emulado
try:
	pluginhandle = int( sys.argv[ 1 ] )
except:
	pluginhandle = ""

# Traza el inicio del canal
logger.info("[dospuntocerovision.py] init")

DEBUG = True
IMAGES_PATH = xbmc.translatePath( os.path.join( os.getcwd(), 'resources' , 'images','posters' ) )

def mainlist(params,url,category):
	logger.info("[dospuntocerovision.py] mainlist")

	if config.getSetting("forceview")=="true":
	   xbmc.executebuiltin("Container.SetViewMode(50)") #full list

	# A�ade al listado de XBMC
	xbmctools.addnewfolder( CHANNELNAME , "listnovedades"  , category , "�ltimas pel�culas","http://www.dospuntocerovision.com/","","")
	xbmctools.addnewfolder( CHANNELNAME , "listcategorias" , category , "Listado por Genero","http://www.dospuntocerovision.com/2007/11/peliculas.html","","")
	xbmctools.addnewfolder( CHANNELNAME , "listcategoriasvideos" , category , "Estrenos","http://www.dospuntocerovision.com/2008/03/estrenos-online.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "videosprogtv" , category , "Programas de TV","http://www.dospuntocerovision.com/2007/12/tele-visin.html","","")
        xbmctools.addnewfolder( CHANNELNAME , "listalfabetica" , category , "Busqueda Alfab�tica","http://www.dospuntocerovision.com/2009/08/peliculas-online.html","","")
	xbmctools.addnewfolder( CHANNELNAME , "search"         , category , "Buscar","","","")

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def search(params,url,category):
	logger.info("[dospuntocerovision.py] search")

	keyboard = xbmc.Keyboard('default')
	#keyboard.setDefault('')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		tecleado = keyboard.getText()
		if len(tecleado)>0:
			#convert to HTML
			tecleado = tecleado.replace(" ", "+")
			searchUrl = "http://www.dospuntocerovision.com/search?q="+tecleado
			searchresults(params,searchUrl,category)

def searchresults(params,url,category):
	logger.info("[dospuntocerovision.py] searchresults")

	if config.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons

	patronvideos = 'post-title entry-title(.*?)post-footer'
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)       
        if DEBUG:
            for match in matches:
                #logger.info("videos Match " +match)
	        listarvideos(params,url,category,match)
	    # Extrae la marca de siguiente p�gina
            #data = scrapertools.cachePage(url)
            patronvideos  = "<a class='blog-pager-older-link' href='(.*?)'"
            matches = re.compile(patronvideos,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)

            if len(matches)>0 and (not (matches[0]==url)) :
               scrapedtitle = "P�gina siguiente"
               scrapedurl = matches[0]
               scrapedthumbnail = ""
               scrapedplot = ""
               xbmctools.addnewfolder( CHANNELNAME , "searchresults" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )          
    

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listalfabetica(params, url, category):

	if config.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(50)") #full list

	patronvideos = "<div class='post-header-line-1(.*?)post-footer"
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)       
        if DEBUG:
            for match in matches:
                #logger.info("videos Match " +match)
	        buscaporletra(params,url,category,match)
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listnovedades(params,url,category):
	logger.info("[dospuntocerovision.py] listnovedades : " +url)

	if config.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons
        if url=="http://www.dospuntocerovision.com/":
           opciones = []
	   opciones.append("Listado Corto (6) detallado ")
	   opciones.append("Listado Largo (60) vista rapida")
	   dia = xbmcgui.Dialog()
	   seleccion = dia.select("Elige uno", opciones)
	   logger.info("seleccion=%d" % seleccion) 
        elif not url=="http://www.dospuntocerovision.com/2008/03/ultimas-peliculas-aadidas.html":
           seleccion = 0  
        if seleccion==-1:
	       return
	elif seleccion==0:
	       patronvideos = 'post-title entry-title(.*?)post-footer'
	       # Descarga la p�gina
	       data = scrapertools.cachePage(url)
	       #logger.info(data)
               matches = re.compile(patronvideos,re.DOTALL).findall(data)
	       scrapertools.printMatches(matches)
               if DEBUG:
                  for match in matches:
                      #logger.info("videos Match " +match)
	              listarvideos(params,url,category,match)
	        # Extrae la marca de siguiente p�gina
               #data = scrapertools.cachePage(url)
               patronvideos  = "<a class='blog-pager-older-link' href='(.*?)'"
               matches = re.compile(patronvideos,re.DOTALL).findall(data)
               scrapertools.printMatches(matches)

               if len(matches)>0:
                     scrapedtitle = "P�gina siguiente"
                     scrapedurl = matches[0]
                     scrapedthumbnail = ""
                     scrapedplot = ""
                     xbmctools.addnewfolder( CHANNELNAME , "listnovedades" , category , scrapedtitle , scrapedurl , scrapedthumbnail, scrapedplot )          
    
	elif seleccion==1:
	       url = "http://www.dospuntocerovision.com/2008/03/ultimas-peliculas-aadidas.html"
	       patronvideos = '<a onblur=.*?href="(.*?)"><img.*?src="(.*?)" alt='  
	       # Descarga la p�gina
	       data = scrapertools.cachePage(url)
	       #logger.info(data)

	       # Extrae las entradas (carpetas)
	      
	       matches = re.compile(patronvideos,re.DOTALL).findall(data)
	       scrapertools.printMatches(matches)

	       for match in matches:
	       # URL
	       
			scrapedurl = match[0]
	       
	       # Titulo
	       
			for campo in re.findall("http://.*?/.*?/.*?/(.*?).html",match[0]):
				scrapedtitle = campo
				scrapedtitle = scrapedtitle.replace("-"," ")
			
			# Thumbnail
			
			scrapedthumbnail = match[1]
			
			# procesa el resto
			
			if "2008" in scrapedtitle:
				scrapedplot = " "
			elif "2009" in scrapedtitle:
				scrapedplot = " "
			elif "2010" in scrapedtitle:
				scrapedplot = " "
			else:
				scrapedplot = " "
			# Depuracion
			if (DEBUG):
			      logger.info("scrapedtitle="+scrapedtitle)
			      logger.info("scrapedurl="+scrapedurl)
			      logger.info("scrapedthumbnail="+scrapedthumbnail)
			      xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listvideos(params,url,category):
    logger.info("[dospuntocerovision.py] listvideos " +url)
    if "terrorygore" in url:
            patronvideos = "<h3 class='title'>(.*?)<div class='post-footer'>"
    elif "suricato" in url:
            patronvideos = "<h1 class='post-title entry-title'>(.*?)<div class='post-footer'>"
    else:   
            patronvideos = "<h3 class='post-title entry-title'>(.*?)<div class='post-footer'>"
    #logger.info("patron "+patronvideos)
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if DEBUG:
       for match in matches:
           logger.info("videos Match " +match)
           listarvideos(params,url,category,match)
    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
  
def listarvideos(params,url,category,data):
    titulo = params.get("title")
    logger.info("[dospuntocerovision.py] listarvideos ")
    plot = params.get("plot")
    patronmovshare   = 'href="(http://www.movshare.net/.*?)"[^>]+>(.*?)<'         
    patronmegavideoflv= 'href="(http://www.megavideoflv.com/.*?)"'
    patronmegavideo  = 'href="http://www.megavideo.com/.*?v=(.*?)\&.*?>(.*?)</a>'
    patronmegavideo2 = '(<b[^"]+|<b[^<]+<b[^"]+)".*?http\:\/\/www.megavideo.com/\?(v\=|d\=)([A-Z0-9]{8})".*?>(.*?)</a>(.*?)<'
    patronvideo      = "<a href='.*?'>(.*?)<.*?src=\"([^\"]+)\".*? alt=.*?;\">(.*?)</div>"
    patroncinegratis = 'href="(http://www.cinegratis24h.com/.*?)"'
    patronflv        = 'flashvars="file=(http.*?.flv)'	
    scrapedtitle     = ""
    scrapedthumbnail = ""
    scrapedplot      = ""
#-------------------------------------------------------------------------------
    matchesvideo     = re.compile(patronvideo,re.DOTALL).findall(data)
    for match in matchesvideo:
        scrapedtitle = match[0]
        scrapedthumbnail = match[1]
        scrapedplot = match [2]
        scrapedplot = re.sub("<[^>]+>"," ",scrapedplot)
        scrapedplot = scrapedplot.replace("&#191;","�")
        scrapedplot = acentos(scrapedplot)
        
    if DEBUG and ("+" == plot):
		
		detalle = "Esta opcion permite buscar el trailer en youtube para esta pelicula y muestra hasta seis titulos mas aproximados si los hay \n "
		xbmctools.addnewfolder( "trailertools" , "buscartrailer" , category ,"Buscar trailer para : "+scrapedtitle  , titulo , os.path.join(IMAGES_PATH, 'trailertools.png'), detalle )
#-------------------------------------------------------------------------------    
       
    matchesmegavideo = re.compile(patronmegavideo,re.DOTALL).findall(data) # busca los links de megavideo
#http://www.megavideo.com/?s=dospuntocerovision&amp;v=R30GGEMG&amp;confirmed=1
    #logger.info("videos Match " +matchesmegavideo[0])
    for match in matchesmegavideo:
	scrapedurl = match[0]
	# A�ade al listado de XBMC
        xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megavideo" , scrapedtitle+" - "+match[1]+" - (Megavideo)" , scrapedurl , scrapedthumbnail , scrapedplot ) 

  #http://www.megavideo.com/?v=0I5DDHA8

    matchesmegavideo = re.compile(patronmegavideo2,re.DOTALL).findall(data) # busca los links de megavideo
    for match in matchesmegavideo:
        scrapedurl = match[2]
        titulo = re.sub("<[^>]+>","",match[0])
        titulo = titulo.replace("<a href=","")
        titulo = titulo.replace("<a style=","")
        titulo = titulo.replace("<span style=","")
        titulo = titulo.replace("<div style=","")
        if "megavideo" in match[3]:titulo=titulo +match[4]
        else: titulo = titulo+match[3]+match[4]
        
        if "v" in match[1]:
			xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megavideo" , scrapedtitle+" - "+titulo+" - (Megavideo)" , scrapedurl , scrapedthumbnail , scrapedplot )
        elif "d" in match[1]:
			xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Megaupload" , scrapedtitle+" - "+titulo+" - (Megaupload)" , scrapedurl , scrapedthumbnail , scrapedplot )	
			
#-------------------------------------------------------------------------------
	
    matchescinegratis= re.compile(patroncinegratis,re.DOTALL).findall(data) # busca los links de la pagina de cinegratis24h.com
    if len(matchescinegratis)>0:
        #logger.info("videos Match " +matchescinegratis[0])
        data1 = scrapertools.cachePage(matchescinegratis[0])
        matchesflv   = re.compile(patronflv,re.DOTALL).findall(data1)
        c = 0
        for match in matchesflv:
            c = c + 1
            scrapedurl = match
            # A�ade al listado de XBMC
            xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Directo" , scrapedtitle +" - "+"parte "+str(c)+" (FLV) (V.O.S.)", scrapedurl , scrapedthumbnail , scrapedplot )

#-------------------------------------------------------------------------------
    
    matchesmegavideoflv = re.compile(patronmegavideoflv,re.DOTALL).findall(data)  # Busca los link de megavideoflv.com
    if len(matchesmegavideoflv)>0:
        #logger.info("videos Match " +matchesmegavideoflv[0])
        data1 = scrapertools.cachePage(matchesmegavideoflv[0])
        matchesflv   = re.compile(patronflv,re.DOTALL).findall(data1)
        c = 0
        for match in matchesflv:
            c = c + 1
            scrapedurl = match
            # A�ade al listado de XBMC
            xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Directo" , scrapedtitle +" - "+"parte "+str(c)+" (FLV)", scrapedurl , scrapedthumbnail , scrapedplot )

    matchesmovshare = re.compile(patronmovshare,re.DOTALL).findall(data)
    if len(matchesmovshare)>0:
       #import movshare
        
       total = len(matchesmovshare)
       for match in matchesmovshare:
		logger.info("movshare link : "+match[0])
		
		import movshare
		if "#" in match[0]:
			urlsplited = match[0].split("#")
			scrapedurl = urlsplited[0]
		else:
			scrapedurl = match[0]
		
		if len(scrapedurl)>0:
			
			xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Movshare" , scrapedtitle +" - "+match[1]+" (Movshare)", scrapedurl , scrapedthumbnail , scrapedplot )     

#-------------------------------------------------------------------------------
   
    matchesvideoflv = re.compile(patronflv,re.DOTALL).findall(data)  # busca los link flashvar directos
    if len(matchesvideoflv)>0:
      for match in matchesvideoflv:
          scrapedurl = match 
	  # A�ade al listado de XBMC
          xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Directo" , scrapedtitle +" - "+"Directo  (FLV)", scrapedurl , scrapedthumbnail , scrapedplot ) 
 
    # Busca la lista de los videos documentales de suricato.com para youtube  

    patronyoutube = '<param name="movie" value="http://www.youtube.com/p/(.*?)\&'
    matchyoutube  = re.compile(patronyoutube,re.DOTALL).findall(data)
    if len(matchyoutube)>0:
      for match in matchyoutube:
        listyoutubeurl = 'http://www.youtube.com/view_play_list?p='+match
        data1 = scrapertools.cachePage(listyoutubeurl)
        newpatronyoutube = '<a href="(.*?)".*?<img src="(.*?)".*?alt="([^"]+)"'
        matchnewyoutube  = re.compile(newpatronyoutube,re.DOTALL).findall(data1)
        if len(matchnewyoutube)>0:
           for match2 in matchnewyoutube:
               scrapedthumbnail = match2[1]
               scrapedtitle     = match2[2]
               scrapedurl       = match2[0]
     
               logger.info(" lista de links encontrados U "+str(len(matchnewyoutube)))
            
               xbmctools.addnewvideo( CHANNELNAME , "youtubeplay" , category , "Directo" , scrapedtitle +" - "+"(youtube) ", scrapedurl , scrapedthumbnail , scrapedplot )
            
#-------------------------------------------------------------------------------
    patronyoutube = '<a href="http://www.youtube.com(/watch\?v\=.*?)".*?>(.*?)</a>'
    matchyoutube  = re.compile(patronyoutube,re.DOTALL).findall(data)
    for match in matchyoutube:
		scrapedtitle = match[1]
		scrapedtitle = re.sub("<[^>]+>"," ",scrapedtitle)
		scrapedurl   = match[0]
		xbmctools.addnewvideo( CHANNELNAME , "youtubeplay" , category , "Directo" , scrapedtitle +" - "+"(youtube) ", scrapedurl , scrapedthumbnail , scrapedplot )
		
    # busca los link directos de Google

    patrongoogle  = 'href="(http://video.google.com/videoplay.*?)"'
    matchesgoogle = re.compile(patrongoogle,re.DOTALL).findall(data)
    for match in matchesgoogle:
        urllink = "http://www.flashvideodownloader.org/download.php?u="+match
        logger.info(" Url = "+urllink[0])
        data1 = scrapertools.cachePage(urllink)
        newpatron = '</script><div.*?<a href="(.*?)" title="Click to Download">'
        newmatches = re.compile(newpatron,re.DOTALL).findall(data1)
        if len(newmatches)>0:
          scrapedurl = newmatches[0]
          xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Directo" , scrapedtitle +" - "+"(Google) ", scrapedurl , scrapedthumbnail , scrapedplot )
          
    # busca las url de los videos alojados en tu.tv
    patronvideotv = '(http://www.tu.tv/videos/.*?)"><img src="(.*?)" alt="(.*?)".*?'
    #logger.info("dataa "+data)
    matchestv  = re.compile(patronvideotv,re.DOTALL).findall(data)
    for match in matchestv:
		xbmctools.addnewfolder( CHANNELNAME , "listvideosTVmirror" , category , match[2] , match[0] , match[1], scrapedplot ) 
	
	# Busca las URLs de los videos alojados en videoweed
    patronvideos = 'href="(http://www.videoweed.com/file/[^"]+)" target="_blank">(.*?)</a>'
    matchesweed  = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matchesweed)>0:
		for match in matchesweed:
			scrapedurl = match[0]
			xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "videoweed" , scrapedtitle +" - "+match[1]+" (Videoweed)", scrapedurl , scrapedthumbnail , scrapedplot )
	
	
def listcategorias(params,url,category):
	logger.info("[dospuntocerovision.py] listcategorias")

	if config.getSetting("forceview")=="true":
		xbmc.executebuiltin("Container.SetViewMode(50)") #full list

	patronvideos = '<a onblur=.*?href="(.*?)"><img.*?src="(.*?)" alt='  
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# Extrae las entradas (carpetas)
	      
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:

            # URL
            scrapedurl = match[0]
                       #http://1.bp.blogspot.com/__kdloiikFIQ/SftOQ_gIDsI/AAAAAAAAbE8/mboXI4XyhyA/s400/accion.jpg
            # Titulo
            for campo in re.findall("http://.*?/.*?/.*?/.*?/.*?/.*?/(.*?).jpg",match[1]):
		       
		scrapedtitle = campo
                scrapedtitle = scrapedtitle.replace("+"," ")

		   
		
	    # Thumbnail
            scrapedthumbnail = match[1]
		
            # procesa el resto
            scrapedplot = ""

            # Depuracion
            if (DEBUG):
	       logger.info("scrapedtitle="+scrapedtitle)
	       logger.info("scrapedurl="+scrapedurl)
	       logger.info("scrapedthumbnail="+scrapedthumbnail)

	       # A�ade al listado de XBMC
		
               xbmctools.addnewfolder( CHANNELNAME , "listcategoriasvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listcategoriasvideos(params,url,category):
         logger.info("[dospuntocerovision.py] listcategoriasvideos")
         patronvideos = '<a onblur=.*?href="(.*?)"><img.*?src="(.*?)".*?alt='  
      # Descarga la p�gina
	 data = scrapertools.cachePage(url)
	 #logger.info(data)

       # Extrae las entradas (carpetas)
	      
         matches = re.compile(patronvideos,re.DOTALL).findall(data)
         scrapertools.printMatches(matches)

         for match in matches:

                   # URL
                       scrapedurl = match[0]
                       
		   # Titulo
                       for campo in re.findall("http://.*?/.*?/.*?/(.*?).html",match[0]):
		       
		           scrapedtitle = campo
                           scrapedtitle = scrapedtitle.replace("-"," ")
                           
		      
		
		   # Thumbnail
		       scrapedthumbnail = match[1]
		
		   # procesa el resto
		       scrapedplot = " "

		   # Depuracion
		       if (DEBUG):
			      logger.info("scrapedtitle="+scrapedtitle)
			      logger.info("scrapedurl="+scrapedurl)
			      logger.info("scrapedthumbnail="+scrapedthumbnail)

		              # A�ade al listado de XBMC
		    
                              xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	
	# Label (top-right)...
	 xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	 xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	 xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )


def buscaporletra(params,url,category,data):
        logger.info("[dospuntocerovision.py] buscaporletra")

        patron  = 'href="(.*?)">(.*?)</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        opciones = []
        opciones.append("Buscar por palabras")
        opciones.append("0-9")  
        for letra in letras:
            opciones.append(letra)
                          
        dia = xbmcgui.Dialog()
	seleccion = dia.select("busqueda rapida, elige uno : ", opciones)
        logger.info("seleccion=%d" % seleccion)
        if seleccion == -1 :return
        if seleccion == 0:
            keyboard = xbmc.Keyboard('')
	    keyboard.doModal()
	    if (keyboard.isConfirmed()):
	       tecleado = keyboard.getText()
	       if len(tecleado)>0:
                               
                  logger.info("Nuevo string tecleado   "+tecleado)
                  for match in matches:
                      
                      if (string.lower(tecleado)) in (string.lower(match[1])):
                         scrapedurl   = match[0]
                         scrapedtitle = match[1]
                         scrapedthumbnail = ""
                         scrapedplot = " "
                         if (DEBUG):
		            logger.info("scrapedtitle="+scrapedtitle)
		            logger.info("scrapedurl="+scrapedurl)
		            logger.info("scrapedthumbnail="+scrapedthumbnail)

                         #  A�ade al listado de XBMC
		    
                            xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )    
        elif seleccion == 1:  # href="http://www.dospuntocerovision.com/2008/07/100-chicas.html">100 chicas</a><b
            #patron = '(([0-9].*?html)">.*?</a>'
            for match in matches:
              if match[1][0:1] in ("0123456789"): 
               
                scrapedurl   = match[0]
                scrapedtitle = match[1]
                scrapedthumbnail = ""
                scrapedplot = " "
                if (DEBUG):
		     logger.info("scrapedtitle="+scrapedtitle)
		     logger.info("scrapedurl="+scrapedurl)
		     logger.info("scrapedthumbnail="+scrapedthumbnail)

                     # A�ade al listado de XBMC
		    
                     xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

        else:
            #patron = 'http://.*?/.*?/.*?/'+letras[seleccion-2]+'.*?html'
            #logger.info("patroooooooooooooooooooo  "+patron)
            for match in matches:   
               if match[1][0:1] == letras[seleccion-2]:
                  
		   scrapedurl   = match[0]
                   scrapedtitle = match[1]
                   scrapedthumbnail = ""
                   scrapedplot = " " 	
                   if (DEBUG):  
		     logger.info("scrapedtitle="+scrapedtitle)
		     logger.info("scrapedurl="+scrapedurl)
		     logger.info("scrapedthumbnail="+scrapedthumbnail)

                     # A�ade al listado de XBMC
		    
                     xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )                  
        
        
       

def videosprogtv(params,url,category):
	logger.info("[dospuntocerovision.py] videosprogtv")

	if config.getSetting("forceview")=="true":
	   xbmc.executebuiltin("Container.SetViewMode(53)")  #53=icons

	patronvideos = '<a onblur=.*?href="(.*?)"><img.*?src="(.*?)".*?alt='  
	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	#logger.info(data)

	# Extrae las entradas (carpetas)
	      
	matches = re.compile(patronvideos,re.DOTALL).findall(data)
	scrapertools.printMatches(matches)

	for match in matches:

            # URL
              scrapedurl = match[0]
                       
            # Titulo
              titulo = match[0]
              if  titulo.endswith(".html"):

                  for campo in re.findall("http://.*?/.*?/.*?/(.*?).html",match[0]):
		       
		      scrapedtitle = campo
                      scrapedtitle = scrapedtitle.replace("-"," ")
              else:  #http://3.bp.blogspot.com/__kdloiikFIQ/Sbvq6Xis_GI/AAAAAAAAYBw/CrgJne1OfXs/s320/hora+de+jose+mota.JPG
                  
                  #logger.info("titulo "+match[0])   
                  for campo in re.findall("http://.*?/.*?/.*?/.*?/.*?/.*?/(.*?).JPG",match[1]):
		      scrapedtitle = campo
		      scrapedtitle = scrapedtitle.replace("+"," ")
	    # Thumbnail
    	      scrapedthumbnail = match[1]
		
	    # procesa el resto
	      scrapedplot = ""

	    # Depuracion
	      if (DEBUG):
		 logger.info("scrapedtitle="+scrapedtitle)
		 logger.info("scrapedurl="+scrapedurl)
	         logger.info("scrapedthumbnail="+scrapedthumbnail)

	    # A�ade al listado de XBMC
		    
                 xbmctools.addnewfolder( CHANNELNAME , "listvideos" , category , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

	
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def listvideosTVmirror(params,url,category):
	logger.info("[dospuntocerovision.py] listvideosTVmirror")
	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )

	# Descarga la p�gina
	data = scrapertools.cachePage(url)
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = servertools.findvideos(data)
	
	for video in listavideos:
		#logger.info("")
		if video[2] == "tu.tv":
			url = urllib.unquote_plus(servertools.findurl(video[1],video[2]))
			xbmctools.addnewvideo( CHANNELNAME , "detail" , category , "Directo" , title +" - "+video[0], url, thumbnail , "" )
		else:
			xbmctools.addnewvideo( CHANNELNAME , "detail" , category , video[2] , title +" - "+video[0], video[1], thumbnail , "" )
	# ------------------------------------------------------------------------------------

	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
		
	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
	
	
	
def detail(params,url,category):
	logger.info("[dospuntocerovision.py] detail")

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
        try:
	   plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
        except:
           plot = xbmc.getInfoLabel( "ListItem.Plot" )
        server = params["server"]
        
	
	xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)

def youtubeplay(params,url,category):
        logger.info("[dospuntocerovision.py] youtubeplay")
	if "www.youtube" not in url:
		url  = 'http://www.youtube.com'+url
 

	title = urllib.unquote_plus( params.get("title") )
	thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = "Ver Video"
	server = "Directo"
	id = youtube.Extract_id(url)
	videourl = youtube.geturl(id)
	
	if len(videourl)>0:
		logger.info("link directo de youtube : "+videourl)
		xbmctools.playvideo("Trailer",server,videourl,category,title,thumbnail,plot)
	
	return
	
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
        
def buscartrailer(params,url,category):
	logger.info("[dospuntocerovision.py] buscartrailer")
	titulo = url
	#thumbnail = urllib.unquote_plus( params.get("thumbnail") )
	plot = urllib.unquote_plus( params.get("plot") )
	# ------------------------------------------------------------------------------------
	# Busca los enlaces a los videos
	# ------------------------------------------------------------------------------------
	listavideos = trailertools.gettrailer(titulo)
	if len(listavideos)>0:
		for video in listavideos:
			videotitle = video[1]
			url        = video[0]
			thumbnail  = video[2]
			xbmctools.addnewvideo( CHANNELNAME , "youtubeplay" , category , "Directo" ,  videotitle , url , thumbnail , "Ver Video" )
			
	#else:
	#	respuesta = trailertools.alertnoencontrado(titulo)
	#	if respuesta:
	#		listavideos = trailertools.trailerbykeyboard(titulo)
	#		for video in listavideos:
	#			videotitle = video[1]
	#			url        = video[0]
	#			thumbnail  = video[2]
	#			xbmctools.addnewvideo( CHANNELNAME , "youtubeplay" , category , "Directo" ,  videotitle , url , thumbnail , "Ver Video" )
	# ------------------------------------------------------------------------------------
	# Label (top-right)...
	xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

	# Disable sorting...
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

	# End of directory...
	xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
	
def alertaerror():
	ventana = xbmcgui.Dialog()
	ok= ventana.ok ("Plugin Pelisalacarta", "Uuppss...El video no esta disponible en youtube",'o la resolucion es muy baja',"elij� otra resolucion distinta y vuelva a probar")
