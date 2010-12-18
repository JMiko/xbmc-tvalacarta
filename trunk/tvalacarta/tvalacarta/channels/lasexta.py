# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta
# Canal para La Sexta
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[lasexta.py] init")

DEBUG = False
CHANNELNAME = "lasexta"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[lasexta.py] mainlist")

    # Descarga la página
    data = scrapertools.cachePage("http://www.lasexta.com/ps3/programas")

    '''
    <a href="http://www.lasexta.com/ps3/programa/quien_vive_ahi/51" class="nvideo_programa" title="quien_vive_ahi">
    <img src="http://www.sitios.lasexta.com/pictures/168043/LASEXTA_PICTURE_20100202_1335168043_crop75sub1.jpg" width="245" height="140" alt="quien_vive_ahi" />
    <span id="nvideo_cortina_10" class="media video_cortina">
    <b class="titulo" title="quien_vive_ahi - 01/01/70"></b>
    </span>
    </a>
    '''

    # Extrae las entradas
    patron  = '<a href="([^"]+)" class="nvideo_programa" title="([^"]+)">[^<]+'
    patron += '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = match[2]
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[lasexta.py] episodios")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)

    '''
    <li>
    <a href="javascript:;" id="315352" class="" title="Título de la fotografía 4" onclick="javascript:creaVideo('http://www.lasexta.com/ps3/playlist/315352','ps3-programas-494842','%C2%BFQui%C3%A9n+vive+ah%C3%AD%3F.+Jueves%2C+21+de+octubre','51','315352');">
    <img src="http://www.sitios.lasexta.com/pictures/215481/pictures_20101020_1601215481_crop70sub1.jpg" width="152" height="85" alt="quien_vive_ahi___jueves__21_de_octubre" />
    <img src="http://www.lasexta.com/media/playstation/img/bg_video_highlight_small.png" width="149" height="58" alt="" class="highlight"/>
    <span id="nvideo_cortina_14" class="media video_cortina">
    <b class="titulo" title="quien_vive_ahi - 21/10/10">21/10/10</b>
    <b class="titulo2" title="quien_vive_ahi___jueves__21_de_octubre">¿Quién vive ahí?. Jueves, 21 de octubre</b>
    </span>
    </a>
    </li>
    '''

    patron  = '<li>[^<]+'
    patron += '<a.*?onclick="javascript.creaVideo\(\'([^\']+)\'.\'[^\']+\'.\'([^\']+)\'.*?'
    patron += '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = urllib.unquote_plus(match[1])
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def getvideo(item):
    logger.info("[lasexta.py] play")

    # Descarga
    data = scrapertools.cachePage(item.url)
    patron = '<PARAM NAME="url" VALUE="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        url = matches[0]
    except:
        url = ""

    patron = 'so.addVariable\("sinopsis", "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        scrapedplot = matches[0]
    except:
        scrapedplot = ""

    # Descarga el .ASX
    data = scrapertools.cachePage(url)
    patron = 'href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    try:
        url = matches[len(matches)-1]
    except:
        url = ""
    
    logger.info("[barcelonatv.py] scrapedplot="+scrapedplot)

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=item.thumbnail , plot=scrapedplot , server = "directo" , folder=False) )

    return itemlist