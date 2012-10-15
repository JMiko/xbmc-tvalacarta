# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para vertelenovelas
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "vertelenovelas"
__category__ = "S"
__type__ = "generic"
__title__ = "Ver Telenovelas"
__language__ = "ES"
__creationdate__ = "20121015"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[vertelenovelas.py] mainlist")
    
    itemlist = []

    itemlist.append( Item(channel=__channel__, action="novedades_episodios" , title="�ltimos cap�tulos agregados" , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="novedades"           , title="Nuevas telenovelas"     , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="top"                 , title="Telenovelas TOP"        , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="emision"             , title="Telenovelas en emisi�n" , url="http://vertelenovelas.net/"))
    itemlist.append( Item(channel=__channel__, action="todas"               , title="Lista completa"         , url="http://vertelenovelas.net/"))

    return itemlist

def novedades_episodios(item):
    logger.info("[vertelenovelas.py] novedades_episodios")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    '''
    <div class="dia">
    <a href="capitulo/la-voz-espana-5.html" title="La Voz Espa�a 5">
    <img src="http://vertelenovelas.net/image_files/la-voz-espana.jpg" width="70px" height="105px" align="left"/></a>
    <div class="dia-titulo"><a href="capitulo/la-voz-espana-5.html" class="tts">La Voz Espa�a 5</a></div>
    10/13/2012<br /><br />
    '''
    patron  = '<div class="dia">[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)"[^<]+</a>[^<]+'
    patron += '<div class="dia-titulo"><a[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    return itemlist

def novedades(item):
    logger.info("[vertelenovelas.py] novedades")
    itemlist = []

    # Descarga la p�gina
    data = scrapertools.cachePage(item.url)
    '''
    <div class="cont_anime"><div class="anime_box"> <a href="mi-problema-con-las-mujeres.html" title="Mi problema con las mujeres"><img src="http://vertelenovelas.net/image_files/mi-problema-con-las-mujeres.jpg" alt="Mi problema con las mujeres"></a> <div></div> <span><h1><a href="mi-problema-con-las-mujeres.html" title="Mi problema con las mujeres">Mi problema con las mujeres</a></h1></span> </div></div>
    '''
    patron  = '<div class="cont_anime"><div class="anime_box"[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,scrapedtitle,scrapedthumbnail in matches:
        scrapedplot = ""
        scrapedurl = urlparse.urljoin(item.url,url)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="episodios", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    return itemlist

def episodios(item):
    logger.info("[vertelenovelas.py] episodios")
    itemlist = []

    # Descarga la p�gina
    
    data = scrapertools.cachePage(item.url)
    patron  = '<li class="lc"><a href="([^"]+)" class="lcc">([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for url,scrapedtitle in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedurl = urlparse.urljoin(item.url,url)

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )
    
    return itemlist

def findvideos(item):
    logger.info("[vertelenovelas.py] findvideos")
    data = scrapertools.cache_page(item.url)
    itemlist=[]

    #<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf" width="680" height="430" id="mpl" name="mpl" quality="high" allowscriptaccess="always" allowfullscreen="true" wmode="transparent" flashvars="&file=http://content1.catalog.video.msn.com/e2/ds/4eeea8b3-6228-492b-a2be-e8b920cf4d4e.flv&backcolor=fd4bc5&frontcolor=fc9dde&lightcolor=ffffff&controlbar=over&volume=100&autostart=false&image=">
    #<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf" width="680" height="430" id="mpl" name="mpl" quality="high" allowscriptaccess="always" allowfullscreen="true" wmode="transparent" flashvars="&file=http://content1.catalog.video.msn.com/e2/ds/4eeea8b3-6228-492b-a2be-e8b920cf4d4e.flv&backcolor=fd4bc5&frontcolor=fc9dde&lightcolor=ffffff&controlbar=over&volume=100&autostart=false&image="></embed></d
    patron = '<embed type="application/x-shockwave-flash" src="http://vertelenovelas.net/player.swf".*?file=([^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=match , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    #<embed width="680" height="450" flashvars="file=mp4:p/459791/sp/45979100/serveFlavor/flavorId/0_0pacv7kr/forceproxy/true&amp;image=&amp;skin=&amp;abouttext=&amp;dock=false&amp;streamer=rtmp://rtmpakmi.kaltura.com/ondemand/&amp;
    patron = '<embed width="[^"]+" height="[^"]+" flashvars="file=([^\&]+)&.*?streamer=(rtmp[^\&]+)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for final,principio in matches:
        itemlist.append( Item(channel=__channel__, action="play", server="directo", title=item.title , url=principio+final , thumbnail=item.thumbnail , plot=item.plot , folder=False) )

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist

def todas(item):
    logger.info("[vertelenovelas.py] todas")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div id="noti-titulo">Lista de Telenovelas</div>[^<]+<div class="dm">(.*?)</div>')
    
    patron = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for url,title in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=scrapedurl , folder=True) )

    return itemlist

def emision(item):
    logger.info("[vertelenovelas.py] todas")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'titulo">Telenovelas En Emis[^<]+</div>(.*?)</div>')
    
    patron = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for url,title in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=scrapedurl , folder=True) )

    return itemlist

def top(item):
    logger.info("[vertelenovelas.py] todas")
    itemlist=[]

    data = scrapertools.cache_page(item.url)
    data = scrapertools.get_match(data,'<div id="categoria-titulo">Telenovelas TOP</div>(.*?)</div>')
    
    patron = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for url,title in matches:
        scrapedurl = urlparse.urljoin(item.url,url)
        itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=scrapedurl , folder=True) )

    return itemlist

# Verificaci�n autom�tica de canales: Esta funci�n debe devolver "True" si est� ok el canal.
def test():

    # mainlist
    mainlist_items = mainlist(Item())
    novedades_items = novedades_episodios(mainlist_items[1])
    # Da por bueno el canal si alguno de los v�deos de "Novedades" devuelve mirrors
    bien = False
    for singleitem in novedades_items:
        mirrors = findvideos( item=singleitem )
        if len(mirrors)>0:
            bien = True
            break

    return bien