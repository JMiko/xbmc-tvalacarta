# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Giralda TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = True
CHANNELNAME = "giraldatv"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[giraldatv.py] mainlist")
    item = Item(url="http://www.giraldatv.es/alacarta.html")
    return programas(item)

def programas(item):
    logger.info("[giraldatv.py] programas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #print data

    # Extrae los programas
    '''
    <td><a onclick="_gaq.push(['_trackEvent', 'Cabecera', 'A la carta', 'En el corazon sevilla']);" href="http://www.giraldatv.es/enelcorazonsevilla/" target="_top"><img src="http://www.giraldatv.es/img/logoenelcorazonsevilla.png" border=0 alt="En el corazon sevilla" title="En el corazon sevilla"></a></td></tr>
    <td align="center"><a onclick="_gaq.push(['_trackEvent', 'Cabecera', 'A la carta', 'Sevilla siglo XXI']);" href="http://www.giraldatv.es/sevillasigloxxi/" target="_top"><img src="http://www.giraldatv.es/img/logosevillasigloxxi.png" border=0 alt="Sevilla siglo XXI" title="Sevilla siglo XXI"></a></td>
    '''
    patron  = "<td.*?<a onclick=\"_gaq.push\(\['_trackEvent', 'Cabecera', 'A la carta', '([^']+)'\]\)\;\""
    patron += ' href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[0]
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""

        scrapedpage = scrapedurl
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] plot=["+scrapedplot+"]")
        #logger.info(scrapedplot)

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , page=scrapedpage, show=scrapedtitle , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[giraldatv.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae los capítulos
    '''
    contentArray[8] = new Content(371,6220,7149,8, 'En el corazón... Sevilla 1x13 (2/2)', 'En el corazón... Sevilla 1x13 (2/2)', 'Hoy hablamos de Antonia Colomé', 'http://files.velocix.com/c653/giralda_tv/gt101214_corazon_sevilla_01x13_antonia_colome_b_gitv_16x9_1800.mov', 'true', 'http://www.vidzapper.net/live/assets/images/metacontent/741F3B3E-2031-48A5-BF70-22F54DEB7299.JPEG', '1667', '0', '0', 'true', 'en el corazon,sevilla,antonia colome', 'http://files.velocix.com/c653/giralda_tv/gt101214_corazon_sevilla_01x13_antonia_colome_b_gitv_16x9_1800.mov', 'http://www.vidzapper.net/live/assets/images/metacontent/741F3B3E-2031-48A5-BF70-22F54DEB7299_thumb.JPEG',1, 'Content', 'Content', 'false', 'http://www.giraldatv.es/enelcorazonsevilla', 'true', 'false', 'nonadult', 'None', '00:00:00:000', '00:00:00:000', 'plain', 'true', 'false', '', 'false', 'false'
    '''
    patron = "new Content\(.*?'([^']+)', '([^']+)', '([^']+)', '([^']+)', '([^']+)', '([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    # Extrae los items
    for match in matches:
        scrapedtitle = match[0]
        scrapedurl = match[3]
        scrapedthumbnail = match[5]
        scrapedplot = match[2]
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="Directo", page=item.page, url=scrapedurl, thumbnail=scrapedthumbnail, show=item.show , plot=scrapedplot , folder=False) )

    return itemlist
