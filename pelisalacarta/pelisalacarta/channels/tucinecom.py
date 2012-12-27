# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tucinecom
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "tucinecom"
__category__ = "F"
__type__ = "generic"
__title__ = "tucinecom"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tucinecom.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="peliculas"    , title="Peliculas"    , url="http://www.tucinecom.com/" ))
    itemlist.append( Item(channel=__channel__ , action="novedades"    , title="Documentales" , url="http://tucinecom.com/Pel%C3%ADculas/documentales/" ))

    return itemlist

def peliculas(item):
    logger.info("[tucinecom.py] peliculas")

    itemlist = []
    itemlist.append( Item(channel=__channel__ , action="novedades"    , title="Novedades"    , url="http://tucinecom.com/Pel%C3%ADculas/peliculas/" ))
    itemlist.append( Item(channel=__channel__ , action="letras"       , title="Alfabético"   , url="http://tucinecom.com/Pel%C3%ADculas/peliculas/" ))
    itemlist.append( Item(channel=__channel__ , action="generos"      , title="Géneros"      , url="http://tucinecom.com/Pel%C3%ADculas/peliculas/" ))
    itemlist.append( Item(channel=__channel__ , action="idiomas"      , title="Idiomas"      , url="http://tucinecom.com/Pel%C3%ADculas/peliculas/" ))

    return itemlist

def novedades(item):
    logger.info("[tucinecom.py] novedades")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <div class="review-box review-box-compact" style="width: 140px;">
    <!--Begin Image1-->
    <div class="post-thumbnail">
    <!--User Rating-->
    <div class="review-box-stars">
    <div style="display: none">VN:RO [1.9.21_1169]</div><div class="ratingblock "><div class="ratingheader "></div><div class="ratingstars "><div id="article_rater_5293" class="ratepost gdsr-oxygen gdsr-size-12"><div class="starsbar gdsr-size-12"><div class="gdouter gdheight"><div id="gdr_vote_a5293" style="width: 0px;" class="gdinner gdheight"></div></div></div></div></div><div class="ratingtext "><div id="gdr_text_a5293" class="inactive">Rating: 0.0/<strong>10</strong> (0 votes cast)</div></div></div>										
    </div>					
    <a href="http://tucinecom.com/pelicula/super-tormenta-2012-ver-online-y-descargar-gratis/" title="Super Tormenta (2012) Ver Online Y Descargar Gratis">
    <img src="http://tucinecom.com/wp-content/uploads/2012/12/supertwister-e1356326241567-140x210.jpg" alt="Super Tormenta (2012) Ver Online Y Descargar Gratis" />		
    </a>	
    <div id="mejor_calidad">
    <a href="http://tucinecom.com/pelicula/super-tormenta-2012-ver-online-y-descargar-gratis/" title="Super Tormenta (2012) Ver Online Y Descargar Gratis"><img id="espanol" src="http://tucinecom.com/wp-content/themes/reviewit/images/HD-R_calidad.png" class="idiomas" alt="Super Tormenta (2012) Ver Online Y Descargar Gratis" />	
    </a>
    <span>HD-R</span></div>		
    </div>					
    <!--End Image-->
    <div class="review-box-text">
    <h2><a href="http://tucinecom.com/pelicula/super-tormenta-2012-ver-online-y-descargar-gratis/" title="Super Tormenta (2012) Ver Online Y Descargar Gratis">Super Tormenta (2012) Ver Onli...</a></h2>	
    <p>El vórtice de alta presión del famoso Júpiter se ha ido. Cuando las tormentas gigantes comienzan ...</p>										
    </div>
    <div id="campos_idiomas">				
    <img id="espanol" src="http://tucinecom.com/wp-content/themes/reviewit/images/s.png" class="idiomas" alt="" />
    <img id="latino" src="http://tucinecom.com/wp-content/themes/reviewit/images/lx.png" class="idiomas" alt="" />
    <img id="ingles" src="http://tucinecom.com/wp-content/themes/reviewit/images/ix.png" class="idiomas" alt="" />
    <img id="vose" src="http://tucinecom.com/wp-content/themes/reviewit/images/vx.png" class="idiomas" alt="" />
    </div>
    </div>
    '''
    patron  = '<div class="review-box review-box-compact.*?'
    patron += '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</a[^<]+'
    patron += '<div id="mejor_calidad"[^<]+'
    patron += '<a[^<]+<img[^<]+'
    patron += '</a[^<]+'
    patron += '<span>([^<]+)</span></div[^<]+'
    patron += '</div[^<]+'
    patron += '<!--End Image--[^<]+'
    patron += '<div class="review-box-text"[^<]+'
    patron += '<h2[^<]+<a[^<]+</a></h2>[^<]+'
    patron += '<p>([^<]+)</p[^<]+'
    patron += '</div[^<]+'
    patron += '<div id="campos_idiomas">(.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail,calidad,scrapedplot,idiomas in matches:
        scrapedtitle = scrapedtitle.replace("Ver Online Y Descargar Gratis","").strip()
        scrapedtitle = scrapedtitle.replace("Ver Online Y Descargar gratis","").strip()
        scrapedtitle = scrapedtitle.replace("Ver Online Y Descargar","").strip()
        title=scrapedtitle+" ("+calidad+") ("
        if "s.png" in idiomas:
            title=title+"ESP,"
        if "l.png" in idiomas:
            title=title+"LAT,"
        if "i.png" in idiomas:
            title=title+"ING,"
        if "v.png" in idiomas:
            title=title+"VOSE,"
        title = title[:-1]+")"
        url=urlparse.urljoin(item.url,scrapedurl)
        thumbnail=urlparse.urljoin(item.url,scrapedthumbnail)
        plot=scrapedplot.strip()
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , viewmode="movies_with_plot", folder=True) )

    try:
        next_page = scrapertools.get_match(data,"<a href='([^']+)'>\&rsaquo\;</a>")
        itemlist.append( Item(channel=__channel__, action="novedades", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page) , folder=True) )
    except:
        try:
            next_page = scrapertools.get_match(data,"<span class='current'>\d+</span><a href='([^']+)'")
            itemlist.append( Item(channel=__channel__, action="novedades", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page) , folder=True) )
        except:
            pass
        pass

    return itemlist

def letras(item):
    logger.info("[tucinecom.py] letras")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<div id="alphaList" align="center">(.*?)</div>')

    # Extrae las entradas
    patron  = '<a href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title=scrapedtitle.strip()
        url=urlparse.urljoin(item.url,scrapedurl)
        thumbnail=""
        plot=""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def generos(item):
    logger.info("[tucinecom.py] generos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<li class="cat-item cat-item-\d+"><a href="http...tucinecom.com/Pel.*?s/generos/"[^<]+</a>(.*?)</ul>')

    # Extrae las entradas
    patron  = '<li class="cat-item cat-item-\d+"><a href="([^"]+)"[^>]+>([^<]+)</a>\s+\((\d+)\)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,cuantas in matches:
        title=scrapedtitle.strip()+" ("+cuantas+")"
        url=urlparse.urljoin(item.url,scrapedurl)
        thumbnail=""
        plot=""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def idiomas(item):
    logger.info("[tucinecom.py] idiomas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<div class="widget"><h3>Versiones</h3>(.*?)</ul>')

    # Extrae las entradas
    patron  = '<li class="cat-item cat-item-\d+"><a href="([^"]+)"[^>]+>([^<]+)</a>\s+\((\d+)\)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,cuantas in matches:
        title=scrapedtitle.strip()+" ("+cuantas+")"
        url=urlparse.urljoin(item.url,scrapedurl)
        thumbnail=""
        plot=""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="novedades", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def findvideos(item):
    itemlist = servertools.find_video_items(item)

    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.thumbnail = item.thumbnail
        videoitem.fulltitle = item.title
        videoitem.title = "Ver en ["+videoitem.server+"]"
    
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien