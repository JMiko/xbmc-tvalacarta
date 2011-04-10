# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para IB3
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re

try:
    from core import logger
    from core import scrapertools
    from core.item import Item
except:
    # En Plex Media server lo anterior no funciona...
    from Code.core import logger
    from Code.core import scrapertools
    from Code.core.item import Item

logger.info("[ib3.py] init")

DEBUG = True
CHANNELNAME = "ib3"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[ib3.py] mainlist")
    item = Item(url="http://ib3noticies.com/seccio/videoprogrames")
    return episodios(item)

def episodios(item):
    logger.info("[ib3.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae los capítulos
    '''
    <div class="item">                                    
    <h3><a href="http://ib3noticies.com/20110117_133928-una-jornada-per-creure.html" title="Una jornada per creure">Una jornada per creure</a></h3>
    <a href="http://ib3noticies.com/20110117_133928-una-jornada-per-creure.html" target ="_blank" class="item-img"><img src="http://ib3noticies.com/wp-content/plugins/fresh-page/thirdparty/phpthumb/phpThumb.php?src=http://ib3noticies.com/wp-content/files_flutter/1295297815menorcabàsquet.JPG&w=300>&zc=C"></a>
    <p><p>En bàsquet estam pendents de l&#8217;estat de Diego Ciorciari. Ahir a Manresa, el base i líder del Menorca va jugar infiltrat després de rebre un cop al peu. Que pugui jugar dissabte a Valladolid és ara mateix una incògnita.</p>
    </p>
    </div>
    '''
    patron  = '<div class="item">[^<]+'                                    
    patron += '<h3><a href="([^"]+)"[^>]+>([^<]+)</a></h3>[^<]+'
    patron += '<a[^>]+><img src="([^"]+)"></a>[^<]+'
    patron += '<p>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    # Extrae los items
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = match[3]
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="findvideos" , page = scrapedurl, url=scrapedurl, thumbnail=scrapedthumbnail, show=item.show , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patron = "<span class='current'>[^<]+</span><a href='([^']+)' class='page'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    # Extrae los items
    for match in matches:
        scrapedtitle = "!Página siguiente"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , page = scrapedurl, url=scrapedurl, thumbnail=scrapedthumbnail, show=item.show , plot=scrapedplot , folder=True) )

    return itemlist
