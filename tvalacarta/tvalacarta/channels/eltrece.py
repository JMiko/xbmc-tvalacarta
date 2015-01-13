# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para El Trece (Argentina)
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item

CHANNEL = "eltrece"
MAIN_URL = "http://www.eltrecetv.com.ar/"
DEBUG = (config.get_setting("debug")=="true")

def isGeneric():
    return True

def mainlist(item):
    logger.info("tvalacarta.channels.eltrece mainlist")
    itemlist = []

    data = scrapertools.cachePage("http://www.eltrecetv.com.ar/programas/2015")
    data = scrapertools.find_single_match(data,'<select class="programas">(.*?)</select>')
    patron = '<option.*?value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = "http://www.eltrecetv.com.ar/programas/"+scrapedurl
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNEL, action="programas", title=title , url=url, folder=True) )

    return itemlist

def programas(item):
    logger.info("tvalacarta.channels.eltrece programas")

    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page( item.url )
    patron  = '<(article.*?)</article>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        logger.info("tvalacarta.channels.eltrece programas match="+match)
        title = scrapertools.find_single_match(match,'figure alt="([^"]+)"')
        title = scrapertools.htmlclean(title)

        url = scrapertools.find_single_match(match,'article  about="([^"]+)"')
        url = urlparse.urljoin(item.url,url)

        thumbnail = scrapertools.find_single_match(match,'data-uri="public\:\/\/([^"]+)"')
        thumbnail = "http://eltrecetv.cdncmd.com/sites/default/files/styles/298x168/public/"+thumbnail
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNEL, action="episodios", title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, viewmode="movie", folder=True) )

    # Paginación
    current_page = scrapertools.find_single_match(item.url,"page\=(\d+)")
    if current_page=="":
        next_page_url = item.url+"?page=1"
    else:
        next_page_url = item.url.replace("page="+current_page,"page="+str(int(current_page)+1))
    itemlist.append( Item(channel=CHANNEL, action="programas", title=">> Página siguiente" , url=next_page_url, folder=True) )

    return itemlist

def episodios(item):
    logger.info("tvalacarta.channels.eltrece episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page( item.url )
    item.url = urlparse.urljoin( item.url , scrapertools.find_single_match( data , 'href="(/[^\/]+/capitulos-completos)">Cap' ) )
    
    # Busca la opción de "Capítulos completos"
    data = scrapertools.cache_page( item.url )
    #data = scrapertools.find_single_match(data,'<h1>(.*?)$')
    patron  = '<(figure.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        logger.info("tvalacarta.channels.eltrece programas match="+match)
        title = scrapertools.find_single_match(match,'figure alt="([^"]+)"')
        title = scrapertools.htmlclean(title)

        url = urlparse.urljoin(item.url,scrapertools.find_single_match(match,'a href="([^"]+)"'))

        thumbnail = scrapertools.find_single_match(match,'data-uri="public\:\/\/([^"]+)"')
        thumbnail = "http://eltrecetv.cdncmd.com/sites/default/files/styles/298x168/public/"+thumbnail
        plot = scrapertools.find_single_match(match,'<p>([^<]+)</p>')

        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNEL, action="play" , server="eltrece", title=title , url=url, thumbnail=thumbnail, plot=plot , fanart=thumbnail, viewmode="movie_with_plot", folder=False) )

    # Paginación
    current_page = scrapertools.find_single_match(item.url,"page\=(\d+)")
    logger.info("tvalacarta.channels.eltrece programas current_page="+current_page)
    if current_page=="":
        next_page_url = item.url+"?page=1"
    else:
        next_page_url = item.url.replace("page="+current_page,"page="+str(int(current_page)+1))
    logger.info("tvalacarta.channels.eltrece programas next_page_url="+next_page_url)
    itemlist.append( Item(channel=CHANNEL, action="episodios", title=">> Página siguiente" , url=next_page_url, folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # Busca videos en alguna de las opciones del menu (excepto en programas)
    mainlist_items = mainlist(Item())
    mainlist_item_programas = mainlist_items.pop()

    alguno = False
    for mainlist_item in mainlist_items:
        exec "itemlist="+mainlist_item.action+"(mainlist_item)"
    
        if len(itemlist)>0:
            alguno = True
            break

    if not alguno:
        print "No hay videos en las secciones del menu"
        return False

    # Comprueba que primer programa devuelve episodios
    programas_items = programas(mainlist_item_programas)
    secciones_items = secciones(programas_items[0])
    episodios_items = episodios(secciones_items[0])

    if len(episodios_items)==0:
        return False

    return True
