# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para TVN (Chile)
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "tvn"

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.tvn mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Teleseries" , action="programas" , url="http://www.tvn.cl/player/", extra="teleseries", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Entretención" , action="programas" , url="http://www.tvn.cl/player/", extra="entretencion", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Series" , action="programas" , url="http://www.tvn.cl/player/", extra="series", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Docurrealidad" , action="programas" , url="http://www.tvn.cl/player/", extra="docurrealidad", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Cultura" , action="programas" , url="http://www.tvn.cl/player/", extra="cultura", folder=True) )

    return itemlist

def programas(item):
    logger.info("tvalacarta.channels.tvn programas")
    itemlist = []

    #http://www.tvn.cl/cultura/menuportadaplayer/?service=blank

    # Extrae las series
    data = scrapertools.cachePage("http://www.tvn.cl/"+item.extra+"/menuportadaplayer/?service=blank")
    logger.info("data="+data.strip())

    patron  = '<li><a href="([^"]+)">([^<]+)<'
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
    logger.info("tvalacarta.channels.tvn episodios")
    itemlist=[]

    '''
    <article class="ventana3 efecto-hover">
    <img src="http://www.tvn.cl/incoming/article566557.ece/ALTERNATES/w300/cumbres_170313.jpg" alt="Lhasa la ciudad prohibida"/>
    <a href="/player/play/?id=566567&s=8959">
    <div class="mask">
    <h5><span></span>Cumbres del Mundo</h5>
    <h3>Capítulo 11</h3>
    <h2>Lhasa la ciudad prohibida</h2>
    </div>
    </a>
    </article>
    '''

    # Extrae los episodios
    data = scrapertools.cachePage(item.url)
    patron  = '<article class="ventana3 efecto-hover"[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<div class="mask"[^<]+'
    patron += '<h5><span></span>([^<]+)</h5[^<]+'
    patron += '<h3>([^<]+)</h3[^<]+'
    patron += '<h2>([^<]+)</h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedthumbnail,scrapedurl,scrapedshow,scrapedepisode,scrapedtitle in matches:
        title = scrapedepisode.strip()+" - "+scrapedtitle.strip()
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = ""
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item( channel=item.channel , title=title , action="play" , server="tvn" , url=url , thumbnail=thumbnail , plot=plot , show=title , fanart=thumbnail , folder=False ) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # El canal tiene estructura
    items_mainlist = mainlist(Item())
    items_programas = []

    # Todas las opciones del menu tienen que tener algo
    for item_mainlist in items_mainlist:
        exec "itemlist="+item_mainlist.action+"(item_mainlist)"
    
        if len(itemlist)==0:
            print "La sección '"+item_mainlist.title+"' no devuelve nada"
            return False

        items_programas = itemlist

    # Ahora recorre los programas hasta encontrar vídeos en alguno
    for item_programa in items_programas:
        print "Verificando "+item_programa.title
        items_episodios = episodios(item_programa)

        if len(items_episodios)>0:
            return True

    print "No hay videos en ningún programa"
    return False
