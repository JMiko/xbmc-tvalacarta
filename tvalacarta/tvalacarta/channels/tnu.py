# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para TNU (Uruguay)
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "tnu"

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.tnu mainlist")

    item = Item(channel=CHANNELNAME, url="http://www.tnu.com.uy/videos")
    return programas(item)

def programas(item):
    logger.info("tvalacarta.channels.tnu programas")
    itemlist = []

    '''
    <li class=" prog_li" id="3289">
    <a href="/videos?prog=3289&v=1" class="program_menu_3289">Artes Escénicas</a>
    </li>
    '''

    # Extrae las series
    data = scrapertools.cachePage(item.url)
    patron  = '<li class=" prog_li" id="\d+"[^<]+'
    patron += '<a href="([^"]+)" class="program_menu_\d+">([^<]+)</'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        thumbnail = ""
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item( channel=item.channel , title=title , action="episodios" , url=url , thumbnail=thumbnail , plot=plot , show=title , fanart=thumbnail , folder=True ) )

    return itemlist

def episodios(item):
    logger.info("tvalacarta.channels.tnu episodios")
    itemlist=[]

    '''
    <div class='vid_mod'>
    <a href='http://www.tnu.com.uy/videos/programa-7-jorge-burgos-cerro-largo'>
    <div class='thumb-video-full'>
    <img src='http://i.ytimg.com/vi/nY9MiTM02K4/0.jpg' />
    </div>
    </a>
    <ul>
    <li class='video-title-prog' >
    Programa 7: Jorge Burgos, Cerro Largo                           </li> 
    <li class='video-subtitle-prog'>
    Cuerdas y vientos                           </li> 
    <li class="video-btn-reproducir">
    <a href='http://www.tnu.com.uy/videos/programa-7-jorge-burgos-cerro-largo' class='reprod'>Reproducir</a>
    </li>
    </ul>
    </div>
    '''

    # Extrae los episodios
    data = scrapertools.cachePage(item.url)
    patron  = "<div class='vid_mod'[^<]+"
    patron += "<a href='([^']+)'[^<]+"
    patron += "<div class='thumb-video-full'>[^<]+"
    patron += "<img src='([^']+)' />[^<]+"
    patron += "</div>[^<]+"
    patron += "</a>[^<]+"
    patron += "<ul>[^<]+"
    patron += "<li class='video-title-prog'\s*>([^<]+)</li"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        title = scrapedtitle.strip()
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        #http://i.ytimg.com/vi/nY9MiTM02K4/0.jpg
        youtube_code = scrapertools.get_match(thumbnail,"http://i.ytimg.com/vi/([^\/]+)/0.jpg")
        url = "http://www.youtube.com/watch?v="+youtube_code
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item( channel=item.channel , title=title , action="play" , server="youtube" , url=url , thumbnail=thumbnail , plot=plot , show=title , fanart=thumbnail , folder=False ) )

    try:
        next_page = scrapertools.get_match(data,"<span class='page-numbers current'>\d+</span[^<]+<a class='page-numbers' href='([^']+)'")
        #/videos?prog=3798&#038;v=1&#038;pag=2
        itemlist.append( Item( channel=item.channel , title=">> Página siguiente" , action="episodios" , url=urlparse.urljoin(item.url,next_page.replace("&#038;","&")) ) )
    except:
        pass

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # El canal tiene estructura
    items_mainlist = mainlist(Item())
    if len(items_mainlist)==0:
        print "No hay programas"
        return False

    # Ahora recorre los programas hasta encontrar vídeos en alguno
    for item_programa in items_mainlist:
        print "Verificando "+item_programa.title
        items_episodios = episodios(item_programa)

        if len(items_episodios)>0:
            return True

    print "No hay videos en ningún programa"
    return False
