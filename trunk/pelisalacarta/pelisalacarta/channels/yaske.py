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
    itemlist.append( Item(channel=__channel__, title="Novedades"          , action="menu_novedades", url="http://www.yaske.net/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Por categorías"     , action="menu_categorias", url="http://www.yaske.net/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Por calidades"      , action="menu_calidades", url="http://www.yaske.net/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Buscar"             , action="search") )

    return itemlist

def menu_novedades(item):
    logger.info("[yaske.py] menu_novedades")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Portada"            , action="peliculas", url="http://www.yaske.net/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Más vistas hoy"     , action="peliculas", url="http://www.yaske.net/es/peliculas/custom/?show=today"))
    itemlist.append( Item(channel=__channel__, title="Novedades latino"   , action="peliculas", url="http://www.yaske.net/es/peliculas/custom/?show=new&language=la"))
    itemlist.append( Item(channel=__channel__, title="Novedades español"  , action="peliculas", url="http://www.yaske.net/es/peliculas/custom/?show=new&language=es"))
    itemlist.append( Item(channel=__channel__, title="Novedades subtitulos", action="peliculas", url="http://www.yaske.net/es/peliculas/custom/?show=new&language=sub"))

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
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    patron  = '<div class="itemdos c(\d+)" id="numitem\d+"><div class="img_box"><a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"[^<]+</a[^<]+'
    patron += '<div class="quality">([^<]+)</div><div class="view"><span>[^<]+</span></div></div[^<]+'
    patron += '<div class="bttm"><div class="br"></div><div class="ttl"><a href="[^"]+" title="[^"]+">([^<]+)</a></div><div class="tori">([^<]+)</div[^<]+'
    patron += '<div class="idiom.s">(.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for idcalidad, scrapedurl, scrapedthumbnail, calidad, scrapedtitle, categorias, idiomas in matches:
        
        patronidiomas = '<img src="[^"]+" title="([^"]+)"'
        matchesidiomas = re.compile(patronidiomas,re.DOTALL).findall(idiomas)
        idiomas_disponibles = ""
        for idioma in matchesidiomas:
            idiomas_disponibles = idiomas_disponibles + idioma.strip() + "/"
        if len(idiomas_disponibles)>0:
            idiomas_disponibles = "["+idiomas_disponibles[:-1]+"]"
        
        title = scrapedtitle.strip()+" "+idiomas_disponibles+"["+calidad+"]"
        title = scrapertools.htmlclean(title)
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

def menu_categorias(item):
    logger.info("[yaske.py] menu_categorias")

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    data = scrapertools.get_match(data,'cc-type="generos">(.*?)</div>')
    logger.info("data="+data)

    '''
    <div cc-type="generos">
    <li><a href="http://www.yaske.net/es/peliculas/genero/drama" cc-value="drama">Drama</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/romance" cc-value="romance">Romance</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/comedy" cc-value="comedy">Comedias</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/crime" cc-value="crime">Crimen</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/action" cc-value="action">Accion</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/thriller" cc-value="thriller">Thrillers</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/war" cc-value="war">Guerra</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/adventure" cc-value="adventure">Aventura</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/mystery" cc-value="mystery">Misterio</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/family" cc-value="family">Familiar</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/history" cc-value="history">Historica</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/musical" cc-value="musical">Musicales</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/biography" cc-value="biography">Biografias</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/horror" cc-value="horror">Terror</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/fantasy" cc-value="fantasy">Fantasia</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/music" cc-value="music">Musica</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/western" cc-value="western">Westerns</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/sci_fi" cc-value="sci_fi">ciencia Ficcion</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/sport" cc-value="sport">Deporte</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/film_noir" cc-value="film_noir">Cine negro</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/animation" cc-value="animation">Animacion</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/adult" cc-value="adult">Adultos</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/news" cc-value="news">Noticia</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/reality_tv" cc-value="reality_tv">Reality-TV</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/talk_show" cc-value="talk_show">Espectaculos</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/animes" cc-value="animes">Animes</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/trailers" cc-value="trailers">Proximos</a></li><li><a href="http://www.yaske.net/es/peliculas/genero/premieres" cc-value="premieres">Estrenos</a></li></div>
    </div>
    '''

    # Extrae las entradas
    patron  = '<li><a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for scrapedurl,scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def menu_calidades(item):
    logger.info("[yaske.py] menu_calidades")

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)
    data = scrapertools.get_match(data,'cc-type="calidades">(.*?)</div>')
    logger.info("data="+data)


    '''
    <div class="ccbutton shadow right hd" style="right:540px;" cc-type="calidades">Calidades
    <div class="menu">
    <a href="http://www.yaske.net/es/peliculas/custom/?calidad=c8" cc-value="c8">HD REAL 720</a>
    <a href="http://www.yaske.net/es/peliculas/custom/?calidad=c7" cc-value="c7">HD-RIP 320</a>
    <a href="http://www.yaske.net/es/peliculas/custom/?calidad=c6" cc-value="c6">BR-SCREENER</a>
    <a href="http://www.yaske.net/es/peliculas/custom/?calidad=c5" cc-value="c5">DVD-RIP</a>
    <a href="http://www.yaske.net/es/peliculas/custom/?calidad=c4" cc-value="c4">DVD-SCREENER</a>
    <a href="http://www.yaske.net/es/peliculas/custom/?calidad=c3" cc-value="c3">TS-SCREENER HQ</a>
    <a href="http://www.yaske.net/es/peliculas/custom/?calidad=c2" cc-value="c2">TS-SCREENER</a>
    <a href="http://www.yaske.net/es/peliculas/custom/?calidad=c1" cc-value="c1">CAM</a>
    </div>
    '''

    # Extrae las entradas
    patron  = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
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
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    '''
    <tr bgcolor="#e6e3e3"><td align="left" >
    <a href="http://www.yaske.net/es/reproductor/pelicula/2148/15588/" title="El origen de los guardianes" target="_blank" style="text-decoration: none;"><img src="http://www.yaske.net/imagenes/servers/veronline.png" height="19" width="19"><font color="black">Opcion 1</font></a>
    </td> <td align="left"><span style="margin-left:15px;"><img src="http://www.google.com/s2/favicons?domain=www.putlocker.com" />putlocker</span>
    </td> <td align="left"><span style="margin-left:15px;"><img src="http://www.yaske.net/imagenes/flags/en_es.png" width="19"> Subtitulada</span></td> 
    <td align="center" class="center">
    <span title="HD REAL 720" style="text-transform:capitalize;">hd real 720</span></td> <td align="center" class="center">
    <span title="HD REAL 720" style="text-transform:capitalize;">
    <div class="star on"><a href="javascript:void(0)" onClick="foo()"  style="width: 100%;">1</a></div>
    <div class="star on"><a href="javascript:void(0)" onClick="foo()"  style="width: 100%;">1</a></div>
    <div class="star on"><a href="javascript:void(0)" onClick="foo()"  style="width: 100%;">1</a></div>
    <div class="star on"><a href="javascript:void(0)" onClick="foo()"  style="width: 100%;">1</a></div>
    <div class="star on"><a href="javascript:void(0)" onClick="foo()"  style="width: 100%;">1</a></div>
    </span>
    </td> <td align="center"> 
    <a class="btn btn-mini enlace_link" style="text-decoration:none;color:#0088cd;" rel="nofollow" target="_blank" title="Ver..." href="http://www.yaske.net/es/reproductor/pelicula/2148/15588/"><i class="icon-play"></i>&nbsp;&nbsp;Reproducir</a>
    </td> <td align="center" class="center">19395 visitas.</td> </tr>
    '''
    patron  = '<tr bgcolor=(.*?)</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for tr in matches:
        logger.info("tr="+tr)
        try:
            title = scrapertools.get_match(tr,'<font color="black">([^<]+)</font>')
            server = scrapertools.get_match(tr,'"http\://www.google.com/s2/favicons\?domain\=([^"]+)"')
            idioma = scrapertools.get_match(tr,'<img src="http://www.yaske.net/imagenes/flags/([a-z_]+).png"[^>]+>[^<]+</span>')
            subtitulos = scrapertools.get_match(tr,'<img src="http://www.yaske.net/imagenes/flags/[^"]+"[^>]+>([^<]+)</span>')
            calidad = scrapertools.get_match(tr,'<td align="center" class="center"[^<]+<span title="[^"]+" style="text-transform:capitalize;">([^<]+)</span></td>')
            
            #<a href="http://www.yaske.net/es/reproductor/pelicula/2244/15858/" title="Batman: El regreso del Caballero Oscuro, Parte 2"
            url = scrapertools.get_match(tr,'<a href="([^"]+)" title="[^"]+"')
            thumbnail = scrapertools.get_match(data,'<meta\s+property="og\:image"\s+content="([^"]+)"')
            plot = scrapertools.get_match(data,'<meta\s+property="og:description"\s+content="([^"]+)"')

            if "es_es" in idioma:
                scrapedtitle = title + " en "+server.strip()+" [Español]["+calidad+"]"
            elif "la_la" in idioma:
                scrapedtitle = title + " en "+server.strip()+" [Latino]["+calidad+"]"
            elif "en_es" in idioma:
                scrapedtitle = title + " en "+server.strip()+" [Inglés SUB Español]["+calidad+"]"
            else:
                scrapedtitle = title + " en "+server.strip()+" ["+idioma+" / "+subtitulos+"]["+calidad+"]"
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