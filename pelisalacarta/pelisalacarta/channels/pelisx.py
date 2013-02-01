# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para PelisX (por ZeDinis)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pelisx"
__category__ = "F"
__type__ = "generic"
__title__ = "PelisX"
__language__ = "ES"

# Traza el inicio del canal
logger.info("[pelisx.py] init")

DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pelisx.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Ver Todas" , url="http://www.pelisx.net/ver-todos/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias"      , title="Categorias" , url="http://www.pelisx.net/ver-todos/"))
    itemlist.append( Item(channel=__channel__, action="listactrices"    , title="Actrices y Tags", url="http://www.pelisx.net/actrices-porno/"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar...", url=""))
    return itemlist

def listcategorias(item):
    logger.info("[pelisx.py] listcategorias")
    itemlist=[]

    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Amateur" , url="http://www.pelisx.net/amateur/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Anal" , url="http://www.pelisx.net/anal/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Asiaticas" , url="http://www.pelisx.net/asiaticas/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Grupos" , url="http://www.pelisx.net/grupos/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Hentai" , url="http://www.pelisx.net/hentai/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Interracial" , url="http://www.pelisx.net/interracial/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Jovencitas" , url="http://www.pelisx.net/jovencitas-peliculas-online/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Lesbianas" , url="http://www.pelisx.net/lesbianas/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Maduritas" , url="http://www.pelisx.net/maduritas/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Oral" , url="http://www.pelisx.net/oral-peliculas-online/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Pornstars" , url="http://www.pelisx.net/pornstars/"))
    itemlist.append( Item(channel=__channel__, action="listapelis"      , title="Tetonas" , url="http://www.pelisx.net/tetonas/"))    

    return itemlist
        
def listactrices(item):
    logger.info("[pelisx.py] listactrices")
    
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    logger.info(data)
    
    # Extrae las entradas (carpetas)
    patronvideos = "<a href='(.+?)'[^<]+>(.+?)</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    scrapertools.printMatches(matches)
    
    for match in matches:

        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item ( channel=__channel__ , action="listapelis" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist

def search(item,texto):
    logger.info("[pelisx.py] search")
    itemlist = []

    texto = texto.replace(" ","+")
    item.url="http://www.pelisx.net/?s=" + texto    
    itemlist.extend(listapelis(item))
    
    return itemlist

def listapelis(item):
    logger.info("[pelisx.py] listapelis")

    itemlist=[]
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    logger.info(data)

    # Extrae las entradas 
    patronvideos  = '<img src="http://www.pelisx.net/wp-content/themes/twenten/thumb.php.*?http://(.+?)&amp.*?<h2><a href="(.+?)">(.+?)</a></h2>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedurl = urlparse.urljoin(item.url,match[1])     
        scrapedtitle = match[2]
        scrapedthumbnail = "http://" + match[0]
        scrapedplot = ""
        
        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle.strip(), url=scrapedurl, thumbnail=scrapedthumbnail))
        

    # Extrae la marca de siguiente página
    
    patronvideos  = '<a href="([^"]+)" class="nextpostslink">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedtitle = "Siguiente página >>"
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        itemlist.append( Item(channel=__channel__, action="listapelis" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail))
        
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())

    return bien
