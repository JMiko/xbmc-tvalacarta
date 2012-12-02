# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinemastreaming
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
__title__ = "cinemastreaming"
__channel__ = "cinemastreaming"
__language__ = "ES"
__creationdate__ = "20121105"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cinemastreaming.py] mainlist")
    item.url="http://www.cinemastreaming.net/"
    return menu(item)

def menu(item):
    logger.info("[cinemastreaming.py] menu")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<li><a class="home" href="http://www.cinemastreaming.net">Home</a></li>(.*?)</ul>')
    
    patron = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)    

    i=1
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip().replace("&#8211;","-")
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        if i>=2 and i<=6:
            itemlist.append( Item(channel=__channel__, action="listado" , title=title , url=url, thumbnail=thumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/cinemastreaming.jpg", plot=plot))
        i = i + 1

    return itemlist

def listado(item):
    logger.info("[cinemastreaming.py] listado")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    '''
    <div class="archive">
    <div class="thumb left">
    <a href="http://www.cinemastreaming.net/la-scomparsa-di-haruhi-suzumiya-2010-anime-japsubita-completa/" rel="bookmark"><img src="http://www.cinemastreaming.net/wp-content/themes/portal/includes/timthumb.php?src=http://www.cinemastreaming.net/wp-content/uploads/2012/11/La-scomparsa-di-Haruhi-Suzumiya.jpg&amp;h=100&amp;w=100&amp;zc=1" alt="La scomparsa di Haruhi Suzumiya (2010) (Anime) (JAP/subITA) (Completa)" /></a>
    </div> <!--end: thumb-->
    <h2><a href="http://www.cinemastreaming.net/la-scomparsa-di-haruhi-suzumiya-2010-anime-japsubita-completa/" rel="bookmark">La scomparsa di Haruhi Suzumiya (2010) (Anime) (JAP/subITA) (Completa)</a></h2>
    
    Trama:
    È circa metà dicembre ed il capo della SOS Brigade Haruhi Suzumiya annuncia ai propri compagni che la brigata terrà un party natalizio nell&#8217;aula del proprio club. I membri del club Kyon, Yuki Nagato, Mikuru Asahina ed Itsuki Koizumi si...    	<div class="clear"></div>
    </div> <!--end: archive-->
    '''
    patron  = '<div class="archive">[^<]+'
    patron += '<div class="thumb left">[^<]+'
    patron += '<a href="([^"]+)"[^<]+<img src="http.//www.cinemastreaming.net/wp-content/themes/portal/includes/timthumb.php.src=([^\&]+)\&[^"]+"[^<]+</a>[^<]+'
    patron += '</div> <!--end. thumb-->[^<]+'
    patron += '<h2><a[^>]+>([^<]+)</a></h2>(.*?)</div> <!--end. archive-->'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapedplot in matches:
        title = scrapedtitle.strip().replace("&#8211;","-")
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        plot = scrapedplot.strip()
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=title , url=url, thumbnail=thumbnail, fanart="http://pelisalacarta.mimediacenter.info/fanart/cinemastreaming.jpg", plot=plot, viewmode="movie_with_plot"))

    try:
        siguiente = scrapertools.get_match(data,"<span class='current'>[^<]+</span><a href='([^']+)'")
        scrapedurl = urlparse.urljoin(item.url,siguiente)
        scrapedtitle = ">> Pagina Siguiente"
        scrapedthumbnail = ""
        scrapedplot = ""

        itemlist.append( Item(channel=__channel__, action="listado", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    except:
        pass
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
                mirrors = findvideos(item=itemlist[0])
                if len(mirrors)>0:
                    return True

    return False