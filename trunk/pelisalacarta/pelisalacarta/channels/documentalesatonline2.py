# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para documentalesatonline2
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

import xml.dom.minidom

CHANNELNAME = "documentalesatonline2"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[documentalesatonline2.py] mainlist")
    itemlist=[]

    itemlist.append( Item(channel=CHANNELNAME, title="Novedades"  , action="novedades" , url="http://www.bizzentte.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Categorías" , action="categorias" , url="http://www.bizzentte.com/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar"     , action="search"))

    return itemlist

def search(item):
    buscador.listar_busquedas(item)

def searchresults(params,tecleado,category):
    logger.info("[documentalesatonline2.py] search")

    buscador.salvar_busquedas(params,tecleado,category)
    tecleado = tecleado.replace(" ", "+")
    searchUrl = "http://documentalesatonline.loquenosecuenta.com/search/"+tecleado+"?feed=rss2&paged=1"
    novedades(params,searchUrl,category)

def categorias(item):
    logger.info("[documentalesatonline2.py] novedades")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    #<li class="jcl_category" style="display:none;" >
    #<a href="http://www.bizzentte.com/categoria/categorias-en-general-para-todo/arte-y-cultura/" >Arte y Cultura (80)</a>
    #<a class="jcl_link" href="#jcl" title="Ver Sub-Categor&iacute;as">
    #<span class="jcl_symbol" style="padding-left:5px">(+)</span></a>
    #<ul>
    #<li class="jcl_category" style="display:none;" ><a href="http://www.bizzentte.com/categoria/categorias-en-general-para-todo/arte-y-cultura/fotografia/" >Fotografia (2)</a></li><li class="jcl_category" style="display:none;" ><a href="http://www.bizzentte.com/categoria/categorias-en-general-para-todo/arte-y-cultura/grafiti/" >Grafiti (2)</a></li>
    patronvideos  = '<li class="jcl_category"[^>]+><a href="([^"]+)"[^>]*>([^<]+)</a></li>'
    # '\" url nombre cantidad_entradas
    matches = re.compile(patronvideos).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        #xbmctools.addnewfolder( CHANNELNAME , "novedades" , category , match[1] , match[0] + "feed?paged=1" , "" , "")
        itemlist.append( Item(channel=CHANNELNAME, action="novedades", title=match[1] , url=match[0] , folder=True) )

    return itemlist

def novedades(item):
    logger.info("[documentalesatonline2.py] novedades")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    
    # Entradas
    '''
    <h2 id="post-5250"><a href="http://www.bizzentte.com/2011/08/chips-implantes-de-futuro-2009-documental-c-odisea-rfid-espanol/" rel="bookmark">Chips: Implantes de futuro.2009 (Documental C.Odisea) (RFID) (Español)</a></h2>
    <div class="main">
    <p>En este interesante documental, seguimos a Mark Stepanek mientras delibera si debe o no obtener una identificación por radiofrecuencia (RFID), es decir, implantarse un microchip, semejante al que pueda llevar una mascota, en su propia mano..</p>
    <ul class="readmore">
    <li>&raquo;
    <a href="http://www.bizzentte.com/2011/08/chips-implantes-de-futuro-2009-documental-c-odisea-rfid-espanol/#comments">Comentarios</a>
    <a href="http://www.bizzentte.com/2011/08/chips-implantes-de-futuro-2009-documental-c-odisea-rfid-espanol/#comments" title="Comentarios en Chips: Implantes de futuro.2009 (Documental C.Odisea) (RFID) (Español)">(3)</a>						</li>
    </ul>
    </div>
    '''
    patron  = '<h2 id="post-[^"]+"><a href="([^"]+)"[^>]+>([^<]+)</a></h2>[^<]+'
    patron += '<div class="main">[^<]+'
    patron += '<p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    # Página siguiente
    patron  = '<a href="([^"]+)" >P..gina siguiente \&raquo\;</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, action="novedades", title="!Página siguiente" , url=urlparse.urljoin(item.url,match) , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[documentalesatonline2.py] findvideos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patronvideos0  = '- [0-9]+? de [0-9]+?:(.+)'
    #- 1 de 3:
    matches0 = re.compile(patronvideos0).findall(data)
    
    if len(matches0)==0:
        patronvideos0  = 'Episodio \d+(.+)'
        #- Episodio 03:
        matches0 = re.compile(patronvideos0).findall(data)
        #logger.info(matches0)
    
    if len(matches0)>0:
        listavideos = servertools.findvideos(data)
        if (2*len(matches0))==len(listavideos):
            logger.info("es el doble, vamos a anadir un link de megavideo y uno de megaupload por cada fideo")
            length=len(matches0)
            for i in range(len(matches0)):
                title=listavideos[0+i][0]
                url=listavideos[0+i][1]
                server=listavideos[0+i][2]
                #logger.info(matches0)
                itemlist.append( Item(channel=CHANNELNAME, action="play", title=strip_ml_tags(matches0[i]).replace(":","").strip() + " " + listavideos[0+i][0] , url=listavideos[0+i][1] , server=listavideos[0+i][2] , folder=False ))
                itemlist.append( Item(channel=CHANNELNAME, action="play", title=strip_ml_tags(matches0[i]).replace(":","").strip() + " " + listavideos[length+i][0] , url=listavideos[length+i][1] , server=listavideos[length+i][2] , folder=False ))
        elif len(listavideos)>0:
            for video in listavideos:
                itemlist.append( Item(channel=CHANNELNAME, action="play", title=matches[0] +  video[0] , url=video[1] , server=video[2], folder=False ))
        else:
            logger.info("vamos a ponerlos con el nombre del titulo todos, el mismo que el por defecto")
            logger.info("no hay capitulos")
            patronvideos  = '(.+?)\('
            matches = re.compile(patronvideos).findall(category)
            listavideos = servertools.findvideos(data)
            
            for video in listavideos:
                itemlist.append( Item(channel=CHANNELNAME, action="play", title=matches[0] +  video[0] , url=video[1] , server=video[2], folder=False ))
    else: 
        logger.info("no hay capitulos")
        patronvideos  = '(.+?)\('
        matches = re.compile(patronvideos).findall(category)
        # Busca los enlaces a los videos
        listavideos = servertools.findvideos(data)
        
        for video in listavideos:
            itemlist.append( Item(channel=CHANNELNAME, action="play", title=matches[0] +  video[0] , url=video[1] , server=video[2] , folder=False ))

    patronvideos  = '<a rel="bookmark" href="../(.+?)">(.+?)<'
    matches = re.compile(patronvideos).findall(data)
    for z in matches:
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=z[1], url=urlparse.urljoin(item.url,z[0]) , folder=True ))

    return itemlist

def strip_ml_tags(in_text):
    #source http://code.activestate.com/recipes/440481-strips-xmlhtml-tags-from-string/
    s_list = list(in_text)
    i = 0

    while i < len(s_list):
        if s_list[i] == '<':
            while s_list[i] != '>':
                s_list.pop(i)
            s_list.pop(i)
        else:
            i=i+1

    join_char=''
    return join_char.join(s_list)
