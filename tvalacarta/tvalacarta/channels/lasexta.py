# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Canal para la sexta
#------------------------------------------------------------
import urlparse,re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[sexta.py] init")

DEBUG = True
CHANNELNAME = "lasexta"
MAIN_URL = "http://www.lasexta.com/programas"
def isGeneric():
    return True

def mainlist(item):
    logger.info("[sexta.py] mainlist")
    itemlist=[]
    
    itemlist.append( Item(channel="antena3", title="Series"         , action="series"       , url="http://www.lasexta.com/videos/series.html", folder=True) )
    itemlist.append( Item(channel="antena3", title="Noticias"       , action="series"     , url="http://www.lasexta.com/videos/noticias.html", folder=True) )
    itemlist.append( Item(channel="antena3", title="Programas"      , action="series"    , url="http://www.lasexta.com/videos/programas.html", folder=True) )
    itemlist.append( Item(channel="antena3", title="Xplora"         , action="series"       , url="http://www.lasexta.com/videos/series-infantiles.html", folder=True) )

    return itemlist

    # Descarga la pagina
    #item.url = MAIN_URL
    #return programas(item)

def programas(item):
    logger.info("[sexta.py] programas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae los programas
    patron  = '<div class="mod_promocion_producto">[^<]+'
    patron += '<div class="">[^<]+'
    patron += '<a title="([^"]+)" href="([^"]+)">[^<]+'
    patron += '<img title="[^"]+" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    for scrapedtitle,scrapedurl,scrapedthumbnail in matches:
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="episodios" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=urlparse.urljoin(item.url,scrapedthumbnail) , show = scrapedtitle, folder=True) )
    
    return itemlist

def episodios(item):
    logger.info("[sexta.py] episodios")
    itemlist = []

    # Descarga la página principal
    datapre = scrapertools.cache_page(item.url)
    #logger.info(datapre)

    # Accede a la sección 'todos los programas'
    patron  = '<a title="PROGRAMAS COMPLETOS" href="([^"]+)"'
    episodiosurl = re.compile(patron,re.DOTALL).search(datapre).group(1);
    logger.info("URL episodios: " + episodiosurl)
    data = scrapertools.cache_page(episodiosurl)
    logger.info(data)

    # Extrae la parte de programas
    patron = '<div class="visor">(.*)<!-- fin clase visor -->'
    episodiosdata = re.compile(patron,re.DOTALL).search(data).group(1);

    # Extrae las series
    patron  = '<img title="[^"]+"[^s]+src="([^"]+)"'
    patron += '[^a]+alt="[^"]+"[^h]+href="([^"]+)".*?'
    patron += '<h2><p>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(episodiosdata)
    if DEBUG: scrapertools.printMatches(matches)
    
    for scrapedthumbnail,scrapedurl,scrapedtitle in matches:

        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="partes" , url=urlparse.urljoin(item.url,scrapedurl), thumbnail=scrapedthumbnail , show = scrapedtitle, folder=True) )

    return itemlist

def partes(item):
    logger.info("[sexta.py] partes")
    itemlist = []

    # Descarga la página
    dataplayer = scrapertools.cache_page(item.url)
    logger.info(dataplayer)

    #player_capitulo.xml='/chapterxml//60000001/60000007/2012/10/03/00008.xml';
    patron  = "player_capitulo.xml='([^']+)'"
    partesurl = re.compile(patron,re.DOTALL).search(dataplayer).group(1);
    xmldata = scrapertools.cache_page(urlparse.urljoin('http://www.lasexta.com',partesurl))
    logger.info(xmldata)

    # url prefix
    patron  = '<urlVideoMp4><!\[CDATA\[(.*?)\]\]></urlVideoMp4>'
    prefix  = re.compile(patron,re.DOTALL).search(xmldata).group(1);
    logger.info(prefix)

    patron  = '<archivoMultimedia>[^<]+<archivo><!\[CDATA\[([^\]]+)'
    matches = re.compile(patron,re.DOTALL).findall(xmldata)
    if DEBUG: scrapertools.printMatches(matches)
    logger.info("matches="+str(matches))
    i=1
    for url in matches:
        scrapedtitle = "("+str(i)+") "+item.title
        scrapedurl = urlparse.urljoin(prefix.replace('rtmp:','http:'),url).replace('http:','rtmp:')
        scrapedthumbnail = item.thumbnail
        scrapedplot = item.plot
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail , show = scrapedtitle, folder=False) )
        i=i+1

    return itemlist
