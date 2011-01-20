# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para Extremadura TV
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item 

logger.info("[extremaduratv.py] init")

DEBUG = True
CHANNELNAME = "extremaduratv"
CHANNELCODE = "extremaduratv"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[extremaduratv.py] channel")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Por categorías" , action="categorias" , url="http://extremaduratv.canalextremadura.es/tv-a-la-carta", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Por programas"  , action="programas"  , url="http://extremaduratv.canalextremadura.es/tv-a-la-carta", folder=True) )

    return itemlist

def categorias(item):
    logger.info("[extremaduratv.py] categorias")

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae los programas
    # --------------------------------------------------------
    patron = '<select name="categoria"(.*?)</select>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data = matches[0]
    patron = '<option value="(\d+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = "http://extremaduratv.canalextremadura.es/search/videos/programa%3A" + match[0] + "+categoria%3A0"
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , folder=True) )

    return itemlist

def programas(item):
    logger.info("[extremaduratv.py] programas")

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae los programas
    # --------------------------------------------------------
    patron = ' <select name="programa"(.*?)</select>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data = matches[0]
    patron = '<option value="(\d+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = "http://extremaduratv.canalextremadura.es/search/videos/programa%3A" + match[0] + "+categoria%3A0"
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , folder=True) )

    return itemlist

def videolist(item):
    logger.info("[extremaduratv.py] videolist")

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae los programas
    # --------------------------------------------------------
    patron  = '<div class="item_busqueda">\W*<div class="foto">\W*<img src="([^"]+)" alt="" title=""\W*/>\W*</div>\W*<div class="datos">\W*<div class="titulo"><a href="([^"]+)">(.*?)</a>.*?-->(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    
    for match in matches:
        # Datos
        #'<span class="color_1">extremadura</span><span class="miniespacio"> </span><span class="color_2">desde</span><span class="miniespacio"> </span><span class="color_3">el</span><span class="miniespacio"> </span><span class="color_1">aire:</span><span class="miniespacio"> </span><span class="color_2">llega</span><span class="miniespacio"> </span><span class="color_1">aire</span><span class="miniespacio"> </span><span class="color_3">con</span><span class="miniespacio"> </span><span class="color_1">olores</span><span class="miniespacio"> </span><span class="color_2">portugueses</span><span class="miniespacio"> </span>'
        #'extremadura desde el aire: llega aire con olores portugueses '
        scrapedtitle = match[2]
        scrapedtitle = scrapedtitle.replace('<span class="color_1">','')
        scrapedtitle = scrapedtitle.replace('<span class="color_2">','')
        scrapedtitle = scrapedtitle.replace('<span class="color_3">','')
        scrapedtitle = scrapedtitle.replace('</span>','')
        scrapedtitle = scrapedtitle.replace('<span class="miniespacio">','')
        scrapedurl = "http://tv.canalextremadura.es%s" % match[1]
        scrapedurl = scrapedurl.replace("#","%")
        scrapedthumbnail = match[0].replace(" ","%20")
        #'\n\t  \n\t\tApenas\xc2\xa0 30 kil\xc3\xb3metros en l\xc3\xadnea recta separan la...\t\t\n\t\t<div>\n\t\td\xc3\xada de emisi\xc3\xb3n_<span class="date-display-single">11Mayo09</span>\t\t')
        #Apenas\xc2\xa0 30 kil\xc3\xb3metros en l\xc3\xadnea recta separan la...\t\t\n\t\t<div>\n\t\td\xc3\xada de emisi\xc3\xb3n_<span class="date-display-single">11Mayo09</span>')
        scrapedplot = match[3].strip()
        scrapedplot = scrapertools.htmlclean(scrapedplot)

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        #addvideo( scrapedtitle , scrapedurl , category )
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , folder=True) )

    return itemlist

def getvideo(item):
    logger.info("[extremaduratv.py] play")

    # --------------------------------------------------------
    # Descarga pagina detalle
    # --------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    patron = 'fluURL\: "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        url = matches[0].replace(' ','%20')
    except:
        url = ""
    logger.info("[extremaduratv.py] play url="+url)
    
    # Construye un plot más completo
    matches = re.compile("<div class=\"view-field view-data-title\">([^<]+)<",re.DOTALL).findall(data)
    descripcion1 = matches[0]
    matches = re.compile("<div class=\"view-field view-data-body\">([^<]+)<",re.DOTALL).findall(data)
    descripcion2 = matches[0]
    matches = re.compile("<div class=\"view-field view-data-created\">([^<]+)<",re.DOTALL).findall(data)
    descripcion3 = matches[0]
    matches = re.compile("<div class=\"view-field view-data-duracion\">([^<]+)<",re.DOTALL).findall(data)
    descripcion4 = matches[0]
    descripcioncompleta = descripcion1[0].strip() + " " + descripcion2[0].strip() + " " + descripcion3[0].strip() + " " + descripcion4[0].strip()
    descripcioncompleta = descripcioncompleta.replace("\t","");
    descripcioncompleta = unicode( descripcioncompleta, "utf-8" ).encode("iso-8859-1")
    plot = descripcioncompleta

    data = scrapertools.cache_page(url)
    print data
    patron = "(http[^\?]+)\?"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    url = matches[0]

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , server="directo" , url=url, thumbnail=item.thumbnail, plot=plot , show=item.show , folder=False) )

    return itemlist