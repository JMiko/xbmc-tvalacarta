# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para RTVA
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item 

logger.info("[rtva.py] init")

DEBUG = False
CHANNELNAME = "rtva"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtva.py] mainlist")

    url = "http://www.radiotelevisionandalucia.es/tvcarta/impe/web/portada"
    itemlist = []

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae los programas
    # --------------------------------------------------------
    patron = '<div class="infoPrograma"><h3 class="h3TituloProgramaCarta"><a href="([^"]+)" title="[^"]+">([^<]+)</a></h3><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div><div class="enlacePrograma"><a href="[^"]+" title="[^"]+"><img class="imgLista" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    dictionaryurl = {}

    for match in matches:
        titulo = match[1].replace("á","Á")
        titulo = titulo.replace("é","É")
        titulo = titulo.replace("í","Í")
        titulo = titulo.replace("ó","Ó")
        titulo = titulo.replace("ú","Ú")
        titulo = titulo.replace("ñ","Ñ")
        titulo = titulo.replace('&Aacute;','Á')
        titulo = titulo.replace('&Eacute;','É')
        titulo = titulo.replace('&Iacute;','Í')
        titulo = titulo.replace('&Oacute;','Ó')
        titulo = titulo.replace('&Uacute;','Ú')
        titulo = titulo.replace('&ntilde;','ñ')
        titulo = titulo.replace('&Ntilde;','Ñ')
        scrapedtitle = titulo
        scrapedurl = 'http://www.radiotelevisionandalucia.es/tvcarta/impe/web/portada'
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        if dictionaryurl.has_key(scrapedtitle):
            if DEBUG: logger.info("%s ya existe" % scrapedtitle)
        else:
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , folder=True) )
            dictionaryurl[scrapedtitle] = True

    return itemlist

def videolist(item):
    logger.info("[rtva.py] videolist")

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae los programas
    # --------------------------------------------------------
    patron  = '<div class="infoPrograma"><h3 class="h3TituloProgramaCarta"><a href="([^"]+)" title="[^"]+">([^<]+)</a></h3><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div><div class="enlacePrograma"><a href="[^"]+" title="[^"]+"><img class="imgLista" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Datos
        titulo = match[1].replace("á","Á")
        titulo = titulo.replace("é","É")
        titulo = titulo.replace("í","Í")
        titulo = titulo.replace("ó","Ó")
        titulo = titulo.replace("ú","Ú")
        titulo = titulo.replace("ñ","Ñ")
        titulo = titulo.replace('&Aacute;','Á')
        titulo = titulo.replace('&Eacute;','É')
        titulo = titulo.replace('&Iacute;','Í')
        titulo = titulo.replace('&Oacute;','Ó')
        titulo = titulo.replace('&Uacute;','Ú')
        titulo = titulo.replace('&ntilde;','ñ')
        titulo = titulo.replace('&Ntilde;','Ñ')
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url, match[0])
        scrapedthumbnail = match[6].replace(' ','%20')
        titulocapitulo =  ( "%s %s %s %s" % (match[2],match[3],match[4],match[5]))
        titulocapitulo = titulocapitulo.replace('&Aacute;','Á')
        titulocapitulo = titulocapitulo.replace('&Eacute;','É')
        titulocapitulo = titulocapitulo.replace('&Iacute;','Í')
        titulocapitulo = titulocapitulo.replace('&Oacute;','Ó')
        titulocapitulo = titulocapitulo.replace('&Uacute;','Ú')
        titulocapitulo = titulocapitulo.replace('&ntilde;','ñ')
        titulocapitulo = titulocapitulo.replace('&Ntilde;','Ñ')
        titulocapitulo = titulocapitulo.replace('&aacute;','á')
        titulocapitulo = titulocapitulo.replace('&eacute;','é')
        titulocapitulo = titulocapitulo.replace('&iacute;','í')
        titulocapitulo = titulocapitulo.replace('&oacute;','ó')
        titulocapitulo = titulocapitulo.replace('&uacute;','ú')
        scrapedplot = titulocapitulo

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        if scrapedtitle == item.title:
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle + " " + scrapedplot , action="getvideo" , url=scrapedurl, page = scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , folder=True) )

    return itemlist

def getvideo(item):
    logger.info("[rtva.py] getvideo")

    # --------------------------------------------------------
    # Descarga pagina detalle
    # --------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    patron = '<param name="flashvars" value="&amp;video=(http://[^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        url = matches[0].replace(' ','%20')
    except:
        url = ""
    logger.info("[rtva.py] url="+url)
    if url.find("&") != -1:
        url = url.split("&")[0]
        logger.info("[rtva.py] url="+url)

    # --------------------------------------------------------
    # Argumento detallado
    # --------------------------------------------------------
    patron = '<div class="zonaContenido"><p>([^<]+)</p>(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?(?:<p>([^<]+)</p>)?</div>'
    argumento = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(argumento)
    argumentofull = ""
    if len(argumento) > 0:
        if len(argumento[0]) >= 4:
            argumentofull = ("%s\n%s\n%s\n%s\n%s" % (item.title , argumento[0][0] , argumento[0][1] , argumento[0][2] , argumento[0][3] ))
        elif len(argumento[0]) >= 3:
            argumentofull = ("%s\n%s\n%s\n%s" % (item.title , argumento[0][0] , argumento[0][1] , argumento[0][2] ))
        elif len(argumento[0]) >= 2:
            argumentofull = ("%s\n%s\n%s" % (item.title , argumento[0][0] , argumento[0][1] ))
        elif len(argumento[0]) >= 1:
            argumentofull = ("%s\n%s" % (item.title , argumento[0][0] ))
    #argumentofull = ("%s\n%s" % (.description , argumento[0][0] ))
    plot = scrapertools.entityunescape(argumentofull)

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Ver el vídeo" , action="play" , server="directo" , url=url, thumbnail=item.thumbnail, plot=plot , show=item.show , folder=False) )

    return itemlist