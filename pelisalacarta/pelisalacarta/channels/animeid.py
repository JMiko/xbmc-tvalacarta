# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para animeid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "Animeid"
__channel__ = "animeid"
__language__ = "ES"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[animeid.py] mainlist")
    
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="destacados", title="Destacados"               , url="http://animeid.com/" ))
    itemlist.append( Item(channel=__channel__, action="newlist"   , title="Últimas series agregadas" , url="http://animeid.com/" ))
    itemlist.append( Item(channel=__channel__, action="chaplist"  , title="Últimos capítulos"        , url="http://animeid.com/" ))
    itemlist.append( Item(channel=__channel__, action="airlist"   , title="Series en emisión"        , url="http://animeid.com/" ))
    itemlist.append( Item(channel=__channel__, action="fulllist"  , title="Lista completa de animes" , url="http://animeid.com/" ))
    itemlist.append( Item(channel=__channel__, action="genrelist" , title="Listado por genero"       , url="http://animeid.com/" ))
    itemlist.append( Item(channel=__channel__, action="alphalist" , title="Listado alfabetico"       , url="http://animeid.com/" ))

    return itemlist

def alphalist(item):
    logger.info("[animeid.py] alphalist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="newlist" , title="0-9", url="http://animeid.com/letras/0-9.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="A"  , url="http://animeid.com/letras/a.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="B"  , url="http://animeid.com/letras/b.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="C"  , url="http://animeid.com/letras/c.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="D"  , url="http://animeid.com/letras/d.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="E"  , url="http://animeid.com/letras/e.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="F"  , url="http://animeid.com/letras/f.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="G"  , url="http://animeid.com/letras/g.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="H"  , url="http://animeid.com/letras/h.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="I"  , url="http://animeid.com/letras/i.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="J"  , url="http://animeid.com/letras/j.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="K"  , url="http://animeid.com/letras/k.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="L"  , url="http://animeid.com/letras/l.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="M"  , url="http://animeid.com/letras/m.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="N"  , url="http://animeid.com/letras/n.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="O"  , url="http://animeid.com/letras/o.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="P"  , url="http://animeid.com/letras/p.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="Q"  , url="http://animeid.com/letras/q.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="R"  , url="http://animeid.com/letras/r.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="S"  , url="http://animeid.com/letras/s.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="T"  , url="http://animeid.com/letras/t.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="U"  , url="http://animeid.com/letras/u.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="V"  , url="http://animeid.com/letras/v.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="W"  , url="http://animeid.com/letras/w.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="X"  , url="http://animeid.com/letras/x.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="Y"  , url="http://animeid.com/letras/y.html"))
    itemlist.append( Item(channel=__channel__, action="newlist" , title="Z"  , url="http://animeid.com/letras/z.html"))

    return itemlist

def genrelist(item):
    logger.info("[animeid.py] genrelist")
    '''
    <div class="ctit">Animes por g&eacute;nero:</div>
    <div class="ccon">
    <div id="genuno"> <ul class="alfa" style="margin-top:6px; margin-left: 31px;">
      <li><a href="/genero/accion.html" class="let">Acci&oacute;n</a></li>
      <li><a href="/genero/aventura.html" class="let">Aventura</a></li>
      <li><a href="/genero/carreras.html" class="let">Carreras</a></li>
      <li><a href="/genero/comedia.html" class="let">Comedia</a></li>
      <li><a href="/genero/cyberpunk.html" class="let">Cyberpunk</a></li> </ul> <ul class="alfa" style="margin-left: 30px;">
      <li><a href="/genero/deportes.html" class="let">Deportes</a></li>
      <li><a href="/genero/drama.html" class="let">Drama</a></li>
      <li><a href="/genero/ecchi.html" class="let">Ecchi</a></li>
      <li><a href="/genero/escolares.html" class="let">Escolares</a></li>
      <li><a href="/genero/fantasia.html" class="let">Fantas&iacute;a</a></li>
      <li><a href="javascript:void(0);" class="let" id="unodos"><img src="/img/ncat.png" alt="Siguiente" border="0" /></a></li> </ul> </div>
    <div id="gendos" style="display: none; margin-top:6px;"> <ul class="alfa" style="margin-left:29px;"> <li><a href="javascript:void(0);" class="let" id="dosuno"><img src="/img/pcat.png" alt="Anterior" border="0" /></a></li> <li><a href="/genero/ficcion.html" class="let">Ficci&oacute;n</a></li> <li><a href="/genero/gore.html" class="let">Gore</a></li> <li><a href="/genero/harem.html" class="let">Harem</a></li> <li><a href="/genero/horror.html" class="let">Horror</a></li> <li><a href="/genero/josei.html" class="let">Josei</a></li> <li><a href="/genero/lucha.html" class="let">Lucha</a></li> </ul> <ul class="alfa" style="margin-left: 50px;"> <li><a href="/genero/magia.html" class="let">Magia</a></li> <li><a href="/genero/mecha.html" class="let">Mecha</a></li> <li><a href="/genero/militar.html" class="let">Militar</a></li> <li><a href="/genero/misterio.html" class="let">Misterio</a></li> <li><a href="/genero/musica.html" class="let">M&uacute;sica</a></li> <li><a href="javascript:void(0);" class="let" id="dostres"><img src="/img/ncat.png" alt="Siguiente" border="0" /></a></li> </ul> </div>
    <div id="gentres" style="display: none; margin-top:6px;"> <ul class="alfa" style="margin-left: 5px;"> <li><a href="javascript:void(0);" class="let" id="tresdos"><img src="/img/pcat.png" alt="Anterior" border="0" /></a></li> <li><a href="/genero/parodias.html" class="let">Parodias</a></li> <li><a href="/genero/psicologico.html" class="let">Psicol&oacute;gico</a></li> <li><a href="/genero/recuentos-de-la-vida.html" class="let">Recuentos de la Vida</a></li> <li><a href="/genero/romance.html" class="let">Romance</a></li> </ul> <ul class="alfa" style="margin-left: 40px;"> <li><a href="/genero/seinen.html" class="let">Seinen</a></li> <li><a href="/genero/shojo.html" class="let">Shojo</a></li> <li><a href="/genero/shonen.html" class="let">Shonen</a></li> <li><a href="/genero/vampiros.html" class="let">Vampiros</a></li> <li><a href="/genero/yaoi.html" class="let">Yaoi</a></li> <li><a href="/genero/yuri.html" class="let">Yuri</a></li> </ul> </div>
    </div>
    </div>
    '''
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  <a class="accion linkFader" href="../accion-1.html"></a>
    patron  = '<div id="gen[^"]+"(.*?)</div>'
    matches2 = re.compile(patron,re.DOTALL).findall(data)
    
    for match2 in matches2:
        patron = '<li><a href="([^"]+)" class="let">([^<]+)<'
        matches = re.compile(patron,re.DOTALL).findall(match2)
        
        for match in matches:
            scrapedtitle = scrapertools.unescape(match[1])
            scrapedurl = urlparse.urljoin(item.url,match[0])
            scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            itemlist.append( Item(channel=__channel__, action="newlist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def fulllist(item):
    logger.info("[animeid.py] airlist")

    if config.get_setting("forceview")=="true" and config.get_platform()=="xbmcdharma":
        logger.info("Forzando vista")
        import xbmc
        # Confluence: 50,51,550,560,500,501,508,505
        #xbmc.executebuiltin("Container.SetViewMode(550)")  #53=mediainfo

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  <a class="accion linkFader" href="../accion-1.html"></a>
    #<div class="dt">Ultimos Animes Agregados</div> <div class="dm"> <ul> <li><a href="/anime/mobile-suit-gundam-wing.html" title="Mobile Suit Gundam Wing" class="anime">Mobile Suit Gundam
    patronvideos  = '<div class="dt">Lista completa de animes</div> <div class="dm"(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
        patronvideos = '<li><a href="([^"]+)" title="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def airlist(item):
    logger.info("[animeid.py] airlist")

    if config.get_setting("forceview")=="true" and config.get_platform()=="xbmcdharma":
        logger.info("Forzando vista")
        import xbmc
        # Confluence: 50,51,550,560,500,501,508,505
        #xbmc.executebuiltin("Container.SetViewMode(550)")  #53=mediainfo

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  <a class="accion linkFader" href="../accion-1.html"></a>
    #<div class="dt">Ultimos Animes Agregados</div> <div class="dm"> <ul> <li><a href="/anime/mobile-suit-gundam-wing.html" title="Mobile Suit Gundam Wing" class="anime">Mobile Suit Gundam
    patronvideos  = '<div class="dt">Series en Emisi\&oacute\;n</div> <div class="dm">(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
        patronvideos = '<li><a href="([^"]+)" title="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def animelist(item):
    logger.info("[animeid.py] animelist")

    if config.get_setting("forceview")=="true" and config.get_platform()=="xbmcdharma":
        logger.info("Forzando vista")
        import xbmc
        # Confluence: 50,51,550,560,500,501,508,505
        #xbmc.executebuiltin("Container.SetViewMode(550)")  #53=mediainfo

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  <a class="accion linkFader" href="../accion-1.html"></a>
    #<div class="dt">Ultimos Animes Agregados</div> <div class="dm"> <ul> <li><a href="/anime/mobile-suit-gundam-wing.html" title="Mobile Suit Gundam Wing" class="anime">Mobile Suit Gundam
    patronvideos  = '<div class="dt">Ultimos Animes Agregados</div> <div class="dm">(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        data = matches[0]
        patronvideos = '<li><a href="([^"]+)" title="([^"]+)"'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def chaplist(item):
    logger.info("[animeid.py] chaplist")

    if config.get_setting("forceview")=="true" and config.get_platform()=="xbmcdharma":
        logger.info("Forzando vista")
        import xbmc
        # Confluence: 50,51,550,560,500,501,508,505
        #xbmc.executebuiltin("Container.SetViewMode(550)")  #53=mediainfo

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  <a class="accion linkFader" href="../accion-1.html"></a>
    #<div class="a"> <a href="/ver/dragon-ball-kai-94.html" title="Dragon Ball Kai 94"><img src="http://img.animeid.com/dbk.jpg" alt="Dragon Ball Kai" width="49" height="71" border="0" /></a> <div class="at"><a href="/ver/dragon-ball-kai-94.html" title="Dragon Ball Kai 94">Dragon Ball Kai 94</a></div> <div class="at" style="margin-top:0px"><span>Publicado: 21/02/2011</span></div> <div class="ad">Despu�s de los rumores que llevaban tiempo apuntando a que se realizar�a una nueva serie de Dra&hellip;</div> </div>
    patronvideos  = '<div class="a"> <a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, viewmode="movie"))

    return itemlist


def newlist(item):
    logger.info("[animeid.py] newlist")

    if config.get_setting("forceview")=="true" and config.get_platform()=="xbmcdharma":
        logger.info("Forzando vista")
        import xbmc
        # Confluence: 50,51,550,560,500,501,508,505
        #xbmc.executebuiltin("Container.SetViewMode(550)")  #53=mediainfo

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  <a class="accion linkFader" href="../accion-1.html"></a>
    # <div class="bl"> <a href="/anime/mobile-suit-gundam-wing.html" title="Mobile Suit Gundam Wing"><img src="http://img.animeid.com/mobilesuitgundam.gif" alt="Mobile Suit Gundam Wing" width="166" height="250" border="0" class="im" /></a> <div class="tt"> <h1><a href="/anime/mobile-suit-gundam-wing.html" title="Mobile Suit Gundam Wing">Mobile Suit Gundam Win&hellip;</a></h1></div> </div>
    patronvideos  = '<div class="bl"> <a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, viewmode="movie"))

    return itemlist

def destacados(item):
    logger.info("[animeid.py] destacados")

    if config.get_setting("forceview")=="true" and config.get_platform()=="xbmcdharma":
        logger.info("Forzando vista")
        import xbmc
        # Confluence: 50,51,550,560,500,501,508,505
        #xbmc.executebuiltin("Container.SetViewMode(550)")  #53=mediainfo

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)  <a class="accion linkFader" href="../accion-1.html"></a>
    patronvideos  = "\$\('w_fss'\).slideshow \= new FeaturedSlideshow\(\[(.*?)\]\)\;"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches)>0:
        data = matches[0]

        patronvideos  = '\{"series_name"\:"([^"]+)"\,"media_name"\:"([^"]+)"\,"description"\:"([^"]+)"\,"image"\:"([^"]+)","url":"([^"]+)".*?\}'
        scrapertools.printMatches(matches)
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

    itemlist = []
    
    for match in matches:
        scrapedtitle = match[0]+" "+match[1]
        scrapedurl = urlparse.urljoin(item.url,match[4])
        scrapedthumbnail = match[3].replace("\\/","/")
        scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, viewmode="movie_with_plot", fanart=scrapedthumbnail))

    return itemlist

def serie(item):
    logger.info("[animeid.py] serie")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Saca el argumento
    patronvideos  = '<div class="sinop">(.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches)>0:
        scrapedplot = scrapertools.htmlclean( matches[0] )
    
    # Saca enlaces a los episodios
    patronvideos  = '<li class="lcc"><a href="([^"]+)" class="lcc">([^<]+)</a></li>'
    scrapertools.printMatches(matches)
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    itemlist = []
    
    for match in matches:
        scrapedtitle = scrapertools.entityunescape( match[1] )
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        #scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    # mainlist
    mainlist_items = mainlist(Item())

    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            if len(itemlist)==0:
                return false

    # Da por bueno el canal si alguno de los vídeos de las series en "Destacados" devuelve mirrors
    series_items = destacados(mainlist_items[0])
    episodios_items = serie(series_items[0])
    bien = False
    for episodio_item in episodios_items:
        mirrors = servertools.find_video_items(item=episodio_item)
        if len(mirrors)>0:
            bien = True
            break
    
    return bien