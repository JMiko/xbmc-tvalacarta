# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesdanko.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

PLUGIN_NAME = "pelisalacarta"

__channel__ = "seriesdanko"
__category__ = "S"
__type__ = "generic"
__title__ = "Seriesdanko"
__language__ = "ES"

DEBUG = config.get_setting("debug")

if config.get_system_platform() == "xbox":
    MaxResult = "55"
else:
    MaxResult = "500"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesdanko.py] mainlist")
    item.url = 'http://www.seriesdanko.org/'
    return series(item)

def series(item):
    logger.info("[seriesdanko.py] completo")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"Listado de series disponibles</h2>(.*?)<div class='clear'></div>")

    # Extrae las entradas (carpetas)
    #<a dir='ltr' href='http://www.seriesdanko.org/search/label/White%20Collar'>White Collar</a>
    patronvideos  = "<a.*?href='([^']+)'>([^<]+)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    totalItems = len(matches)
    for url,title in matches:
        scrapedtitle = title.replace("\n","").replace("\r","")
        scrapedurl = url
        scrapedurl = urlparse.urljoin(item.url,scrapedurl.replace("\n","").replace("\r",""))
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="episodios" , title=scrapedtitle , show=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, fulltitle = scrapedtitle , totalItems = totalItems))

    return itemlist

def detalle_programa(item):
    data = scrapertools.cache_page(item.url)

    # Argumento
    '''
    <i>Informacion de Continuum:</i><br />
    <div style="border-bottom-color: #C0C0C0; border-bottom-style: solid; border-bottom-width: 1px;">
    </div>
    <br />
    <div class="separator" style="clear: both; text-align: center;">
    <a href="http://3.bp.blogspot.com/-a7E5QNadVOw/UAmuh6Zwm2I/AAAAAAAAAWM/oxu6-O60VCA/s1600/Continuum.jpg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" height="200" src="http://3.bp.blogspot.com/-a7E5QNadVOw/UAmuh6Zwm2I/AAAAAAAAAWM/oxu6-O60VCA/s200/Continuum.jpg" width="138" /></a></div>
    <div style="text-align: justify;">
    Continuum es una serie de ciencia ficción canadiense que se centra en el conflicto entre un policía y un grupo de rebeldes desde el año 2077, que el tiempo de viaje a Vancouver, BC, en el año 2012. Se estrenó el Showcase el 27 de mayo de 2012. [1] La primera temporada constará de 10 episodios.</div>
    </div>
    '''
    patron = '<img border="0" height="\d+" src="([^"]+)" width="\d+"[^<]+</a></div>[^<]+'
    patron += '<div style="text-align. justify.">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.plot = scrapertools.htmlclean(matches[1]).strip()
        item.thumbnail = matches[0]

    return item

def episodios(item):
    logger.info("[seriesdanko.py] episodios")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<div class='post-body entry-content' id='post-body[^<]+"+'<div dir="ltr" style="text-align. left;" trbidi="on">(.*?)</ul>')
    patron = '<a href="([^"]+)">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for url,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , fulltitle = item.fulltitle, show = item.show , context="4", folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools

    lista_series = mainlist(Item())
    bien = False
    for una_serie in lista_series:
        lista_episodios = episodios(una_serie)
        
        for un_episodio in lista_episodios:
            
            lista_mirros = servertools.find_video_items(item=un_episodio)

            if len(lista_mirros)>0:
                return True

    return False