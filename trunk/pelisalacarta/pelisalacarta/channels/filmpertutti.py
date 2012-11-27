# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "filmpertutti"
__category__ = "F"
__type__ = "generic"
__title__ = "filmpertutti"
__language__ = "IT"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[filmpertutti.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novità"     , action="peliculas", url="http://filmpertutti.tv"))
    itemlist.append( Item(channel=__channel__, title="Film per genere" , action="categorias", url="http://filmpertutti.tv|film"))
    itemlist.append( Item(channel=__channel__, title="Serie Tv" , action="categorias", url="http://filmpertutti.tv|serie"))
    itemlist.append( Item(channel=__channel__, title="Anime" , action="categorias", url="http://filmpertutti.tv|anime"))
    itemlist.append( Item(channel=__channel__, title="Cerca Film", action="search"))
    return itemlist
    
def search(item,texto):
    logger.info("[filmpertutti.py] search "+texto)
    itemlist = []
    texto = texto.replace(" ","%20")
    item.url = "http://filmpertutti.tv/?s="+texto+"&x=0&y=0"
    item.extra = ""

    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def categorias(item):
    '''
    <select name="linkIole2" size="1" onchange="location.href=this.value">
    <option value="#">Categorie Film</option>
	<option value="http://filmpertutti.tv/category/animazione/">Animazione</option>
	<option value="http://filmpertutti.tv/category/avventura/">Avventura</option>
	<option value="http://filmpertutti.tv/category/azione/">Azione</option>
	<option value="http://filmpertutti.tv/category/biografico/">Biografico</option>
	<option value="http://filmpertutti.tv/category/comico/">Comico</option>
	</select>
	<td><tr>
	</td></tr>
	<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<tr>
	<select name="linkIole2" size="1" onchange="location.href=this.value">
	<option value="#">Serie Tv</option>
	<option value="http://filmpertutti.tv/category/serie-tv/0-9/">0-9</option>
	<option value="http://filmpertutti.tv/category/serie-tv/a-f/">A-F</option>
	<option value="http://filmpertutti.tv/category/serie-tv/g-l/">G-L</option>
	<option value="http://filmpertutti.tv/category/serie-tv/m-r/">M-R</option>
	<option value="http://filmpertutti.tv/category/serie-tv/s-z/">S-Z</option>
	</select></td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<td><select name="linkIole2" size="1" onchange="location.href=this.value">
	<option value="#">Anime Cartoon</option>
	<option value="http://filmpertutti.tv/category/anime-cartoon-italiani/">Anime Cartoon ITA</option>
	<option value="http://filmpertutti.tv/category/anime-cartoon-sub-ita/">Anime Cartoon Sub-ITA</option>
	</select>
    '''
    url=item.url.split("|")[0]
    cat=item.url.split("|")[1]
    itemlist = []
    data = scrapertools.cache_page(url)
    if cat=="film":
    	data = scrapertools.get_match(data,'<option value="#">Categorie Film</option>(.*?)</select>' )
    else:
    	if cat=="serie":
    		data = scrapertools.get_match(data,'<option value="#">Serie Tv</option>(.*?)</select>' )
    	else:
    		data = scrapertools.get_match(data,'<option value="#">Anime Cartoon</option>(.*?)</select>' )
    patron  = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def peliculas(item):
    logger.info("[filmpertutti.py] peliculas")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <div class="xboxcontent">
    <h2><a href="http://filmpertutti.tv/il-padrino-di-chinatown/" rel="bookmark" title="Il padrino di Chinatown" target=""><img width="192" height="262" src="http://filmpertutti.tv/wp-content/uploads/2012/06/IlpadrinodiChinatown.jpeg" class="attachment-post-thumbnail wp-post-image" alt="IlpadrinodiChinatown" title="IlpadrinodiChinatown">              Il padrino di Chinatown              </a>  </h2> 
    <p>  ...  </p>
    </div>
    '''
    patron  = '<div class="xboxcontent">\s*'
    patron += '<h2><a href="?([^>"]+)"?.*?title="?([^>"]+)"?.*?<img.*?src="([^>"]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedtitle=scrapertools.decodeHtmlentities(scrapedtitle.replace("Streaming",""))
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Extrae el paginador
    patronvideos  = '<div class=\'Navi\'>.*?<a href="([^"]+)" ><strong>&raquo;</strong></a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="Next Page >>" , url=scrapedurl , folder=True) )

    return itemlist

# Verificaci�n autom�tica de canales: Esta funci�n debe devolver "True" si est� ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los v�deos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien