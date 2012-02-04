# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesyonkis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por Truenon y Jesus, modificada por Boludiko
# v11
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core import aes          
from core.item import Item
from servers import servertools

__channel__ = "mitele"
__category__ = "S,F,A"
__type__ = "generic"
__title__ = "Mi tele"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesyonkis.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series"    , action="series"    , thumbnail = "" , url="http://www.mitele.es/series-online/"))
    itemlist.append( Item(channel=__channel__, title="Programas" , action="series" , thumbnail = "" , url="http://www.mitele.es/programas-tv/"))
    itemlist.append( Item(channel=__channel__, title="TV Movies"   , action="series" , thumbnail = "" , url="http://www.mitele.es/tv-movies/"))
    itemlist.append( Item(channel=__channel__, title="TV Infantil"   , action="series" , thumbnail = "" , url="http://www.mitele.es/tv-infantil/"))
    #itemlist.append( Item(channel=__channel__, title="Directo"   , action="directo" , thumbnail = "" , url="http://www.mitele.es/directo/"))
    return itemlist

def series(item):
    logger.info("[mitele.py] series")
    itemlist = []
    data = scrapertools.cachePage(item.url)
        
    # Extrae los programas
    patron  = '<div class="programList">(.*?)</div>'
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        subdata = matches[0]
    else:
        return itemlist
    
    patron  = '<li.*?</li>'
    matches = re.findall(patron,subdata,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)
    
    if len(matches)>0:
        for subdata in matches:
            patron  = 'href="([^"]+)".*?title="([^"]+)".*?src="([^"]+)"'
            matches2 = re.findall(patron,subdata,re.DOTALL)
            for match in matches2:
                scrapedurl = "http://www.mitele.es" + match[0]
                scrapedtitle = match[1]
                scrapedthumbnail = match[2]
                scrapedplot = ""
                itemlist.append( Item(channel=__channel__, action="temporadas" , title=scrapedtitle,  fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))
    else:
        return []
    return itemlist

def temporadas(item):
    logger.info("[mitele.py] Temporadas")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = 'temporadas:.*?[(.*?)]'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '{"ID":"(.*?)","post_title":"(.*?)","post_name":".*?"}'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = "http://www.mitele.es/temporadasbrowser/getCapitulos/"+match2[0]+"/"
            scrapedtitle =match2[1]
            scrapedthumbnail = ""
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="capitulos"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    return itemlist

def capitulos(item):
    logger.info("[mitele.py] Capitulos")

    url = item.url
                
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = '{(.*?)}'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '"ID":"(.*?)".*?'
        patron  += '"post_title":"(.*?)","post_subtitle":"(.*?)".*?'
        patron  += '"post_content":"(.*?)".*?'
        patron  += '"image":"(.*?)".*?'
        patron  += '"url":"(.*?)".*?'
        
        matches2 = re.compile(patron,re.DOTALL).findall(data2)
        logger.info("hay %d matches2" % len(matches2))

        for match2 in matches2:
        # Atributos
            scrapedurl = "http://www.mitele.es"+match2[5].replace("\\","")
            scrapedtitle = match2[1] +": "+ match2[2]
            scrapedthumbnail = match2[4].replace("\\","")
            scrapedplot = match2[3]
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            # A�ade al listado de XBMC
            itemlist.append( Item(channel=item.channel , action="capitulo"   , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot ))
    
    return itemlist

def capitulo(item):
    logger.info("[mitele.py] Capitulo")

    url = item.url
    data = scrapertools.cachePage(url)

    # Extrae las entradas (carpetas)
   
    patron = 'var flashvars = {(.*?)}'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("hay %d matches" % len(matches))
    

    itemlist = []
    for match in matches:
        data2 = match
        patron  = '"host":"(.*?)".*?'
        matches2 = re.compile(patron,re.DOTALL).findall(data2)

        for match2 in matches2:
        # Atributos
            xml = match2.replace("\\","")
            logger.info("XML = "+xml)
           
    # Extraemos datos xml
    
    data = scrapertools.cachePage(xml)
    patron = '<link start="(.*?)" end="(.*?)">(.*?)</link>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    id="XX"
    startTime = "0"
    endTime = "0"
    for match in matches:
        startTime = match[0]
        endTime = match[1]
        id = match[2]
        logger.info("Datos xml = "+startTime+";"+endTime+";"+id)
        
    #Datos clock.php
    
    data = scrapertools.cachePage("http://www.mitele.es/media/clock.php")
    serverTime = data.strip();
    logger.info("Server Time ="+serverTime)
    
    data = serverTime+";"+id+";"+startTime+";"+endTime
    logger.info("Data = "+data)
    
    try:
        AES = aes.AES()                   
        ciphertext = AES.encrypt(data,'xo85kT+QHz3fRMcHNXp9cA',256)      
                
        #metodo 1
        url = 'http://servicios.mitele.es/tokenizer/tk2.php'
        values = {'force_http' : '1',
          'sec' : ciphertext,
          'id' : id}

        search_data = urllib.urlencode(values,doseq=True)
        request = urllib2.Request(url,search_data)
        request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
        response = urllib2.urlopen(request)
        data = response.read()
        response.close()
        itemlist.append( Item(channel=__channel__, action="play" , title="play", url=data, thumbnail=item.thumbnail, plot="", server="directo", extra="", category=item.category, fanart=item.thumbnail, folder=False))
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)

    return itemlist

def directo (item):
    logger.info("[mitele.py] directo")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    
    # Extrae los programas
    patron  = '<ul id="canales">(.*?)</ul>'
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        subdata = matches[0]
    else:
        return itemlist
    
    patron  = '<li.*?</li>'
    matches = re.findall(patron,subdata,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)
    
    if len(matches)>0:
        for subdata in matches:
            patron  = 'href="([^"]+)".*?src="([^"]+)"'
            matches2 = re.findall(patron,subdata,re.DOTALL)
            for match in matches2:
                scrapedurl = "http://www.mitele.es" + match[0]
                #/directo/cuatro/
                patron  = '/directo/([^/]+)/'
                matches2 = re.findall(patron,match[0],re.DOTALL)
                if DEBUG: scrapertools.printMatches(matches2)
                scrapedtitle = ""
                if len(matches2)>0:
                    scrapedtitle = matches2[0]
                scrapedthumbnail = match[1]
                scrapedplot = ""
                itemlist.append( Item(channel=__channel__, action="" , title=scrapedtitle,  fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))
    else:
        return []
    return itemlist

    










