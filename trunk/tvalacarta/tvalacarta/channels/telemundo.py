# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para http://conectate.gov.ar
# creado por rsantaella
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "telemundo"
__category__ = "L"
__type__ = "generic"
__title__ = "telemundo"
__language__ = "ES"
__creationdate__ = "20130322"
__vfanart__ = "http://msnlatino.telemundo.com/_images/telemundo_bg_tile.jpg"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[telemundo.py] mainlist")    
    itemlist = []

    item.url="http://msnlatino.telemundo.com/videos/allprograms/"
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
    data = " ".join(data.split())
    #logger.info(data)
    '''
    <div class="thumb"> <a href="/videos/12_corazones/" class="img156x89"> <img src="/_cdncache/images/fotos/2011-06/12corazones/jpg/sizes/156/89/TC/100/C/12corazones.jpg" alt="" /></a> </div> <div class="video-description"> <h3> <a href="/videos/12_corazones/">12 Corazones</a> </h3> <p></p> </div>
    '''
    patron  = '<div class="thumb"> <a href=".*?" class="img156x89"> <img src="(.*?)" alt="" /></a> </div> <div class="video-description"> <h3> <a href="(.*?)">(.*?)</a> </h3> <p></p> </div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedthumbnail,scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        thumbnail = urlparse.urljoin("http://msnlatino.telemundo.com",scrapedthumbnail)
        url = scrapedurl
        #plot = scrapedplot.strip()
        itemlist.append( Item(channel=__channel__, action="videos", title=title, url=url, thumbnail=thumbnail,  folder=True))

    return itemlist

def videos(item):
    logger.info("[telemundo.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage("http://msnlatino.telemundo.com/module/video_extras_content" + item.url)
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
    data = " ".join(data.split())
    logger.info(data)
    '''
    <div class="thumb"> <a href="/videos/12_corazones/especial_de_dia_de_vacaciones_15_032113/487c3def-6a00-42bc-83d2-84d05ac81d80" class="img156x90"> <img src="http://img2.catalog.video.msn.com/image.aspx?uuid=487c3def-6a00-42bc-83d2-84d05ac81d80&w=160&h=90&so=4" alt="" /></a> </div> <div class="tooltip"> <div class="c_tip"> <div class="arrow_tip"></div> <h3><a href="/videos/12_corazones/especial_de_dia_de_vacaciones_15_032113/487c3def-6a00-42bc-83d2-84d05ac81d80">12 Corazones</a></h3> <p><span class='tp_black'>Especial de dia de Vacaciones (1/5) (03-21-13)</span></p> <p><span class='tp_grey'>Descripción:</span> <br> Diviértete con las declaraciones de amor de nuestros participantes.</p> <p><span class='tp_grey'>Duraci&#243;n:</span> <span class='tp_black'>9:22</span></p> <p><span class='tp_grey'>Vistas:</span> <span class='tp_black'>115</span></p> </div> <div class="b_tip"> </div> </div> <div class="video-description"> <h3><a href="/videos/12_corazones/especial_de_dia_de_vacaciones_15_032113/487c3def-6a00-42bc-83d2-84d05ac81d80">12 Corazones</a></h3> <p>Especial de dia de...</p> </div> </div>
    '''
    patron  = '<div class="thumb"> <a href="(.*?)" class="img156x90"> <img src="(.*?)" alt="" /></a> </div> <div class="tooltip">.*?<span class=\'tp_black\'>(.*?)</span></p> <p><span class=\'tp_grey\'>Descripción:</span> <br>(.*?)</p>.*?</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedthumbnail,scrapedtitle,scrapeddescription in matches:
        title = scrapertools.htmlclean(scrapedtitle) + " - " + scrapertools.htmlclean(scrapeddescription)
        thumbnail = urlparse.urljoin("http://msnlatino.telemundo.com",scrapedthumbnail)
        #url = urlparse.urljoin("http://msnlatino.telemundo.com",scrapedurl)
        url = scrapedurl[-36:]
        itemlist.append( Item(channel=__channel__, action="play", title=title, url=url, thumbnail=thumbnail,  folder=False))

    patron = '<a href="([^"]+)" class="next"></a>'  
    matches = re.compile(patron,re.DOTALL).findall(data)
    if matches:
        itemlist.append( Item(channel=__channel__, action="videos", title="!Página Siguiente", url=matches[0], thumbnail="",  folder=True))             	
    return itemlist

def play(item):
    logger.info("[telemundo.py] play")    
    data = scrapertools.cachePage("http://hub.video.msn.com/services/videodata/?ids=" + item.url + "&detailed=true&v=2")
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
    data = " ".join(data.split())
    logger.info(data)
    itemlist = []
    
    #<file><formatCode>1002</formatCode><url>http://content4.catalog.video.msn.com/e2/ds/9436b1e2-199a-493f-a96b-3b17c80525c0.mp4</url></file>
    patron = '<file><formatCode>.*?</formatCode><url>(.*?)</url></file>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for match in matches:
        scrapedurl = match
        itemlist.append( Item(channel=__channel__, action="play",  server="directo",  title=item.title, url=scrapedurl, folder=False))


    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():

    # Todas las opciones tienen que tener algo
    series_items = mainlist(Item())

    # Lista de series
    if len(series_items)==0:
        print "No hay series"
        return False

    videos_items = videos(series_items[0])
    if len(videos_items)==0:
        print "La serie "+series_items[0].title+" no tiene episodios"
        return False

    mediaurl_items = play(videos_items[0])
    if len(mediaurl_items)==0:
        print "Error al averiguar la URL del primer episodio de "+series_items[0].title
        return False

    return True
