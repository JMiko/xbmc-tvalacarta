# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Clan TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = True
CHANNELNAME = "clantve"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[clantv.py] mainlist")
    item = Item(url="http://www.rtve.es/infantil/series/")
    return programas(item)

def programas(item):
    logger.info("[clantv.py] programas")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    # Extrae los programas
    patron  = '<div class="informacion-serie">[^<]+'
    patron += '<h3>[^<]+'
    patron += '<a href="([^"]+)">([^<]+)</a>[^<]+'
    patron += '</h3>[^<]+'
    patron += '<a[^>]+>[^<]+</a><img.*?src="([^"]+)"><div>(.*?)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedtitle = scrapertools.unescape(scrapedtitle)
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedurl = urlparse.urljoin(scrapedurl,"videos")
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = match[3]
        scrapedplot = scrapertools.unescape(scrapedplot).strip()
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()

        scrapedpage = urlparse.urljoin(item.url,match[0])
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] plot=["+scrapedplot+"]")
        #logger.info(scrapedplot)

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , page=scrapedpage, show=scrapedtitle , folder=True) )

    # Añade el resto de páginas
    patron = '<li class="siguiente">[^<]+<a rel="next" title="Ir a la p&aacute;gina siguiente" href="([^"]+)">Siguiente'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        match = matches[0]
        newitem = Item(channel=CHANNELNAME,url=urlparse.urljoin(item.url,match))
        itemlist.extend(programas(newitem))

    return itemlist

def detalle_programa(item):
    
    #http://www.rtve.es/infantil/series/monsuno/videos/
    #http://www.rtve.es/infantil/series/hay-nuevo-scooby-doo/
    url = item.url
    if url.endswith("/videos"):
        url = url.replace("/videos","")
    
    # Descarga la página
    data = scrapertools.cache_page(url)
    data = scrapertools.get_match(data,'<div class="contenido-serie">(.*?)</div>')

    # Obtiene el thumbnail
    try:
        item.thumbnail = scrapertools.get_match(data,'<img.*?src="([^"]+)"')
    except:
        pass

    try:
        item.plot = scrapertools.htmlclean( scrapertools.get_match(data,'</h3>(.*?)</div>') )
    except:
        pass

    try:
        title = scrapertools.get_match(data,'<h3>[^<]+<a[^>]+>([^<]+)</a>[^<]+</h3>').strip()
        item.title = scrapertools.entityunescape(title)
    except:
        pass

    return item

def episodios(item):
    logger.info("[clantv.py] episodios")

    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)

    # Extrae los capítulos
    patron = '<div class="contenido-serie">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    logger.info("[clantv.py] encontrados %d episodios" % len(matches) )
    if len(matches)==0:
        return itemlist
    data2 = matches[0]

    patron = '<a rel="([^"]+)".*?href="([^"]+)"><img src="([^"]+)"[^>]+>(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data2)
    scrapertools.printMatches(matches)

    # Extrae los items
    for match in matches:
        scrapedtitle = match[3]
        scrapedtitle = scrapertools.unescape(scrapedtitle)
        scrapedtitle = scrapertools.htmlclean(scrapedtitle)
        scrapedtitle = unicode(scrapedtitle,"utf-8").capitalize().encode("utf-8")
        
        # La página del vídeo
        scrapedpage = urlparse.urljoin(item.url,match[1])
        scrapedpage = scrapedpage.replace("videos-juegos/videos","videos-juegos/#/videos")
        
        # Código de la serie
        scrapedcode = match[0]
        
        # Url de la playlist
        scrapedurl = "http://www.rtve.es/infantil/components/"+scrapedcode+"/videos.xml.inc"
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("scraped title=["+scrapedtitle+"], url=["+scrapedurl+"], page=["+scrapedpage+"] thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="Directo", page=scrapedpage, url=scrapedurl, thumbnail=scrapedthumbnail, fanart=item.thumbnail, show=item.show , plot=scrapedplot , folder=False) )

    # Ahora extrae el argumento y la url del vídeo
    dataplaylist = scrapertools.cachePage(scrapedurl)
    
    for episodeitem in itemlist:
        partes = episodeitem.page.split("/")
        code = partes[len(partes)-2]
        patron  = '<video id="'+code+'".*?url="([^"]+)".*?'
        patron += '<sinopsis>(.*?)</sinopsis>'
        matches = re.compile(patron,re.DOTALL).findall(dataplaylist)

        if len(matches)>0:
            episodeitem.url = urlparse.urljoin(item.url,matches[0][0])
            episodeitem.plot = matches[0][1]

    # Añade el resto de páginas
    patron = '<li class="siguiente"><a rel="next" title="Ir a la p&aacute;gina siguiente" href="([^"]+)">Siguiente</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)>0:
        match = matches[0]
        item.url = urlparse.urljoin(item.url,match)
        itemlist.extend(episodios(item))

    from core import config
    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title=">> Añadir la serie completa a la lista de descarga", url=item.url, action="download_all_episodes##episodios", show=item.show) )

    return itemlist
