# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools
import urllib

__channel__ = "submityourtapes"
__category__ = "F"
__type__ = "generic"
__title__ = "submityourtapes"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[submityourtapes.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Útimos videos" , url="http://www.submityourtapes.com/"))
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Más vistos" , url="http://www.submityourtapes.com/most-viewed/1.html"))
    itemlist.append( Item(channel=__channel__, action="videos"    , title="Más votados" , url="http://www.submityourtapes.com/top-rated/1.html"))
    itemlist.append( Item(channel=__channel__, action="search"    , title="Buscar", url="http://www.submityourtapes.com/index.php?mode=search&q=%s&submit=Search"))
    
    return itemlist

# REALMENTE PASA LA DIRECCION DE BUSQUEDA

def search(item,texto):
    logger.info("[submityourtapes.py] search")
    tecleado = texto.replace( " ", "+" )
    item.url = item.url % tecleado
    return videos(item)

# SECCION ENCARGADA DE BUSCAR

def videos(item):
    logger.info("[submityourtapes.py] videos")
    data = scrapertools.downloadpageGzip(item.url)

    itemlist = [] 
    matches = re.compile(r"""<div class='content_item' style="width: 242px;">.*?<br style='clear: both'>.*?</div>.*?</div>""",re.DOTALL).findall(data)
    for match in matches:
        
        info = re.compile(r"""<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)" alt="([^"]+)" name="([^"]+)" border="1" id='([^"]+)' width="240" height="180""""", re.S).findall(match)
        if len(info) == 1:
            video = info[0]
            
        time = re.compile(r"""<span style='([^']+)'>([^']+)</span>""", re.S).findall(match)
        posted = re.compile(r"""<div style='float:right'>Posted: ([^']+)<br /></div>""", re.S).findall(match)
        
        try:
            scrapedtitle = unicode( video[1], "utf-8" ).encode("iso-8859-1")
        except:
            scrapedtitle = video[1]

        if len(time) > 0:
            scrapedtitle = scrapedtitle + "("+time[0][1]+")"
            
        if len(posted) > 0:
            scrapedtitle = scrapedtitle + "["+posted[0]+"]"
        
        scrapedurl =  urlparse.urljoin( "http://www.submityourtapes.com/", video[0] )
        scrapedthumbnail = urlparse.urljoin( "http://www.submityourtapes.com/", video[2] )
        scrapedplot = ""
        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=__channel__, action="video" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    #Paginador
    print "paginador"
    matches = re.compile('<a href="([^"]+)">Next</a>', re.DOTALL).findall(data)
    if len(matches)>0:
        scrapedurl =  urlparse.urljoin( "http://www.submityourtapes.com/", matches[0] )
        print scrapedurl
        paginador = Item(channel=__channel__, action="videos" , title="!Página siguiente" , url=scrapedurl, thumbnail="", plot="", extra = "" , show=item.show)
    else:
        paginador = None
    
    if paginador is not None:
        itemlist.append( paginador )

    return itemlist

# SECCION ENCARGADA DE VOLCAR EL LISTADO DE CATEGORIAS CON EL LINK CORRESPONDIENTE A CADA PAGINA
    
def listcategorias(item):
    logger.info("[submityourtapes.py] listcategorias")
    itemlist = []
    return itemlist
    

# OBTIENE LOS ENLACES SEGUN LOS PATRONES DEL VIDEO Y LOS UNE CON EL SERVIDOR
def video(item):
    logger.info("[submityourtapes.py] play")
    # <div id="movies" style="width: 100%; ">
    data = scrapertools.downloadpage(item.url)
    
    itemlist = []
    matches = re.compile('so.addVariable\("file", "([^"]+)"\);', re.DOTALL).findall(data)
    if len(matches)>0:
        parsed_url = urllib.unquote_plus(matches[0])
        print parsed_url
        paginador = Item(channel=__channel__, action="play" , title=item.title, fulltitle=item.fulltitle , url=parsed_url, thumbnail=item.thumbnail, plot=item.plot, show=item.title, server="directo", folder=False)
    else:
        paginador = None
    
    if paginador is not None:
        itemlist.append( paginador )

    return itemlist

