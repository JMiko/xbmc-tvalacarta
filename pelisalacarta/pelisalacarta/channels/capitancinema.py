# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para capitancinema
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "capitancinema"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[capitancinema.py] mainlist")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage("http://www.capitancinema.com/foro/")

    # Extrae los títulos de los subforos
    '''
    <div class="forabg">
    <div class="inner"><span class="corners-top"><span></span></span>
    <ul class="topiclist">
    <li class="header">
    <dl class="icon">
    <dt><a href="http://www.capitancinema.com/foro/descargas-series/">Series TV en Descarga Directa</a></dt>
    '''
    patron  = '<div class="forabg">[^<]+'
    patron += '<div class="inner"><span class="corners-top"><span></span></span>[^<]+'
    patron += '<ul class="topiclist">[^<]+'
    patron += '<li class="header">[^<]+'
    patron += '<dl class="icon">[^<]+'
    patron += '<dt><a href="([^"]+)">([^<]+)</a></dt>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist=[]
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="subforos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def subforos(item):
    logger.info("[capitancinema.py] subforos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # De la página del foro, extrae primero los subforos
    '''
    <div class="forabg">
    <div class="inner"><span class="corners-top"><span></span></span>
    <ul class="topiclist">
    <li class="header">
    <dl class="icon">
    <dt>Foro</dt>
    '''
    patron  = '<div class="forabg">[^<]+'
    patron += '<div class="inner"><span class="corners-top"><span></span></span>[^<]+'
    patron += '<ul class="topiclist">[^<]+'
    patron += '<li class="header">[^<]+'
    patron += '<dl class="icon">[^<]+'
    patron += '<dt>Foro</dt>(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    
    data2 = matches[0]
    patron  = '<li class="row">[^<]+'
    patron += '<dl[^>]+>[^<]+'
    patron += '<dt[^>]+>[^<]+'
    patron += '<a href="([^"]+)" class="forumtitle">([^<]+)</a><br />'
    matches = re.compile(patron,re.DOTALL).findall(data2)

    for match in matches:
        # Atributos
        scrapedtitle = "["+match[1]+"]"
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="temas", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # De la página del foro, extrae ahora las entradas directas a los temas
    itemlist.extend(temas(item))
    return itemlist

def temas(item):
    logger.info("[capitancinema.py] temas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas (carpetas)
    '''
    <li class="row bg2">
    <dl class="icon" style="background-image: url(http://www.capitancinema.com/foro/styles/buziness_board/imageset/topic_read.png); background-repeat: no-repeat;">
    <dt title="No hay nuevos mensajes"><a href="http://www.capitancinema.com/foro/brrip/red-t4370.html" class="topictitle">Red [1080p AC3 2010][Accion]</a>
    '''
    patron  = '<li class="row bg.">[^<]+'
    patron += '<dl[^>]+>[^<]+'
    patron += '<dt[^>]+><a href="([^"]+)" class="topictitle">([^<]+)</a>[^<]+'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    itemlist=[]
    for match in matches:
        # Atributos
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist
