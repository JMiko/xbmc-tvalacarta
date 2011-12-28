# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cine-adicto.com by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
#from pelisalacarta import buscador
from servers import servertools

__channel__ = "cineadicto"
__category__ = "F,D"
__type__ = "generic"
__title__ = "Cine-Adicto"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cineadicto.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="listvideos"         , title="Ultimas Películas Añadidas"    , url="http://www.cine-adicto.com/" , extra="ultimas" ))
    itemlist.append( Item(channel=__channel__ , action="ListvideosMirror"   , title="Estrenos"                      , url="" ))
    itemlist.append( Item(channel=__channel__ , action="ListaCat"           , title="Listado por Genero"            , url="http://www.cine-adicto.com/"))
    # Desactivado por problemas en la web
    #itemlist.append( Item(channel=__channel__ , action="ListaAlfa"          , title="Listado Alfanumerico"          , url="http://www.cine-adicto.com/" ))
    itemlist.append( Item(channel=__channel__ , action="ListvideosMirror"   , title="Documentales"                  , url="http://www.cine-adicto.com/category/documentales/"))
    #itemlist.append( Item(channel=__channel__ , action="listvideos"         , title="Peliculas en HD"               , url="http://www.cine-adicto.com/category/peliculas-hd-categorias" ))
    itemlist.append( Item(channel=__channel__ , action="search"             , title="Buscar"                        , url="http://www.cine-adicto.com/?s="))

    return itemlist
    
def search(item,texto,categoria="*"):
    logger.info("[cineadicto.py] search")
    
    itemlist = []
    
    if item.url in ("","none"):
       if categoria in ("*","F"):
          item.url = "http://www.cine-adicto.com/?s=%s&x=0&y=0" % texto
          itemlist.extend(ListvideosMirror(item))
       if categoria in ("*","D"):
          item.url = "http://www.cine-adicto.com/category/documentales/?s=%s&x=0&y=0" % texto
          itemlist.extend(ListvideosMirror(item))
    else:
       itemlist.extend(ListvideosMirror(item))

    return itemlist
    
def ListaCat(item):
    logger.info("[cineadicto.py] ListaCat")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # <li class="cat-item cat-item-1"><a href="http://www.cine-adicto.com/category/2008" title="Películas Online del año 2008">2008</a>
    patronvideos  = '<li class="[^"]+"><a href="([^"]+)" title="[^"]+">([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Atributos
        scrapedurl = match[0]
        scrapedtitle = match[1]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=item.channel , action="ListvideosMirror"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    return itemlist
    
def ListaAlfa(item):
    itemlist = []
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="0-9",url="http://www.cine-adicto.com/alphabet/9/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="A",url="http://www.cine-adicto.com/alphabet/a/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="B",url="http://www.cine-adicto.com/alphabet/b/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="C",url="http://www.cine-adicto.com/alphabet/c/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="D",url="http://www.cine-adicto.com/alphabet/d/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="E",url="http://www.cine-adicto.com/alphabet/e/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="F",url="http://www.cine-adicto.com/alphabet/f/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="G",url="http://www.cine-adicto.com/alphabet/g/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="H",url="http://www.cine-adicto.com/alphabet/h/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="I",url="http://www.cine-adicto.com/alphabet/i/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="J",url="http://www.cine-adicto.com/alphabet/j/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="K",url="http://www.cine-adicto.com/alphabet/k/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="L",url="http://www.cine-adicto.com/alphabet/l/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="M",url="http://www.cine-adicto.com/alphabet/m/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="N",url="http://www.cine-adicto.com/alphabet/n/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="O",url="http://www.cine-adicto.com/alphabet/o/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="P",url="http://www.cine-adicto.com/alphabet/p/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="Q",url="http://www.cine-adicto.com/alphabet/q/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="R",url="http://www.cine-adicto.com/alphabet/r/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="S",url="http://www.cine-adicto.com/alphabet/s/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="T",url="http://www.cine-adicto.com/alphabet/t/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="U",url="http://www.cine-adicto.com/alphabet/u/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="V",url="http://www.cine-adicto.com/alphabet/v/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="W",url="http://www.cine-adicto.com/alphabet/w/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="X",url="http://www.cine-adicto.com/alphabet/x/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="Y",url="http://www.cine-adicto.com/alphabet/y/"))
    itemlist.append( Item(channel=item.channel , action="listvideos" , title="Z",url="http://www.cine-adicto.com/alphabet/z/"))

    return itemlist

def ListvideosMirror(item):
    logger.info("[cineadicto.py] ListvideosMirror")

    if item.url=="":
        data = scrapertools.cachePage("http://www.cine-adicto.com/")
        patron = '<a href="([^"]+)">Ver Estrenos Online</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        item.url = matches[0]
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Patron de las entradas
    '''
    <div class="short_post">
    <h2 id="post-12662"><a href="http://www.cine-adicto.com/setup.html">Setup</a></h2>
    <div class="arch_port">
    <img src="http://www.cine-adicto.com/images/set_up_pelicula.jpg" width="86" height="128" alt="Setup" />
    </div>
    <div class="arch_entry">
    <p>En Setup, un grupo de amigos se verá envuelto en un robo de diamantes en el que termina habiendo muertos de por medio.</p>
    <span class="arch_views">Vista 220 veces</span>
    <a class="movie_arc_go" href="http://www.cine-adicto.com/setup.html" title="Ver Pelicula">Ver Pelicula</a>
    </div>
    '''
    patronvideos  = '<div class="short_post">.*?<a href="([^"]+)">([^<]+)</a>.*?'
    patronvideos += 'src="([^"]+)".*?'
    patronvideos += '<p>([^<]+)</p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        
        # Quita entidades HTML
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        if "http://www.cine-adicto.com/images/" not in scrapedthumbnail:
            scrapedthumbnail = urlparse.urljoin("http://www.cine-adicto.com/images",scrapedthumbnail)
        scrapedplot = match[3]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__ , action="detail"  , title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))

    #Extrae la marca de siguiente página
    patronvideos  = '<span class=[\W]current[\W]>[^<]+</span>?<a href=([\S]+)'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "!Página siguiente"
        scrapedurl = matches[0].strip("'").strip('"')
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__ , action="ListvideosMirror"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))

    return itemlist

def listvideos(item):
    logger.info("[cineadicto.py] listvideos")

    url = item.url
    if url=="":
        url = "http://www.cine-adicto.com/"
    patron = ""
    if item.extra=="ultimas":
        patron = '<div id="latest-movies"(.*?)popular-movies'
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
    '''
    <div class="movie_box">
    <div class="movie-thumbnail">
    <a href="http://www.cine-adicto.com/flypaper.html"><img class="homethumb" src="http://www.cine-adicto.com/images/Atraco_por_duplicado-online.jpg" width="149" height="222" alt="Flypaper" /></a>
    <div class="movie-desc">
    <img src="http://www.cine-adicto.com/wp-content/themes/cineadicto_theme/images/mouseover-arrow.png" alt="" class="mouseover-arrow" />
    <h3>Flypaper</h3>
    <span class="pop_desc">
    <p>Historia que trata sobre un hombre atrapado en medio de dos atracos diferentes pero en el mismo banco. Su objetivo no es otro que proteger a una de las cajeras del banco de quien está locamente enamorado en secreto.</p>
    '''

    itemlist = []
    data2 = re.compile(patron,re.DOTALL).findall(data)
    patronvideos = '<div class="movie_box">.*?<a href="([^"]+)"><img.*?src="([^"]+)".*?/>[^<]+'
    patronvideos += '<[^>]+>([^<]+)</[^>]+>.*?'
    patronvideos += '<p>([^<]+)</p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data2[0])
    logger.info("hay %d matches" % len(matches))

    for match in matches:
        scrapedtitle = match[2]
        
        # Quita entidades HTML
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapedplot = match[3]
            
        itemlist.append( Item(channel=item.channel , action="detail"  , title=scrapedtitle  , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , fanart=scrapedthumbnail ))

    #Extrae la marca de siguiente página
    #<span class='current'>1</span><a href='http://delatv.com/page/2' class='page'>2</a>
    patronvideos  = '<span class="current">[^<]+</span>[^<]*<a.*?href="([^"]+)"' #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    if len(matches)==0:
        patronvideos  = "<span class='current'>[^<]+</span>[^<]*<a.*?href='([^']+)'" #"</span><a href='(http://www.cine-adicto.com/page/[^']+)'""
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Página siguiente"
        scrapedurl = urlparse.urljoin(url,matches[0])#matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=item.channel , action="listvideos"  , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , extra="ultimas" ))

    return itemlist

def detail(item):
    logger.info("[cineadicto.py] detail")

    title = item.title
    thumbnail = item.thumbnail
    plot = item.plot
    scrapedurl = ""
    url = item.url

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)
    patronvideos = 'name="Pelicula" src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        data = scrapertools.cachePage(matches[0])

    # Extrae el argumento
    patronarg = '</p><p>.*?<strong>([^<]+</strong> <strong>.*?)<p></p>'
    matches   = re.compile(patronarg,re.DOTALL).findall(data)
    if len(matches)>0:
        plot  = re.sub("<[^>]+>"," ",matches[0])
  
    # Busca enlaces a videos .flv o (.mp4 dentro de un xml)                     #
    itemlist.extend( find_video_items_cineadicto(item,data,plot) )

    
    # matches = url.split("/")
    # url2 = "http://www.cine-adicto.com/tab/"+matches[3]
    # logger.info(url2)
    # data = scrapertools.cachePage(url2)
    # Busca el ID de megaupload
    patronmega = '<div style="visibility:hidden;" id="megaid">(.*?)&langid.*?</div>'
    matches2 = re.compile(patronmega,re.DOTALL).findall(data)
    url = "http://www.megaupload.com/?d="+matches2[0].strip()
    data = data.replace('<div style="visibility:hidden;" id="megaid">'+matches2[0],url)
    
    # Usa findvideos
    listavideos = servertools.findvideos(data)
    
    c = 0
    for video in listavideos:
        videotitle = video[0]
        url = video[1]
        server = video[2]
        if "youtube" in server:
            videotitle = "[Trailer]"
        if "facebook" in url:
            c += 1
            itemlist.append( Item(channel=item.channel , action="play"   , server=server , title=title.strip() + " - Parte %d %s" %(c,videotitle) , fulltitle=item.fulltitle , url=url , thumbnail=thumbnail , plot=plot , folder=False))
        elif "p5K-vLAO02M" not in url:
            itemlist.append( Item(channel=item.channel , action="play"   , server=server , title=title.strip() + " - " + videotitle , fulltitle=item.fulltitle  , url=url , thumbnail=thumbnail , plot=plot , folder=False ))


    return itemlist

def find_video_items_cineadicto(item,data,plot):

    title = item.title
    thumbnail = item.thumbnail
    scrapedurl = ""
    url = item.url
    
    #patron = ''

    patronvideos = 'file=(http\:\/\/[^\&]+)\&'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    playWithSubt = "play"
    c = 0
    itemlist = []
    for match in matches:
        subtitle = "[FLV-Directo]"
        c += 1
        if ("playlist" in match):
            data2 = scrapertools.cachePage(match)
            logger.info("data2="+data2)
            patronvideos  = '<track>.*?'
            patronvideos += '<title>([^<]+)</title>[^<]+'
            patronvideos += '<location>([^<]+)</location>(?:[^<]+'
            patronvideos += '<meta rel="type">video</meta>[^<]+|[^<]+'
            patronvideos += '<meta rel="captions">([^<]+)</meta>[^<]+)'
            patronvideos += '</track>'
            matches2 = re.compile(patronvideos,re.DOTALL).findall(data2)
            scrapertools.printMatches(matches)
            
            for match2 in matches2:
                subtitle_url=""
                sub = ""
                if match2[2].endswith(".xml"): # Subtitulos con formato xml son incompatibles con XBMC
                    sub = "[Subtitulo incompatible con xbmc]"
                if ".mp4" in match2[1]:
                    subtitle = "[MP4-Directo]"
                scrapedtitle = '%s (castellano) - %s  %s' %(title,match2[0],subtitle)
                
                scrapedurl = match2[1].strip()
                scrapedthumbnail = thumbnail
                scrapedplot = plot
                if ("cast.xml" or "mirror.xml") not in match:
                    scrapedtitle = '%s (V.O.S) - %s  %s %s' %(title,match2[0],subtitle,sub)
                    if not match2[2].endswith("cine-adicto2.srt") and (sub == ""): 
                        scrapedurl = scrapedurl
                        subtitle_url=match2[2]
                        
                if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
                        
                # Añade al listado de XBMC
                itemlist.append( Item(channel=item.channel , action=playWithSubt  , title=scrapedtitle, url=scrapedurl, subtitle=subtitle_url , thumbnail=scrapedthumbnail, plot=scrapedplot, server= "Directo" , folder = False ))
            
        else:
            c +=1
            scrapedurl = match
            if match.endswith(".srt") and not (((c / 2) * 2 - c) == 0) :
                logger.info("[cineadicto.py] Encontrado subtitulo "+match)
                itemlist.append( Item(channel=item.channel , action="play"  , server="Directo" , title=title + " (V.O.S) - "+subtitle, subtitle=match, url=scrapedurl , thumbnail=thumbnail , plot=plot , folder=False))
            elif match.endswith(".xml") and not (((c / 2) * 2 - c) == 0):
                sub = "[Subtitulo incompatible con xbmc]"
                itemlist.append( Item(channel=item.channel , action="play"  , server="Directo" , title=title + " (V.O) - %s %s" %(subtitle,sub), url=scrapedurl , thumbnail=thumbnail , plot=plot , folder=False ))
            elif not match.endswith("srt" or "xml") :
                itemlist.append( Item(channel=item.channel , action="play"  , server="Directo" , title=title + " - [Directo]" , url=scrapedurl , thumbnail=thumbnail , plot=plot , folder=False ))
            print scrapedurl

    return itemlist
