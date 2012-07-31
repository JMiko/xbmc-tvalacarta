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
    <div class="keyelement">
    <div class="shadow">
    <a href="javascript:stepcarousel.loadcontent('f-slide', '/wp-content/themes/ib3/carta/update.php?programId=8bd4ff11-1195-47c3-a8ef-a0b810ad4914')"><img src="http://ib3img.s3.amazonaws.com/files_flutter/bs_cuad.jpg"  width="130" height="125" alt="BALEARS SALVATGE" /></a>
    </div>
    <div class="nombres">BALEARS SALVATGE</div>
    </div>
    '''
    '''
    <div class="keyelement">
    <div class="shadow">
    <a href="javascript:stepcarousel.loadcontent('f-slide', '/wp-content/themes/ib3/carta/update.php?programId=2d15fe76-bbed-40c9-95e3-32a800174b7c')"><img src="http://ib3img.s3.amazonaws.com/files_flutter/unaulladacapenrere240x240.jpg"  width="130" height="125" alt="UNA ULLADA CAP ENRERE" /></a>
    </div>
    <div class="nombres">UNA ULLADA CAP ENRERE</div>
    </div>				
    '''
    patron = '<div class="keyelement">[^<]+'
    patron += '<div class="shadow">[^<]+'
    patron += '<a href="javascript:stepcarousel.loadcontent.\'f-slide\'. \'([^\']+)\'."><img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '</div>[^<]+'
    patron += '<div class="nombres">([^<]+)</div>[^<]+'
    patron += '</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle.strip()
        
        #/wp-content/themes/ib3/carta/update.php?programId=2d15fe76-bbed-40c9-95e3-32a800174b7c
        #http://ib3tv.com/wp-content/themes/ib3/carta/update.php?programId=e8f6d4ec-1d7c-4101-839a-36393d0df2a8
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = scrapedthumbnail
        plot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="episodios" , url=url, page=url , thumbnail=thumbnail, plot=plot , show=title , category = "programas" , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[ib3.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae los capítulos
    '''
    <div class="keyelement">
    <div class="keyimage">
    <div class="shadow">
    <a href="javascript:CambiaGraf('7e10a2b1-29a6-4c59-9bc0-77be28888cf6')" ><img src="http://media.ib3alacarta.com/e8f6d4ec-1d7c-4101-839a-36393d0df2a8/7e10a2b1-29a6-4c59-9bc0-77be28888cf6/5120551.jpg" width="190" height="120"/></a>
    </div>
    </div>	
    <div  class="keytext">
    <font color="#c6006f"><strong><b>Au idò!</b></strong></font>
    <br />
    <font color="#000000"></font>
    <br />
    <font size="0.5">02 06 2011 - Capítol: 57</font>
    </div>
    </div>
    '''
    patron = '<div class="keyelement">[^<]+'
    patron += '<div class="keyimage">[^<]+'
    patron += '<div class="shadow">[^<]+'
    patron += '<a href="javascript:CambiaGraf.\'([^\']+)\'." ><img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '</div>[^<]+'
    patron += '</div>[^<]+'
    patron += '<div  class="keytext">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    # Extrae los items
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle).strip()
        title = re.compile("\s+",re.DOTALL).sub(" ",title)
        url = "http://ib3tv.com/wp-content/themes/ib3/carta/titulos.php?type=TV&id="+scrapedurl
        thumbnail = scrapedthumbnail
        plot = ""
        itemlist.append( Item(channel=CHANNELNAME, title=title , fulltitle = item.show + " - " + title , action="play" , page = url, url=url, thumbnail=thumbnail, show=item.show , plot=plot , folder=False) )

    return itemlist

def play(item):
    logger.info("[ib3.py] play")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    mediaurl = scrapertools.get_match(data,"file:'([^']+)',")
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , server="directo" , url=mediaurl, thumbnail=item.thumbnail, show=item.show , folder=False) )
    
    return itemlist