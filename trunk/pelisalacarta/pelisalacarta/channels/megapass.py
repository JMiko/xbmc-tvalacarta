# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Megapass (por MarioXD)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "F"
__type__ = "generic"
__title__ = "Megapass"
__channel__ = "megapass"
__language__ = "ES"
__creationdate__ = "20111014"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[Megapass.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"                , action="menupeliculas"))
    itemlist.append( Item(channel=__channel__, title="Series"                   , action="menuseries"))
    itemlist.append( Item(channel=__channel__, title="Documentales"             , action="menudocumentales"))
    itemlist.append( Item(channel=__channel__, title="TV Shows"                    , action="menutv"))
    itemlist.append( Item(channel=__channel__, title="Otros Videos"                    , action="menuotros"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )   
    return itemlist

def menupeliculas(item):
    logger.info("[Megapass.py] menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Películas"            , url="http://megapass.se/search.php?c=1_1" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Películas HD"            , url="http://megapass.se/search.php?c=1_8" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Películas ordenadas por fecha"            , url="http://megapass.se/search.php?c=1_1&p=0&o=1" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Películas ordenadas por número de votos"            , url="http://megapass.se/search.php?c=1_1&p=0&o=0" ))  
    return itemlist
    
    
def menuseries(item):
    logger.info("[Megapass.py] menuseries")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Series ordenadas por fecha"            , url="http://megapass.se/search.php?c=1_7&p=0&o=1" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Series ordenadas por número de votos"            , url="http://megapass.se/search.php?c=1_7&p=0&o=0" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Series HD ordenadas por fecha"            , url="http://megapass.se/search.php?c=1_9&p=0&o=1" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Series HD ordenadas por número de votos"            , url="http://megapass.se/search.php?c=1_9&p=0&o=0" ))  
    return itemlist
    
    
def menudocumentales(item):
    logger.info("[Megapass.py] menudocumentales")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Documentales ordenados por fecha"            , url="http://megapass.se/search.php?c=1_10&p=0&o=1" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Documentales ordenados por número de votos"            , url="http://megapass.se/search.php?c=1_10&p=0&o=0" ))  
    return itemlist
    
    
def menutv(item):
    logger.info("[Megapass.py] menutv")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="TV Shows ordenados por fecha"            , url="http://megapass.se/search.php?c=1_4&p=0&o=1" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="TV Shows ordenados por número de votos"            , url="http://megapass.se/search.php?c=1_4&p=0&o=0" ))  
    return itemlist
 
    
def menuotros(item):
    logger.info("[Megapass.py] menuotros")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Otros Videos ordenados por fecha"            , url="http://megapass.se/search.php?c=1_6&p=0&o=1" ))  
    itemlist.append( Item(channel=__channel__, action="peliculas" , title="Otros Videos ordenados por número de votos"            , url="http://megapass.se/search.php?c=1_6&p=0&o=0" ))  
    return itemlist
     

def search(item,texto):
    logger.info("[Megapass.py] search ")
    itemlist = []
    item.url = "http://megapass.se/search.php?b=%s" % texto
    return peliculas(item)
        
    

def peliculas(item):
    logger.info("[Megapass.py] peliculas")
    data = scrapertools.cache_page(item.url)  
    patronvideos = "<div style='([^']+)' class='imgDiv'></div></a></td><td class='nombre' valign='top' align='left' height='10px'><a href='([^']+)'>([^<]+)</a><a href='search.php"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []    
    for match in matches:
        scrapedtitle = scrapertools.entityunescape(match[2])
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedurl = scrapedurl.replace("ver","go")
        scrapedthumbnail = urlparse.urljoin(item.thumbnail,match[0].replace("background-image:url(","http://megapass.se/"))
        scrapedthumbnail = scrapedthumbnail.replace(")","")       
        #scrapedtitle = scrapertools.entityunescape(match[2])
        scrapedtitle=scrapedtitle
        fulltitle = scrapedtitle        
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findbitly_link" , title=fulltitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot,  viewmode="movie"))
        
    
    #EXTRAE EL LINK DE LA SIGUIENTE PAGINA
    patron = "<td align='center'>\d{1,4}</td><td align='center' class='conTexto'><a href='([^']+)'><div>\d{1,4}</div></a></td>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    for scrapedurl in matches:
        scrapedurl = scrapedurl.replace("?","http://megapass.se/search.php?")
        scrapedtitle = "Pagina Siguiente >>>"
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot,  viewmode="movie"))
    return itemlist

#############################################################################################################################
#                                             EXTRAE LINKS DE BITLY.COM                                                     #
#############################################################################################################################

def findbitly_link(item):  
    logger.info("[Megapass.py] otros")
    itemlist=[]
    data = scrapertools.cachePage(item.url)
    patron_bitly  = "CONTENT='.*?; URL=(.*?)'><p align='center'"
    matches = re.compile(patron_bitly,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl in matches:
        scrapedurl = "http://api.bit.ly/expand?version=2.0.1&shortUrl=" + scrapedurl + "&login=pelisprueba&apiKey=R_b16c5ac46083d0e768060440f0137d7d"        
        megalink=scrapedurl
        return extract_mega(item,megalink)

def extract_mega(item,megalink):  
    logger.info("[Megapass.py] peliculas")
    itemlist=[]
    data = scrapertools.cachePage(megalink)
    
    #{"errorCode": 0, "errorMessage": "", "results": {"13DOLlu": {"longUrl": "https://mega.co.nz/#!2A8ESBTI!Fd4g-nQU0bTk9hQ1PaeTy1BQA0o1J4QupyBzmTpbx_U"}}, "statusCode": "OK"}
    patron_mega  = '"longUrl": "([^"]+)"}}, "statusCode": "[^"]+"}'
    matches = re.compile(patron_mega,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for scrapedurl in matches:
        scrapedurl =            scrapedurl.replace("https://mega.co.nz/#!","http://megastreamer.net/mega_stream.php?url=https%3A%2F%2Fmega.co.nz%2F%23%21")
        scrapedurl = scrapedurl.replace("!","%21")
        scrapedurl=scrapedurl+"&mime=vnd.divx"
        itemlist.append( Item(channel=__channel__, action="play" , title="Ver en Mega -" + item.title, url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot))
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # Navega hasta la lista de películas
    mainlist_items = mainlist(Item())
    menupeliculas_items = menupeliculas(mainlist_items[0])
    peliculas_items = peliculas(menupeliculas_items[0])
    
    # Si encuentra algún enlace, lo da por bueno
    for pelicula_item in peliculas_items:
        itemlist = findbitly_link(pelicula_item)
        if not itemlist is None and len(itemlist)>=0:
            return True

    return False
