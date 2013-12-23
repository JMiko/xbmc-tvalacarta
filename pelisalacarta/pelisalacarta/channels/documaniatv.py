# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para documaniatv.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "documaniatv"
__category__ = "D"
__type__ = "generic"
__title__ = "DocumaniaTV"
__language__ = "ES"

DEBUG = config.get_setting("debug")

IMAGES_PATH = os.path.join( config.get_runtime_path(), 'resources' , 'images' , 'documaniatv' )

def isGeneric():
    return True

def mainlist(item):
    logger.info("[documaniatv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="novedades"  , title="Novedades"      , url="http://www.documaniatv.com/newvideos.html",thumbnail=os.path.join(IMAGES_PATH, 'nuevos.png')))
    itemlist.append( Item(channel=__channel__, action="categorias" , title="Por categorías" , url="http://www.documaniatv.com",thumbnail=os.path.join(IMAGES_PATH, 'tipo.png')))
    itemlist.append( Item(channel=__channel__, action="tags" , title="Por tags" , url="http://www.documaniatv.com",thumbnail=os.path.join(IMAGES_PATH, 'tipo.png')))
    itemlist.append( Item(channel=__channel__, action="search"     , title="Buscar"         , thumbnail=os.path.join(IMAGES_PATH, 'search_icon.png')))
    return itemlist

def novedades(item):
    logger.info("[documaniatv.py] novedades")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    matches = re.compile('<li[^<]+<div class="pm-li-video"(.*?)</li>',re.DOTALL).findall(data)

    for match in matches:
        try:
            scrapedtitle = scrapertools.get_match(match,'<h3 dir="ltr"><a[^>]+>([^<]+)</a></h3>')
            scrapedurl = scrapertools.get_match(match,'<a href="([^"]+)" class="pm-title-link')
            scrapedthumbnail = scrapertools.get_match(match,'<img src="([^"]+)"')
            scrapedplot = scrapertools.get_match(match,'<p class="pm-video-attr-desc">([^<]+)</p>')
            #scrapedplot = scrapertools.htmlclean(scrapedplot)
            scrapedplot = scrapertools.entityunescape(scrapedplot)
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , fanart=scrapedthumbnail, folder=False) )
        except:
            logger.info("documaniatv.novedades Error al añadir entrada "+match)

    # Busca enlaces de paginas siguientes...
    try:
        next_page_url = scrapertools.get_match(data,'<li class="active"[^<]+<a[^<]+</a[^<]+</li[^<]+<li[^<]+<a href="([^"]+)">')
        next_page_url = urlparse.urljoin(item.url,next_page_url)
        itemlist.append( Item(channel=__channel__, action="novedades", title=">> Pagina siguiente" , url=next_page_url , thumbnail="" , plot="" , folder=True) )
    except:
        logger.info("documaniatv.novedades Siguiente pagina no encontrada")
    
    return itemlist

def categorias(item):
    logger.info("[documaniatv.py] categorias")
    itemlist = []

    # Saca el bloque con las categorias
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,"<ul id='ul_categories'>(.*?)</ul>")

    #
    patron = '<li[^<]+<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__ , action="novedades" , title=match[1],url=match[0]))
    
    return itemlist


def tags(item):
    logger.info("[documaniatv.py] categorias")
    itemlist = []

    # Saca el bloque con las categorias
    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<h4>Palabras Clave</h4>(.*?)</div>')

    #
    patron = '<a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__ , action="novedades" , title=match[1],url=match[0]))
    
    return itemlist



def search(item,texto):
    #http://www.documaniatv.com/search.php?keywords=luna&btn=Buscar
    logger.info("[documaniatv.py] search")
    if item.url=="":
        item.url="http://www.documaniatv.com/search.php?keywords=%s"
    texto = texto.replace(" ","+")
    item.url = item.url % texto
    try:
        return novedades(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def play(item):
    logger.info("documaniatv.play")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    # Busca los enlaces a los videos
    video_itemlist = servertools.find_video_items(data=data)
    for video_item in video_itemlist:
        itemlist.append( Item(channel=__channel__ , action="play" , server=video_item.server, title=item.title+video_item.title,url=video_item.url, thumbnail=video_item.thumbnail, plot=video_item.plot, folder=False))

    # Extrae los enlaces a los videos (Directo)
    patronvideos = "file: '([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        if not "www.youtube" in matches[0]:
            itemlist.append( Item(channel=__channel__ , action="play" , server="Directo", title=item.title+" [directo]",url=matches[0], thumbnail=item.thumbnail, plot=item.plot))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    items = novedades(mainlist_items[0])
    bien = False
    for singleitem in items:
        mirrors = servertools.find_video_items( item=singleitem )
        if len(mirrors)>0:
            bien = True
            break

    return bien