# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Telefe
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse
import urllib
import re
import traceback

from core import logger
from core import scrapertools
from core import jsontools
from core.item import Item

DEBUG = True
CHANNELNAME = "telefe"
MAIN_URL = "http://telefe.com/capitulos-completos/"

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.telefe mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Últimos episodios añadidos" , action="videos" , thumbnail = "" , url = MAIN_URL))
    itemlist.extend(programas(item))

    return itemlist

def programas(item):
    logger.info("tvalacarta.telefe programas")
    
    itemlist = []

    '''
    <select id="programSearchCombo" style="display:none">
    <option id="0">Todos los programas</option>
    <option id="3133" value="3133">AM</option>
    <option id="6598" value="6598">Casados con hijos</option>
    '''

    data = scrapertools.cache_page(MAIN_URL)
    data = scrapertools.find_single_match(data,'<select id="programSearchCombo"[^<]+<optio[^>]+>Todos los programas</option>(.*?)</select>')

    patron  = '<option id="\d+" value="(\d+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        title = scrapertools.htmlclean(scrapedtitle)
        url = "http://telefe.com/capitulos-completos/?s=&layout=list&programa="+scrapedurl
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="videos" , url=url, thumbnail=thumbnail, plot=plot , show=scrapedtitle, folder=True) )

    itemlist = sorted(itemlist, key=lambda Item: Item.title)

    return itemlist

def videos(item):
    logger.info("tvalacarta.telefe videos")

    '''
    {"IdPost":0,
        "ImageURL":"/media/64285/taxxi.jpg",
        "Title":"Capítulo 40: Sorpresa e impacto",
        "Link":"http://telefe.com/taxxi/capitulo-40-sorpresa-e-impacto/",
        "Content":null,
        "VideoUrl":null,
        "VideoId":0,
        "VideoTags":null,
        "ColorMicrositio":"FF9E4A",
        "NombreMicrositio":"Taxxi","Copete":"Reviví un nuevo capítulo de Taxxi. Intrigas, celos y misterio. ","FechaDeEmision":"Emitido el 20 de diciembre de 2013"}
    '''
    
    itemlist=[]
    data = scrapertools.cache_page(item.url)
    bloque = scrapertools.find_single_match(data,'viewBagBusquedaVideos \= (.*?)\s+refreshMenuVideos')
    #logger.info("tvalacarta.telefe data="+data)

    patron  = '\{([^\}]+)\}'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    if DEBUG: scrapertools.printMatches(matches)

    for entry in matches:
        show = scrapertools.find_single_match(entry,'"NombreMicrositio"\:"([^"]+)"')
        title = show + ": " + scrapertools.find_single_match(entry,'"Title"\:"([^"]+)"')
        url = scrapertools.find_single_match(entry,'"Link"\:"([^"]+)"')
        thumbnail = urlparse.urljoin( item.url , scrapertools.find_single_match(entry,'"ImageURL":"([^"]+)"') )
        plot = scrapertools.find_single_match(entry,'"Copete"\:"([^"]+)"')

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , server="telefe", url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot , show=show, folder=False) )

    try:
        current_page = scrapertools.find_single_match(data,'<input type="hidden" id="pageNumber" value="(\d+)">')
        next_page = str(int(current_page)+1)
        if "page=" in item.url:
            next_page_url = re.compile("page=\d+",re.DOTALL).sub("page="+next_page,item.url)
        else:
            if "?" in item.url:
                next_page_url = item.url+"&page="+next_page
            else:
                next_page_url = item.url+"?page="+next_page
        itemlist.append( Item(channel=CHANNELNAME, title=">> Página siguiente" , action="videos" , url=next_page_url , folder=True ) )
    except:
        logger.info(traceback.format_exc())

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # El canal tiene estructura programas -> episodios -> play
    items_programas = programas(Item())
    if len(items_programas)==0:
        print "No hay programas"
        return False

    # Ahora recorre los programas hasta encontrar vídeos en alguno
    for item_programa in items_programas:
        print "Verificando "+item_programa.title
        items_videos = videos(item_programa)
        if len(items_videos)>0:
            return True

    print "No hay videos en ningún programa"
    return False
