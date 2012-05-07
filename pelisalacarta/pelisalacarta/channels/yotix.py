# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para yotix
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "yotix"
__category__ = "A"
__type__ = "generic"
__title__ = "Yotix.tv"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[yotix.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="series"     , title="Novedades", url="http://yotixanime.com/"))
    itemlist.append( Item(channel=__channel__, action="categorias" , title="Categorías", url="http://yotixanime.com/"))
    itemlist.append( Item(channel=__channel__, action="alfabetico" , title="Alfabético", url="http://yotixanime.com/"))
    itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar"))

    return itemlist

def search(item,texto):
    logger.info("[yotix.py] search")

    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://yotixanime.com/?s=%s"

        # Reemplaza el texto en la cadena de búsqueda
        item.url = item.url % texto

        # Devuelve los resultados
        return videolist(item)
    
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def categorias(item):
    logger.info("[yotix.py] categorias")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas de la home como carpetas
    patron  = '<a class="generos" title="Ver todos los animes[^"]+" href="(http\://yotixanime.com/categoria[^"]+)">([^>]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def alfabetico(item):
    logger.info("[yotix.py] alfabetico")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas de la home como carpetas
    patron = '<a href="(http\://yotixanime.com/tag[^"]+)" title="Ver todos los animes de letra[^"]+" class="alfb">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist


def series(item):
    logger.info("[yotix.py] videolist")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas de la home como carpetas
    '''
    <h2><a href="http://yotixanime.com/they-are-my-noble-masters-kimi-ga-aruji-de-shitsuji-ga-ore-de/" rel="bookmark">Kimi ga Aruji de Shitsuji ga Ore de ~They Are My Noble Masters~</a></h2><div class="entry"> <a title="Ver Serie Kimi ga Aruji de Shitsuji ga Ore de ~They Are My Noble Masters~" href="http://yotixanime.com/they-are-my-noble-masters-kimi-ga-aruji-de-shitsuji-ga-ore-de/"><img class="imagen" src="http://yotixanime.com/caratula/Kimi ga Aruji de Shitsuji ga Ore de.jpg" border="0" /></a><p>Uesugi Ren y su hermana Mihato, tras escapar de su violento padre y la terrible vida que tenían junto a él, deciden empezar una nueva vida juntos. Ren desea poder cuidar de su querida hermana mayor, pero pronto los fondos se acaban y necesita encontrar pronto un trabajo (y no quiere aceptar el ofrecimiento de su hermanad para hacer de modelo). La oportunidad se presenta con las hermanas Kuonji: Shinra, Miyu y Yume; unas chicas de familia rica que parecen siempre necesitar de más mayordomos. Sin nada que perder y no queriendo que su hermana haga otro tipo de labor, Ren y Mihato se unen al staff de sirvientes de la familia; donde tendrán que convivir con los demás mayordomos y sirvientas en busca de complacer a sus queridas amas.</p><div class="clear"></div></div></div>
    '''
    patron  = '<div class="entry"> <a title="([^"]+)" href="([^"]+)">'
    patron += '<img class="imagen" src="([^"]+)" border="0" /></a>'
    patron += '<p>(.*?)</p><div class="clear"></div></div></div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []

    for scrapedtitle,scrapedurl,scrapedthumbnail,scrapedplot in matches:
        scrapedtitle = scrapedtitle.replace("Ver Serie ","")
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        scrapedthumbnail = scrapedthumbnail.replace(" ","%20")
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, fanart=scrapedthumbnail, plot=scrapedplot))

    # Extrae la página siguiente
    #<a href='http://yotixanime.com/pagina/2/' class='nextpostslink'>
    patron = "<a href='([^']+)' class='nextpostslink'>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = "!Pagina siguiente >>"
        scrapedurl = match
        scrapedthumbnail = ""
        scrapeddescription = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="series" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def episodios(item):
    logger.info("[yotix.py] episodios")
    itemlist=[]
    
    data = scrapertools.cachePage(item.url)
    #<a class="azul" href="http://yotixanime.com/rt/kissxsis-capitulo-4/9f44885c43a61e9a337f9ce598078baa/" target="_blank">Capitulo 04 &#8211; Notas de un Amante</a>
    patronvideos  = '<a class="azul" href="([^"]+)" target="_blank">(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot))

    return itemlist