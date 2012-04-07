# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Canal para la sexta
#------------------------------------------------------------
import urlparse,re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[sexta.py] init")

DEBUG = True
CHANNELNAME = "lasexta"
MAIN_URL = "http://www.lasexta.com/lg/programas"
def isGeneric():
    return True

def mainlist(item):
    logger.info("[sexta.py] mainlist")

    # Descarga la pagina
    item.url = MAIN_URL
    return programas(item)

def programas(item):
    logger.info("[sexta.py] programas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Extrae las series
    patron  = '<div class="item">[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<!-- <[^<]+'
    patron += '<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="episodios" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=scrapedthumbnail , show = scrapedtitle, folder=True) )
    
    return itemlist

def episodios(item):
    logger.info("[sexta.py] episodios")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #logger.info(data)
    
    '''
    <div class="item">
    <a href="/lg/programa_detalle/598163" title="¿Quién vive ahí? Una casa de fantasía es como vivir dentro de un cuento" id="item1" style="nav-index:1;nav-right:#item2;nav-left:#item0;" class="item_img_link nav_item">
    <!-- <img class="media" src="media/img/1pxtrans.gif" width="293" height="165" alt="nombre de la fotografia" style="background:#0000C8"/> -->
    <img class="media" src="http://www.sitios.lasexta.com/pictures/6673/396673/Sitios2010_20120331_1958598043_crop75.jpg" width="293" height="165" alt="¿Quién Vive Ahí?" style="background:#0000C8"/>
    
    <label class="item_data">
    <b class="titulo" title="02-04-2012 ¿Quién vive ahí? Una casa de fantasía es como vivir dentro de un cuento">02-04-2012 ¿Quién vive ahí? Una casa de fantasía es como vivir dentro&#8230;</b>
    </label>
    </a>
    </div>
    '''

    # Extrae las series
    patron  = '<div class="item">[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<!-- <[^<]+'
    patron += '<img class="media" src="([^"]+)"[^<]+'
    patron += '<label class="item_data">[^<]+'
    patron += '<b class="titulo" title="([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    for scrapedurl,showtitle,scrapedthumbnail,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="partes" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=scrapedthumbnail , show = scrapedtitle, folder=True) )
    

    '''
    <div class="item">
    <a href="/lg/programa_detalle/588133" title="Una casa de cine y la casa de la propia Barbie" id="item_s1" style="nav-index:1;nav-right:#item_s2;nav-left:#item_s0;" class="item_img_link nav_item_s">
    <!-- <img src="media/img/1pxtrans.gif" width="186" height="105" alt="nombre de la fotografia" style="background:#000000" class="media" /> -->
    <img src="http://www.sitios.lasexta.com/pictures/8713/388713/pictures_20120305_0958388713_crop75sub1.jpg" width="186" height="105" alt="¿Quién Vive Ahí?" style="background:#000000" class="media" />					<label class="item_data">
    <b class="titulo" title="Una casa de cine y la casa de la propia Barbie" title-short="">Una casa de cine y la casa de la propia Barbie</b>
    </label>
    </a>
    </div>
    '''

    # Extrae las series
    patron  = '<div class="item">[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<!-- <[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '<label class="item_data">[^<]+'
    patron += '<b class="titulo" title="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    for scrapedurl,showtitle,scrapedthumbnail,title in matches:
        scrapedtitle = title
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="partes" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=scrapedthumbnail , show = scrapedtitle, folder=True) )

    return itemlist

def partes(item):
    logger.info("[sexta.py] partes")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    logger.info(data)
    
    # var video1 = new PlaylistItem(options = {url: 'http://videos.lasexta.com/quienviveahi/hd/PPD0001293004401_--QUI-_N_VIVE_AH-___-_QUI-_N_VIVE_AH-__18_03_2012_23_40_56_h264.mp4'});
    patron = "url\:\s+'(http\://[a-z]+.lasexta.com/[^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    logger.info("matches="+str(matches))
    i=1
    for url in matches:
        scrapedtitle = "("+str(i)+") "+item.title
        scrapedurl = url
        scrapedthumbnail = item.thumbnail
        scrapedplot = item.plot
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail , show = scrapedtitle, folder=False) )
        i=i+1

    return itemlist
