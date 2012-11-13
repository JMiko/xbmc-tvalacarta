# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para yaske
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "yaske"
__category__ = "F"
__type__ = "generic"
__title__ = "Yaske.net"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[yaske.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Portada"            , action="peliculas", url="http://www.yaske.net/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Categorías"         , action="categorias", url="http://www.yaske.net/es/peliculas/"))
    itemlist.append( Item(channel=__channel__, title="Últimas agregadas"  , action="peliculas", url="http://www.yaske.net/es/peliculas/ultimas"))
    itemlist.append( Item(channel=__channel__, title="Buscar"             , action="search") )

    return itemlist
	
def search(item,texto):

    logger.info("[yaske.py] search")
    itemlist = []

    try:
        item.url = "http://www.yaske.net/es/peliculas/search/%s"
        item.url = item.url % texto
        item.extra = ""
        itemlist.extend(peliculas(item))
        itemlist = sorted(itemlist, key=lambda Item: Item.title) 
        
        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("[yaske.py] listado")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)

    # Extrae las entradas
    patron  = '<div class="itemdos c\d+" id="numitem\d+"><div class="img_box"><a href="([^"]+)" rel="([^"]+)">[^<]+'
    patron += '<img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '<div class="quality">([^<]+)</div><div[^<]+<span[^<]+</span></div></div>[^<]+'
    patron += '<div[^<]+<div[^<]+</div><div[^<]+<a[^<]+</a></div><div[^<]+</div>[^<]+'
    patron += '<div class="idiomes">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for scrapedurl,scrapedtitle,scrapedthumbnail,calidad,idiomas in matches:
        
        patronidiomas = '<img src="[^"]+" title="([^"]+)"'
        matchesidiomas = re.compile(patronidiomas,re.DOTALL).findall(idiomas)
        idiomas_disponibles = ""
        for idioma in matchesidiomas:
            idiomas_disponibles = idiomas_disponibles + idioma.strip() + "/"
        if len(idiomas_disponibles)>0:
            idiomas_disponibles = "["+idiomas_disponibles[:-1]+"]"
        
        title = scrapedtitle.strip()+" "+idiomas_disponibles+"["+calidad+"]"
        url = scrapedurl
        thumbnail = scrapedthumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=scrapedplot , viewmode="movie", folder=True) )

    # Extrae el paginador
    patronvideos  = "<a href='([^']+)'>\&raquo\;</a>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=scrapedurl , folder=True) )

    return itemlist

def categorias(item):
    logger.info("[yaske.py] categorias")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)
    data = scrapertools.get_match(data,'<div cc-type="generos">(.*?)</div>')

    # Extrae las entradas
    #<li><a href="http://www.yaske.net/es/peliculas/genero/drama" cc-value="drama">Drama</a>
    patron  = '<li><a href="([^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []

    for scrapedurl,scrapedtitle in matches:
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[yaske.py] findvideos")

    # Descarga la página
    data = scrapertools.downloadpageGzip(item.url)

    # Extrae las entradas
    '''
    <tr bgcolor="#e6e3e3"><td align="left" >
    <a href="http://www.yaske.net/es/reproductor/pelicula/1748/10734/" title="Los mercenarios 2" target="_blank" style="text-decoration: none;"><img src="http://www.yaske.net/imagenes/servers/veronline.png" height="22" width="22"><b><font color="black">Opcion 11</font></b></a>
    </td> <td align="center"><b>vk</b>
    </td> <td align="left"><span style="margin-left:20px;"><img src="http://www.yaske.net/imagenes/flags/la_la.png" width="23"> Latino</span></td> <td align="center" class="center">
    <span title="DVD SCREENER" style="text-transform:capitalize;">dvd screener</span></td> <td align="center" class="center">
    <a href="http://www.yaske.net/es/reproductor/pelicula/1748/10734/" class="verLink" title="Los mercenarios 2" target="_blank"><img align="middle" width="100" height="26"  src="http://3.bp.blogspot.com/-ueSY010WZK0/UAgWBc6FIGI/AAAAAAAAHVw/P0Qe5GbwJS4/s1600/veron.png" /></a>
    </td> <td align="center" class="episode-uploader"><span>
    <iframe src="http://www.facebook.com/plugins/like.php?href=http://www.yaske.net/es/pelicula/0001748/ver-the-expendables-2-online.html?ref=opcion11&amp;send=false&amp;layout=button_count&amp;width=75&amp;show_faces=true&amp;action=like&amp;colorscheme=light&amp;font=arial&amp;height=21" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:75px; height:21px;" allowTransparency="true"></iframe>
    </span></td> <td align="center" class="center" style="overflow:hidden"><a href="http://twitter.com/share" class="twitter-share-button" data-url="http://www.yaske.net/es/pelicula/0001748/ver-the-expendables-2-online.html?ref=opcion11" data-count="horizontal">Tweet</a></td> </tr>  </tbody>
    '''
    patron  = '<tr[^<]+<td[^<]+'
    patron += '<a href="([^"]+)" title="[^"]+"[^<]+<img[^<]+<b><font[^>]+>([^<]+)</font></b></a>[^<]+'
    patron += '</td[^<]+<td[^<]+<b>([^<]+)</b>[^<]+'
    patron += '</td[^<]+<td[^<]+<span[^<]+<img[^>]+>([^<]+)</span></td[^<]+<td[^<]+'
    patron += '<span title="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []

    for url,title,server,idioma,calidad in matches:
        scrapedtitle = title + " en "+server.strip()+" ["+idioma+" / "+calidad+"]"
        scrapedurl = url
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=False) )

    return itemlist

def play(item):
    logger.info("[letmewatchthis.py] play")
    
    itemlist=[]
    
    data = scrapertools.downloadpageGzip(item.url)
    #logger.info("data="+data)
    itemlist = servertools.find_video_items(data=data)
    
    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    from servers import servertools
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    peliculas_items = peliculas(mainlist_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos( item=pelicula_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien