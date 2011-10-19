# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cineblog01
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import re, htmlentitydefs

from core import scrapertools
from core import logger
from core import config
from core.item import Item

CHANNELNAME = "cineblog01"

DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []

    # Main options
    itemlist.append( Item(channel=CHANNELNAME, action="listvideos", title="Film - Novità" , url="http://cineblog01.com/" ))
    itemlist.append( Item(channel=CHANNELNAME, action="pelisalfa", title="Film - Per Lettera" ))
    itemlist.append( Item(channel=CHANNELNAME, action="peliscat", title="Film - Per Categoria" ))
    itemlist.append( Item(channel=CHANNELNAME, action="searchmovie", title="Film - Cerca" ))
    itemlist.append( Item(channel=CHANNELNAME, action="listserie", title="Serie" , url="http://cineblog01.info/serietv/" ))
    itemlist.append( Item(channel=CHANNELNAME, action="listserie", title="Anime" , url="http://cineblog01.info/anime/" ))

    return itemlist

def pelisalfa(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []

    # Alphabetic menu
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="0-9", url="http://cineblog01.com/category/numero"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="A", url="http://cineblog01.com/category/a"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="B", url="http://cineblog01.com/category/b"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="C", url="http://cineblog01.com/category/c"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="D", url="http://cineblog01.com/category/d"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="E", url="http://cineblog01.com/category/e"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="F", url="http://cineblog01.com/category/f"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="G", url="http://cineblog01.com/category/g"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="H", url="http://cineblog01.com/category/h"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="I", url="http://cineblog01.com/category/i"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="J", url="http://cineblog01.com/category/j"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="K", url="http://cineblog01.com/category/k"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="L", url="http://cineblog01.com/category/l"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="M", url="http://cineblog01.com/category/m"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="N", url="http://cineblog01.com/category/n"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="O", url="http://cineblog01.com/category/o"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="P", url="http://cineblog01.com/category/p"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Q", url="http://cineblog01.com/category/q"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="R", url="http://cineblog01.com/category/r"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="S", url="http://cineblog01.com/category/s"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="T", url="http://cineblog01.com/category/t"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="U", url="http://cineblog01.com/category/u"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="V", url="http://cineblog01.com/category/v"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="W", url="http://cineblog01.com/category/w"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="X", url="http://cineblog01.com/category/x"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Y", url="http://cineblog01.com/category/y"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Z", url="http://cineblog01.com/category/z"))

    return itemlist

def peliscat(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []

    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Animazione", url="http://cineblog01.com/category/animazione/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Avventura", url="http://cineblog01.com/category/avventura/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Azione", url="http://cineblog01.com/category/azione/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Biografico", url="http://cineblog01.com/category/biografico/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Comico", url="http://cineblog01.com/category/comico/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Commedia", url="http://cineblog01.com/category/commedia/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Corti", url="http://cineblog01.com/category/solo-cortometraggio/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Cult", url="http://cineblog01.com/category/cult/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Documentario", url="http://cineblog01.com/category/documentario/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Drammatico", url="http://cineblog01.com/category/drammatico/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Erotico", url="http://cineblog01.com/category/erotico/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Fantascienza", url="http://cineblog01.com/category/fantascienza/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Fantasy", url="http://cineblog01.com/category/fantasyfantastico/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Gangster", url="http://cineblog01.com/category/gangster/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Grottesco", url="http://cineblog01.com/category/grottesco/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Guerra", url="http://cineblog01.com/category/guerra/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Horror", url="http://cineblog01.com/category/horror/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Megavideo", url="http://cineblog01.com/category/solo-megavideo/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Megaupload", url="http://cineblog01.com/?cat=410"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Musical", url="http://cineblog01.com/category/musicale/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Noir", url="http://cineblog01.com/category/noir/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Poliziesco", url="http://cineblog01.com/category/poliziesco/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Sentimentale", url="http://cineblog01.com/category/sentimentale/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Storico", url="http://cineblog01.com/category/storico/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Thriller", url="http://cineblog01.com/category/thriller/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Tutto Totò", url="http://cineblog01.com/category/st-toto/"))
    itemlist.append( Item(channel=CHANNELNAME, action="listcat", title="Western", url="http://cineblog01.com/category/western/"))

    return itemlist

def searchmovie(item):
    logger.info("[cineblog01.py] searchmovie")

    import xbmc
    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
        if len(tecleado)>0:
            #convert to HTML
            tecleado = tecleado.replace(" ", "+")
            item = Item(url="http://cineblog01.com/?s="+tecleado)
            return listvideos(item)

def listcat(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []
    if item.url =="":
        item.url = "http://cineblog01.com/"
        
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div id="covershot".*?<a.*?<img src="(.*?)".*?'
    patronvideos += '<div id="post-title"><a href="(.*?)".*?'
    patronvideos += '<h3>(.*?)</h3>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        # Titulo
        scrapedtitle = scrapertools.unescape(match[2])
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[0])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Remove the next page mark
    patronvideos = '<a href="(http://www.cineblog01.com/category/[0-9a-zA-Z]+/page/[0-9]+/)">Avanti >'
    patronvideos += '/page/[0-9]+/)">Avanti >'
    matches = re.compile (patronvideos, re.DOTALL).findall (data)
    scrapertools.printMatches (matches)

    if len(matches)>0:
        scrapedtitle = "(Next Page ->)"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="listcat" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def listvideos(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []

    if item.url =="":
        item.url = "http://cineblog01.com/"

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div id="covershot".*?<a.*?<img src="(.*?)".*?'
    patronvideos += '<div id="post-title"><a href="(.*?)".*?'
    patronvideos += '<h3>(.*?)</h3>.*?&#160;'
    patronvideos += '&#160;(.*?)</p>'
    #patronvideos += '<div id="description"><p>(.?*)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = scrapertools.unescape(match[2])
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[0])
        scrapedplot = scrapertools.unescape(match[3])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Remove the next page mark <a href="http://cineblog01.com/page/2/">Avanti
    patronvideos = '<a href="(http://[www/.]*cineblog01.com/page/[0-9]+)/">Avanti >'
    matches = re.compile (patronvideos, re.DOTALL).findall (data)
    scrapertools.printMatches (matches)

    if len(matches)>0:
        scrapedtitle = "(Next Page ->)"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="listvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def listserie(item):
    logger.info("[cineblog01.py] mainlist")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = '<div id="covershot".*?<a.*?<img src="(.*?)".*?'
    patronvideos += '<div id="post-title"><a href="(.*?)".*?'
    patronvideos += '<h3>(.*?)</h3>'
    patronvideos += '(.*?)</p>'
    #patronvideos += '<div id="description"><p>(.?*)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = scrapertools.unescape(match[2])
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[0])
        scrapedplot = scrapertools.unescape(match[3])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    # Remove the next page mark
    patronvideos = '<a href="(http://www.cineblog01.info/[^\/]+/page/[0-9]+)">&gt;'
    matches = re.compile (patronvideos, re.DOTALL).findall (data)
    scrapertools.printMatches (matches)

    if len(matches)>0:
        scrapedtitle = "(Next Page ->)"
        scrapedurl = matches[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="listserie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist
