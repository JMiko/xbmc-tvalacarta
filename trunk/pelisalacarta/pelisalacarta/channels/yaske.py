# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para yaske
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "yaske"
__category__ = "F"
__type__ = "generic"
__title__ = "Yaske.net"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[yaske.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Portada"            , action="peliculas", url="http://www.yaske.net/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Más vistas hoy"     , action="peliculas", url="http://www.yaske.net/es/peliculas/custom/?show=today"))
    itemlist.append( Item(channel=__channel__, title="Novedades latino"   , action="peliculas", url="http://www.yaske.net/es/peliculas/custom/?show=new&language=la"))
    itemlist.append( Item(channel=__channel__, title="Novedades español"  , action="peliculas", url="http://www.yaske.net/es/peliculas/custom/?show=new&language=es"))
    itemlist.append( Item(channel=__channel__, title="Novedades subtitulos", action="peliculas", url="http://www.yaske.net/es/peliculas/custom/?show=new&language=sub"))
    itemlist.append( Item(channel=__channel__, title="Categorías"         , action="categorias", url="http://www.yaske.net/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Buscar"             , action="search") )

    return itemlist
	
def search(item,texto):

    logger.info("[yaske.py] search")
    itemlist = []

    try:
        item.url = "http://www.yaske.net/es/peliculas/search/%s"
        item.url = item.url % texto
        item.extra = ""
        itemlist.extend(peliculas(item))
        itemlist = sorted(itemlist, key=lambda Item: Item.title) 
        
        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("[yaske.py] listado")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)

    '''
    <li class="item-movies c5">
    <a class="image-block" href="http://www.yaske.net/es/pelicula/0002504/ver-una-pistola-en-cada-mano-online.html" title="Una pistola en cada mano">
    <img src="http://3.bp.blogspot.com/-GKHvyF8P9Kc/UKPNxqI3uJI/AAAAAAAATPY/aS5SkJMX_wI/s640/una-pistola-en-cada-mano.jpg" width="140" height="200" />
    </a>
    <ul class="bottombox">
    <li title="Una pistola en cada mano"><a href="http://www.yaske.net/es/pelicula/0002504/ver-una-pistola-en-cada-mano-online.html" title="Una pistola en cada mano">Una pistola en cad&hellip;</a></li>
    <li>Comedias</li>
    <li><img src='http://www.yaske.net/theme/01/data/images/flags/es_es.png' title='Spanish ' width='25'/> </li>
    <li><a rel="lyteframe" rev="width: 600px; height: 380px; scrolling: no;" youtube="trailer" href="http://www.youtube.com/v/M6EuKQHLUPo&amp;hl&amp;autoplay=1" target="_blank"><img src="http://2.bp.blogspot.com/-hj7moVFACQU/UBoi0HAFeyI/AAAAAAAAA9o/2I2KPisYtsk/s1600/vertrailer.png" height="22" border="0"></a></li>
    </ul>
    <div class="quality">Dvd-rip</div>
    <div class="view"><span>view: 232</span></div>
    '''

    # Extrae las entradas
    patron  = '<li class="item-movies[^<]+'
    patron += '<a class="image-block" href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"(.*?)'
    patron += '<div class="quality">([^<]+)</div'

    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for scrapedurl,scrapedtitle,scrapedthumbnail,idiomas,calidad in matches:
        
        patronidiomas = "<img src='http://www.yaske.net/theme/01/data/images/flags[^']+' title='([^']+)'"
        matchesidiomas = re.compile(patronidiomas,re.DOTALL).findall(idiomas)
        idiomas_disponibles = ""
        for idioma in matchesidiomas:
            idiomas_disponibles = idiomas_disponibles + idioma.strip() + "/"
        if len(idiomas_disponibles)>0:
            idiomas_disponibles = "["+idiomas_disponibles[:-1]+"]"
        
        title = scrapedtitle.strip()+" "+idiomas_disponibles+"["+calidad+"]"
        url = scrapedurl
        thumbnail = scrapedthumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=scrapedplot , viewmode="movie", folder=True) )

    # Extrae el paginador
    patronvideos  = "<a href='([^']+)'>\&raquo\;</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def categorias(item):
    logger.info("[yaske.py] categorias")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)
    logger.info("data="+data)
    data = scrapertools.get_match(data,'div class="title">Categorias(.*?)</ul>')
    logger.info("data="+data)

    # Extrae las entradas
    #<li><a href='http://www.yaske.net/es/peliculas/genero/drama'>Drama</a></li>
    patron  = "<li><a href='([^']+)'>([^<]+)</a>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for scrapedurl,scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[yaske.py] findvideos url="+item.url)

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)

    # Extrae las entradas
    '''
    <tr bgcolor="">
    <td height="32" align="center">
    <a class="btn btn-mini enlace_link" style="text-decoration:none;" rel="nofollow" target="_blank" title="Ver..." href="http://www.yaske.net/es/reproductor/pelicula/2504/20884/">
    <i class="icon-play"></i><b>&nbsp; Opcion &nbsp; 01</b></a></td>
    <td align="left"><img src="http://www.google.com/s2/favicons?domain=180upload.com" />180upload</td>
    <td align="center"><img src="http://www.yaske.net/theme/01/data/images/flags/es_es.png" width="21">Spa.</td> 
    <td align="center" class="center"><span title="" style="text-transform:capitalize;">dvd-rip</span></td>
    <td align="center"><div class="star_rating" title="DVD-RIP ( 4 de 5 )">
    <ul class="star"><li class="curr" style="width: 80%;"></li></ul>
    </div>
    </td> <td align="center" class="center">128</td> </tr>
    '''
    patron  = '<tr bgcolor="">(.*?)</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    itemlist = []

    for tr in matches:
        try:
            title = scrapertools.get_match(tr,'<i class="icon-play"></i><b>([^<]+)</b>')
            server = scrapertools.get_match(tr,'"http\://www.google.com/s2/favicons\?domain\=([^"]+)"')
            idioma = scrapertools.get_match(tr,'<img src="http\://www.yaske.net/theme/01/data/images/flags/[^"]+"[^>]+>([^<]+)</td>')
            calidad = scrapertools.get_match(tr,'<td align="center" class="center"><span title="" style="text-transform:capitalize;">([^<]+)</span></td>')
            url = scrapertools.get_match(tr,'<a.*?href="([^"]+)">')
            thumbnail = scrapertools.get_match(data,'<meta property="og\:image" content="([^"]+)"/>')
            plot = scrapertools.get_match(data,'<meta property="og:description" content="([^"]+)"/>')
            scrapedtitle = title + " en "+server.strip()+" ["+idioma+" / "+calidad+"]"
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            scrapedtitle = scrapedtitle.strip()
            scrapedurl = url
            scrapedthumbnail = thumbnail
            scrapedplot = plot
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=False) )
        except:
            import traceback
            logger.info("Excepcion: "+traceback.format_exc())

    return itemlist

def play(item):
    logger.info("[yaske.py] play item.url="+item.url)
    
    itemlist=[]
    
    data = scrapertools.downloadpageGzip(item.url)
    #logger.info("data="+data)
    itemlist = servertools.find_video_items(data=data)
    
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien