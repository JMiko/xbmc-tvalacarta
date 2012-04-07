# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para IB3
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[ib3.py] init")

DEBUG = True
CHANNELNAME = "ib3"
MAIN_URL = "http://ib3tv.com/tvalacarta/"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[ib3.py] mainlist")
    return programas(item)

def programas(item):
    logger.info("[rtvc.py] programlist")
    itemlist=[]

    # Descarga la página
    item.url = MAIN_URL
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae los programas
    '''
    <select name="select" class="formulario despl" id="select"><option value=''>Tots els programes</option><option value='a3194b87-719b-4537-a031-9930449f2f1f'>4-4-2</option>...</select>
    '''
    data = scrapertools.get_match(data,'<select name="select" class="formulario despl" id="select">(.*?)</select>')
    logger.info(data)
    
    patron  = "<option value='([^']+)'>([^<]+)</option>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for id,title in matches:
        scrapedtitle = title.strip()
        #http://ib3tv.com/tvalacarta/ajax.php?/0/data?programId=42afe688-1f06-49b3-8408-794270629a45&type=TV&start-index=0&max-results=100&orderby=airdate
        scrapedurl = "http://ib3tv.com/tvalacarta/ajax.php?/0/data?programId="+id+"&type=TV&start-index=0&max-results=100&orderby=airdate"
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, page=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , category = item.category , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[ib3.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae los capítulos
    '''
    <item> <guid isPermaLink="false">8f53b6fb-0331-4d86-a35f-7e07e98c68e1/3320009a-a5ea-42ab-8b25-8c0bfbca148e</guid> <title>Documentals </title> <description></description> <media:keywords> </media:keywords> <media:thumbnail url="http://media.ib3alacarta.com/8f53b6fb-0331-4d86-a35f-7e07e98c68e1/3320009a-a5ea-42ab-8b25-8c0bfbca148e/4802730.jpg" width="100" height="100"/> <copyright>IB3 Televisió de les Illes Balears</copyright> <media:group> <media:content url="http://media.ib3alacarta.com/8f53b6fb-0331-4d86-a35f-7e07e98c68e1/3320009a-a5ea-42ab-8b25-8c0bfbca148e/4802730.mp4" fileSize="465852130" type="video/mp4" medium="video" bitrate="1011" framerate="25" samplingrate="48.0" channels="2" duration="3683" height="360" width="640"> <media:title>Boveret, el bruixot del Trot</media:title> <media:player url="http://ib3alacarta.com/?id=3320009a-a5ea-42ab-8b25-8c0bfbca148e"/> </media:content> </media:group> <media:category scheme="urn:boxee:episode">09</media:category> <media:community> <media:statistics views="474"/> </media:community> <dcterms:issued> 2011-12-27T01:00:00Z</dcterms:issued> <dcterms:valid>start=2011-12-27T01:00:00Z </dcterms:valid> </item>
    '''
    patron  = '<item>\s*'
    patron += '<guid isPermaLink="[^"]+">[^<]+</guid>\s*'
    patron += '<title>([^<]+)</title>\s*'
    patron += '<description>[^<]*</description>\s*'
    patron += '<media:keywords>[^<]*</media:keywords>\s*'
    patron += '<media:thumbnail url="([^"]+)"[^>]+>.*?'
    patron += '<media:content url="([^"]+)"[^>]+>\s*'
    patron += '<media:title>([^>]+)</media:title>.*?'
    patron += '<dcterms:issued>([^>]+)</dcterms:issued>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    # Extrae los items
    for titulo_programa,thumbnail,url,titulo_episodio,fecha in matches:
        scrapedtitle = titulo_episodio
        scrapedurl = url
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , fulltitle = titulo_programa + " - " + titulo_episodio , action="play" , page = scrapedurl, url=scrapedurl, thumbnail=scrapedthumbnail, show=item.show , plot=scrapedplot , folder=False) )

    return itemlist
