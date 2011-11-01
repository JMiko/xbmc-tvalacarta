# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelis24
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin

from core import scrapertools
from core import config
from core import logger
from platform.xbmc import xbmctools
from core.item import Item
from servers import servertools

CHANNELNAME = "pelis24"

# Esto permite su ejecuci�n en modo emulado
try:
    pluginhandle = int( sys.argv[ 1 ] )
except:
    pluginhandle = ""

logger.info("[pelis24.py] init")

DEBUG = True

def mainlist(params,url,category):
    logger.info("[pelis24.py] mainlist")

    # A�ade al listado de XBMC
    xbmctools.addnewfolder( CHANNELNAME , "list", category , "Peliculas","http://pelis24.com/peliculas/","","")
    xbmctools.addnewfolder( CHANNELNAME , "list", category , "Peliculas VOSE","http://pelis24.com/peliculasvose/","","")
    xbmctools.addnewfolder( CHANNELNAME , "list", category , "Series","http://pelis24.com/series/","","")
    xbmctools.addnewfolder( CHANNELNAME , "list", category , "Novedades","http://pelis24.com/","","")

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def list(params,url,category):
    logger.info("[pelis24.py] list")

    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    '''
    <div class="yjnewsflash_title"><a href="http://www.pelis24.com/peliculas/12554-el-castor-2011castellano.html">El castor (2011)(castellano)</a> </div>
    <p><br>
    <br>
    <div id='news-id-12554'><!--dle_image_begin:http://x-peliculas.net/images/ba20e6b6e9.jpg|left--><img src="http://x-peliculas.net/images/ba20e6b6e9.jpg" align="left" alt="El castor (2011)(castellano)" title="El castor (2011)(castellano)"  /><!--dle_image_end--><br />Sinopsis:<br /><br />Water Black (Mel Gibson) est� sumido en una profunda depresi�n. Su vida se viene abajo y ni su mujer (Jodie Foster) ni sus hijos saben c�mo ayudarle. Un d�a, ya al l�mite de la desesperaci�n, encuentra una marioneta con forma de castor en un cubo de basura. A partir de ese momento la vida de Walter da un giro radical.<br /></div><span class="yjnewsflash_date">Hoy, 17:09 | <a href="http://www.pelis24.com/peliculas/">Peliculas</a> | </span></p>
    <div class="linksw"><br /><a href="http://www.pelis24.com/peliculas/12554-el-castor-2011castellano.html#comment"><img src="/templates/Pelis/img/com.png" border="0" />Comentarios (0)</a> &nbsp;<a href="http://www.pelis24.com/peliculas/12554-el-castor-2011castellano.html"><img src="/templates/Pelis/images/arr2.png" width="13" height="9" border="0" /><strong>Ver Pelicula Online!</strong></a></div></div><div class="yjnewsflash">
    '''
    patron  = '<div class="yjnewsflash_title"><a href="([^"]+)">([^<]+)</a> </div>[^<]+'
    patron += '<p><br>[^<]+'
    patron += '<br>[^<]+'
    patron += '<div[^>]+><!--TBegin--><a href="([^"]+)".*?'
    patron += '<!--TEnd-->([^<]+)<' #,*?<a'#.*?<a href="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = match[2]
        scrapedplot = match[3]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        xbmctools.addnewfolder( CHANNELNAME , "detail" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

    '''
    <div class="yjnewsflash_title"><a href="http://www.pelis24.com/series/424-el-mentalista-espanol-online.html">El Mentalista Espa�ol Temporada 1</a> </div>
    <p><br>
    <br>
    <div id='news-id-424'><div align="center"><img src="http://i40.tinypic.com/33392ck.jpg" style="border: none;" alt='El Mentalista Espa�ol Temporada 1' title='El Mentalista Espa�ol Temporada 1' /><br /><br />La historia de El Mentalista comienza cuando Patrick Jane, un hombre que se ganaba la vida como m�dium televisivo, sufre un duro golpe al perder a su mujer y su hija a manos de un asesino. A partir de ese momento, Patrick Jane toma la determinaci�n de dedicarse de lleno a sus habilidades como detective y trabajar en el Departamento de Investigaci�n de Cr�menes de California en la resoluci�n de los casos de asesinato. �l no ve, observa. No oye, escucha. No toca, percibe. No falla.</div></div><span class="yjnewsflash_date">9 enero 2009 | <a href="http://www.pelis24.com/series/">Series</a> | </span></p>
    <div class="linksw"><br /><a href="http://www.pelis24.com/series/424-el-mentalista-espanol-online.html#comment"><img src="/templates/Pelis/img/com.png" border="0" />Comentarios (7)</a> &nbsp;<a href="http://www.pelis24.com/series/424-el-mentalista-espanol-online.html"><img src="/templates/Pelis/images/arr2.png" width="13" height="9" border="0" /><strong>Ver Pelicula Online!</strong></a></div></div><div class="yjnewsflash">
    '''
    patron  = '<div class="yjnewsflash_title"><a href="([^"]+)">([^<]+)<.*?'
    patron  = '<div class="yjnewsflash_title"><a href="([^"]+)">([^<]+)</a> </div>[^<]+'
    patron += '<p><br>[^<]+'
    patron += '<br>[^<]+'
    patron += '<div[^>]+><div[^>]+><img src="([^"]+)".*?>([^<]+)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = match[1]

        # URL
        scrapedurl = urlparse.urljoin(url,match[0])
        
        # Thumbnail
        scrapedthumbnail = match[2]
        
        # procesa el resto
        scrapedplot = match[3]

        # Depuracion
        if (DEBUG):
            logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")



        # A�ade al listado de XBMC
        xbmctools.addnewfolder( CHANNELNAME , "detail" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapedplot )

    # Extrae la entrada para la siguiente p�gina
    patronvideos  = '<div id="right"><a href="([^"]+)">Siguiente P.gina</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = "!P�gina siguiente"

        # URL
        scrapedurl = match
        
        # Thumbnail
        scrapedthumbnail = ""
        
        # procesa el resto
        scrapeddescription = ""

        # Depuracion
        if (DEBUG):
            logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # A�ade al listado de XBMC
        xbmctools.addnewfolder( CHANNELNAME , "list" , CHANNELNAME , scrapedtitle , scrapedurl , scrapedthumbnail , scrapeddescription )

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )

    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def detail(params,url,category):
    logger.info("[pelis24.py] detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = urllib.unquote_plus( params.get("plot") )
    # Descarga la p�gina
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Busca los enlaces a los mirrors, o a los cap�tulos de las series...
    patronvideos  = '<a href="([^"]+)">Sigu'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        xbmctools.addnewfolder( CHANNELNAME , "list", category , "!P�gina siguiente",urlparse.urljoin(url,match),"","")

    patronvideos  = 'file\=(http\://www.pelis24.com/xml[^\&]+)\&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        if ("xml" in matches[0]):
            data2 = scrapertools.cachePage(matches[0])
            logger.info("data2="+data2)
            patronvideos  = '<track>[^<]+'
            patronvideos += '<creator>([^<]+)</creator>[^<]+'
            patronvideos += '<location>([^<]+)</location>.*?'
            patronvideos += '</track>'
            matches = re.compile(patronvideos,re.DOTALL).findall(data2)
            scrapertools.printMatches(matches)

            for match in matches:
                 
                if "vid" not in match[1]: 
                    scrapedtitle = match[0]
                else: 
                    scrapedtitle = match[0]+" no funciona en xbmc"
                scrapedurl = match[1].strip()
                scrapedthumbnail = thumbnail
                scrapedplot = plot
                if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

                # A�ade al listado de XBMC
                xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , scrapedtitle + " [Directo]", scrapedurl , scrapedthumbnail, scrapedplot )
        else:
            # A�ade al listado de XBMC
            xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title + " [Directo]", matches[0] , thumbnail, plot )
    
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a videos directos
    # ------------------------------------------------------------------------------------

    patronvideos  = "url:'([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    i = 1
    for match in matches:
        xbmctools.addnewvideo( CHANNELNAME , "play" , category , "Directo" , title +" %d - [Directo]" % i, match, thumbnail , "" )

    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    listavideos = servertools.findvideos(data)
    
    i = 1
    for video in listavideos:
        xbmctools.addnewvideo( CHANNELNAME , "play" , category , video[2] , (title +" %d - "+video[0]) % i, video[1], thumbnail , "" )
        i = i + 1
    # ------------------------------------------------------------------------------------

    # Label (top-right)...
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
        
    # Disable sorting...
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )

    # End of directory...
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

def play(params,url,category):
    logger.info("[pelis24.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = params["server"]
    
    xbmctools.play_video(CHANNELNAME,server,url,category,title,thumbnail,plot)
