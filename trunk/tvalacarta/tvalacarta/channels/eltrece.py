# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para eltrece
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "eltrece"
MAIN_URL = "http://www.eltrecetv.com.ar/listado-capitulos-completos"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[eltrece.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los capítulos completos" , action="novedades", url=MAIN_URL, folder=True) )

    return itemlist

def novedades(item):
    logger.info("[eltrece.py] novedades")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # episodios
    '''
    <div class="box_programa_listado">
    <a href="/sonando-por-cantar-2012/video/54357/4-de-abril-sonando-por-cantar"><img src="http://static.eltrecetv.com.ar/sites/default/files/imagecache/187x137/sonando_3.jpg" alt="4 de abril - Soñando por cantar" title="4 de abril - Soñando por cantar"/></a>
    <h2><a href="/sonando-por-cantar-2012/video/54357/4-de-abril-sonando-por-cantar">4 de abril - Soñando...</a></h2>
    <h3><a href="/programa/sonando-por-cantar-2012">Soñando por cantar</a></h3>
    <div class="small_gris">Este mi&eacute;rcoles 4 de abril, So&ntilde;ando por Cantar -el programa que conduce Mariano I&uacute;dica en El Trece- escogi&oacute; cuatro nuevos aspirantes a participar del Cantando 2012: Sergio Romero, Karen Pintos, el d&uacute;o de Sergio Casco y Pietrina Catapano y Leonardo Zar.
    El imponente coliseo Tr&aacute;nsito Cocomarola acostumbrado a vibrar al son de los acordeones, recibi&oacute;...</div>
    <p><strong></strong></p>
    </div>
    </div>
    '''
    patron  = '<div class="box_programa_listado">[^<]+'
    patron += '<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)[^<]+</a>[^<]+'
    patron += '<h2><a href="[^"]+">[^<]+</a></h2>[^<]+'
    patron += '<h3><a href="[^"]+">([^<]+)</a></h3>[^<]+'
    patron += '<div class="small_gris">([^"]+)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for url,thumbnail,title,show,plot in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = scrapertools.htmlclean(plot)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="eltrece", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=show , folder=False) )

    # Paginación
    #<li class="pager-next"><a href="/listado-capitulos-completos?page=1" title="Ir a la página siguiente" rel="nofollow" class="active">siguiente ›</a></li>
    patron = '<li class="pager-next"><a href="([^"]+)" title="Ir a la p[^"]+" rel="nofollow" class="active">siguiente'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
        scrapedtitle = ">> Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,match)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="novedades", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=show , folder=True) )

    return itemlist
