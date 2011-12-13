# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para series21 by Bandavi
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys,string
from core import decrypt21

from core import scrapertools
from core import config
from core import logger
from core.item import Item

CHANNELNAME = "series21"
DEBUG = True
FANART = os.path.join( config.get_runtime_path(), 'resources' , 'images' ,'fanart','series21.jpg')

def isGeneric():
    return True

def mainlist(item):
    logger.info("[series21.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Series - A-Z", action="letras"  , url="http://www.series21.com", fanart=FANART))
    print FANART
    return itemlist

def letras(item):
    logger.info("[series21.py] letras")
    itemlist = []

    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letra in alfabeto:
        itemlist.append( Item(channel=item.channel, action="series", title=str(letra), url = "http://www.series21.com/"+letra+"/", fanart=FANART))

    itemlist.append( Item(channel=item.channel, action="series", title=str(letra), url = "http://www.series21.com/0-9/", fanart=FANART))

    return itemlist

def series(item):
    logger.info("[series21.py] series")

    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    '''
    <div class="serietemporadas">
    <a href="/dark-blue/"  target="_blank">
    <img class="thumbSerie" src="http://img1.series21.com/thumbs/series_95x140_85/116.jpg" width="95" height="140" alt="Dark Blue" />
    </a>
    <a href="/dark-blue/"  target="_blank" class="titulo">
    Dark Blue</a>
    <div class="sinopsis">
    <span class="negrita">Sinopsis: </span>Carter Shaw es el líder de un equipo elite de policías que trabajan de una manera encubierta en casos misteriosos, tanto que ni siquiera sus colegas saben que están implicados.
        Shaw es un hombre que a sufrido mucho, perdió a su esposa y con ello una parte de su vida, el intentara capturar a los p...</div>
    '''
    patron  = '<div class="serietemporadas"[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += '<img class="thumbSerie" src="([^"]+)"[^<]+'
    patron += '</a>[^<]+'
    patron += '<a[^>]+>([^<]+)</a>[^<]+'
    patron += '<div class="sinopsis">[^<]+'
    patron += '<span class="negrita">Sinopsis: </span>([^<]+)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot in matches:
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        scrapedtitle = scrapedtitle.strip()
        itemlist.append( Item(channel=item.channel, action="episodios", title=scrapedtitle , fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail, category="series" , plot=scrapedplot, show=scrapedtitle, fanart=FANART) )

    return itemlist

def episodios(item):
    logger.info("[series21.py] episodios")
    
    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #<li><a href="/dark-blue/1x04-ciudad-k-k-town/" class="links-series">1x04 - Ciudad - k</a> <span><img src="/images/esp.gif" class="bandera"> | Subtitulado</span></li></li>
    patron  = '<li><a href="([^"]+)" class="links-series">([^<]+)</a> <span>(.*?)</span></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedtitle, resto in matches:
        scrapedurl = urlparse.urljoin(item.url,scrapedurl)
        resto = resto.replace('<img src="/images/','')
        resto = resto.replace('.gif" class="bandera">','')
        scrapedtitle = scrapedtitle + " ("+resto+")"
        itemlist.append( Item(channel=item.channel, action="findvideos", title=scrapedtitle , fulltitle=item.title+" "+scrapedtitle , url=scrapedurl , thumbnail=item.thumbnail, category="series" , plot=item.plot, show=item.show, fanart=FANART) )

    return itemlist

