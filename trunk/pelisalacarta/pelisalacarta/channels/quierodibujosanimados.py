# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para quierodibujosanimados
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
__title__ = "Quiero dibujos animados"
__channel__ = "quierodibujosanimados"
__language__ = "ES"
__creationdate__ = "20121112"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[quierodibujosanimados.py] mainlist")
    item.url="http://www.quierodibujosanimados.com/"
    return series(item)

def series(item):
    logger.info("[quierodibujosanimados.py] series")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h4 style="[^"]+">Dibujos</h4>(.*?)<h4')
    
    patron = '<a target="_top" title="([^"]+)" href="(/cat[^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    for scrapedtitle,scrapedurl in matches:
        title = unicode( scrapedtitle.strip(), "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="episodios" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart="http://pelisalacarta.mimediacenter.info/fanart/quierodibujosanimados.jpg", viewmode="movie_with_plot"))        

    return itemlist

def episodios(item):
    logger.info("[quierodibujosanimados.py] episodios")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    '''
    <h2><a   target="_self"     title="Donald en: El amor es cosa de dos" href="/Donald-en-El-amor-es-cosa-de-dos/990" class="">Donald en: El amor es cosa de dos</a></h2>
    <div class="titulo_inf">
    <a title="El Pato Donald" href="/cat/el-pato-donald/8" class="">El Pato Donald</a>                  <div class="estrellas">         <style> 
    #stars_990 {
    background-image:url(/ico/estrellas16.png);
    background-repeat: no-repeat;
    background-position: -96px 0px;
    height:16px;
    width:80px;
    display:block;
    }
    #stars_990 span { width:8px; height:16px; display:block; float:left; }
    </style>        
    <div id="stars_990"></div>
    </div>
    </div>
    <div class="texto">

    <div id="foto"><a target="_self" title="Donald en: El amor es cosa de dos" href="/Donald-en-El-amor-es-cosa-de-dos/990" class=""><img alt="Donald en: El amor es cosa de dos"  src="/i/thm-El-amor-es-cosa-de-dos.jpg" /></a></div>

    <span class=""><p style="text-align: justify;">En esta ocasi&oacute;n el divertido Pato Donald, se viste con sus mejores galas para ir a visitar a una bella dama. Sus sobrinos pretenden acompa&ntilde;arle a la cita pero....Cap&iacute;tulo titulado <strong>&quot;El amor es cosa de dos&quot;</strong>.</p></span>                 <div class="leer_mas">
    <a href="/Donald-en-El-amor-es-cosa-de-dos/990" class="">Ver dibujos animados</a>                   </div>
    </div>

    '''
    patron  = '<h2><a[^<]+</a></h2>[^<]+'
    patron += '<div class="titulo_inf">[^<]+'
    patron += '<a[^<]+</a[^<]+<div class="estrellas"[^<]+<style[^<]+</style[^<]+'
    patron += '<div id="stars[^<]+</div>[^<]+'
    patron += '</div>[^<]+'
    patron += '</div>[^<]+'
    patron += '<div class="texto"[^<]+'
    patron += '<div id="foto"><a target="_self" title="([^"]+)" href="([^"]+)"[^<]+<img\s+alt="[^"]+"\s+src="([^"]+)"[^<]+</a></div>[^<]+'
    patron += '<span class="">(.*?)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot in matches:
        title = unicode( scrapedtitle.strip(), "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(scrapedplot)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, viewmode="movie_with_plot", fanart="http://pelisalacarta.mimediacenter.info/fanart/quierodibujosanimados.jpg"))

    try:
        siguiente = scrapertools.get_match(data,"<a href='([^']+)'>Siguientes >")
        scrapedurl = urlparse.urljoin(item.url,siguiente)
        scrapedtitle = ">> Pagina Siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""

        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True, fanart="http://pelisalacarta.mimediacenter.info/fanart/quierodibujosanimados.jpg") )
    except:
        pass
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True
    
    from servers import servertools

    # mainlist
    serie_itemlist = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto el buscador)
    for serie_item in serie_itemlist:
        episodio_itemlist = episodios(serie_item)

        for episodio_item in episodio_itemlist:
            mirrors = servertools.find_video_items(item=episodio_item)

            if len(mirrors)>0:
                return True

    return False