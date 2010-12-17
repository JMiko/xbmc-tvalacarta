# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para programas de RTVE
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse, re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[rtveprogramas.py] init")

DEBUG = True
CHANNELNAME = "rtveprogramas"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtveprogramas.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Españoles en el mundo" , action="espanoles"  , url="http://www.rtve.es/television/espanoles-en-el-mundo/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Águila roja"           , action="aguilaroja" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Así se hizo"           , action="generico"   , url="http://www.rtve.es/television/asi-se-hizo/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Días de cine"          , action="generico"   , url="http://www.rtve.es/television/dias-cine-programas/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="La señora"             , action="lasenora"   , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Guante blanco"         , action="generico"   , url="http://www.rtve.es/television/guanteblanco/capitulos-guante-blanco/" , extra="allowblanktitles", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Tres 14"               , action="generico"   , url="http://www.rtve.es/television/tres14/" , folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Redes"                 , action="generico"   , url="http://www.rtve.es/television/redes/archivo/" , folder=True) )
    #itemlist.append( Item(channel=CHANNELNAME, title="Un país para comérselo", action="generico"   , url="http://www.rtve.es/television/un-pais-para-comerselo/itinerario/" , folder=True) )

    return itemlist

def espanoles(item):
    logger.info("[rtveprogramas.py] espanoles")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las categorias (carpetas)
    #<div class="mark"><div class="news bg01   comp"><span class="imgL"><a href="http://www.rtve.es/television/espanoles-en-el-mundo/camerun/" title="Destino#46 Camerún"><img src="/imagenes/destino46-camerun/1267557505140.jpg" alt="Destino#46 Camerún" title="Destino#46 Camerún"/></a></span><h3 class="M "><a href="http://www.rtve.es/television/espanoles-en-el-mundo/camerun/" title="Destino#46 Camerún">Destino#46 Camerún</a></h3><div class="chapeaux">Este destino es mucho más que un país... es todo un continente. <strong>Vuelve a verlo</strong>.</div></div></div>
    #<div class="mark"><div class="news bg01   comp"><span class="imgT"><a href="http://www.rtve.es/television/espanoles-en-el-mundo/jalisco/" title="Destino#42 Jalisco (México)"><img src="/imagenes/destino42-jalisco-mexico/1264699947886.jpg" alt="Destino#42 Jalisco (México)" title="Destino#42 Jalisco (México)"/></a></span><h3 class="M "><a href="http://www.rtve.es/television/espanoles-en-el-mundo/jalisco/" title="Destino#42 Jalisco (México)">Destino#42 Jalisco (México)</a></h3><div class="chapeaux">¿Sabías que hay mariachis de chicas? ¿De dónde viene el tequila? <strong>Vuelve a verlo</strong>.</div></div></div><div class="mark"><div class="
    patron  = '<div class="mark"><div class="news bg01   comp"><span class="img."><a href="([^"]+)" title="([^"]+)"><img src="([^"]+)" alt="[^"]+" title="[^"]+"/></a></span><h. class=". "><a href="[^"]+" title="[^"]+">([^<]+)</a></h.><div class="chapeaux">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Datos
        scrapedtitle = scrapertools.entityunescape(match[3])
        scrapedurl = urlparse.urljoin(item.url, match[0])
        scrapedthumbnail = urlparse.urljoin(item.url, match[2])
        scrapedplot = match[4]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="generico" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.title , folder=True) )

    # Descarga la página
    url = "http://www.rtve.es/television/espanoles-en-el-mundo/programas-anteriores/"
    data = scrapertools.cachePage(url)
    #logger.info(data)

    # Extrae las categorias (carpetas)
    #<div class="news bg01   comp"><span class="imgT"><a href="http://www.rtve.es/television/espanoles-en-el-mundo/seul/" title="Destino#28 Seúl">
    #<img src="/imagenes/destino28-seul/1264701360856.jpg" alt="Destino#28 Seúl" title="Destino#28 Seúl"/></a></span>
    #<h3 class="M "><a href="http://www.rtve.es/television/espanoles-en-el-mundo/seul/" title="Destino#28 Seúl">Destino#28 Seúl</a></h3><div class="chapeaux"> Viajamos a la capital de Corea del Sur, la segunda urbe más poblada del planeta.<strong> Vuelve a verlo</strong></div>
    patron  = '<div class="news bg01   comp">[^<]*'
    patron += '<span class="img."><a href="([^"]+)" title="[^"]+"><img src="([^"]+)" alt="[^"]+" title="[^"]+"/></a></span>[^<]*'
    patron += '<h. class=". ">[^<]*'
    patron += '<a href="[^"]+" title="([^"]+)">([^<]+)</a>[^<]*'
    patron += '</h.>[^<]*'
    patron += '<div class="chapeaux">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        # Datos
        scrapedtitle = scrapertools.entityunescape(match[3])
        scrapedurl = urlparse.urljoin(url, match[0])
        scrapedthumbnail = urlparse.urljoin(url, match[1])
        scrapedplot = match[4]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="generico" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.title , folder=True) )

    return itemlist

def aguilaroja(item):
    logger.info("[rtveprogramas.py] mainlist")
    itemlist = []
    
    itemlist.append( Item(channel=CHANNELNAME, title="Temporada 1" , action="generico"  , url="http://www.rtve.es/television/aguila-roja/capitulos-completos/primera-temporada/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Temporada 2" , action="generico"  , url="http://www.rtve.es/television/aguila-roja/capitulos-completos/segunda-temporada/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Temporada 3" , action="generico"  , url="http://www.rtve.es/television/aguila-roja/capitulos-completos/tercera-temporada/", folder=True) )

    return itemlist

def lasenora(item):
    logger.info("[rtveprogramas.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Temporada 1" , action="generico"  , url="http://www.rtve.es/television/la-senora/capitulos-completos/primera-temporada/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Temporada 2" , action="generico"  , url="http://www.rtve.es/television/la-senora/capitulos-completos/segunda-temporada/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Temporada 3" , action="generico"  , url="http://www.rtve.es/television/la-senora/capitulos-completos/tercera-temporada/", folder=True) )
    
    return itemlist

def generico(item):
    logger.info("[rtveprogramas.py] generico")
    itemlist = []
    
    # El parametro allowblanks permite que haya vídeos sin título
    allowblanktitles = False
    if item.extra=="allowblanktitles":
        allowblanktitles = True

    # --------------------------------------------------------
    # Descarga la página
    # --------------------------------------------------------
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # --------------------------------------------------------
    # Extrae las categorias (carpetas)
    # --------------------------------------------------------
    patron  = '<div class="news[^"]+">(.*?</div>)'
    bloques = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(bloques)

    for bloque in bloques:
        '''
        ##############################################################################################################    
        <span class="imgL"><a href="/mediateca/videos/20100225/aguila-roja-cap21/705225.shtml" title=""><img src="/imagenes/jpg/1267703487420.jpg" alt="" title=""/></a></span>
        <h3 class="M ">
        <a href="/mediateca/videos/20100225/aguila-roja-cap21/705225.shtml" title="Capítulo 21">Capítulo 21</a>
        </h3>
        <div class="chapeaux">Emitido el 25/02/10</div>
        ##############################################################################################################    
        <span class="imgL"><a href="/mediateca/videos/20100218/aguila-roja-cap20/698541.shtml" title="Capítulo 20"><img src="/imagenes/capitulo-20/1267703445964.jpg" alt="Capítulo 20" title="Capítulo 20"/></a></span>
        <h3 class="M ">
        <a href="/mediateca/videos/20100218/aguila-roja-cap20/698541.shtml" title="Capítulo 20">Capítulo 20</a>
        </h3>
        <div class="chapeaux">Emitido el 18/02/10</div>
        ##############################################################################################################    
        '''
        scrapedtitle = ""
        scrapedurl = ""
        scrapedthumbnail = ""
        scrapedplot = ""

        # Enlace a la página y título
        patron = '<a href="([^"]+)"[^>]+>([^<]+)<'
        matches = re.compile(patron,re.DOTALL).findall(bloque)
        if DEBUG: scrapertools.printMatches(matches)
        if len(matches)>0:
            scrapedurl = urlparse.urljoin(item.url, matches[0][0])
            scrapedtitle = scrapertools.entityunescape(matches[0][1])
        
        # Si no tiene titulo busca el primer enlace que haya
        if scrapedurl=="":
            # Enlace a la página y título
            patron = '<a href="([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(bloque)
            if DEBUG: scrapertools.printMatches(matches)
            if len(matches)>0:
                scrapedurl = urlparse.urljoin(item.url, matches[0])

        # Thumbnail
        patron = '<img src="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(bloque)
        if DEBUG: scrapertools.printMatches(matches)
        if len(matches)>0:
            scrapedthumbnail = urlparse.urljoin(item.url, matches[0])

        # Argumento
        patron = '<div class="chapeaux">(.*?)</div>'
        matches = re.compile(patron,re.DOTALL).findall(bloque)
        if DEBUG: scrapertools.printMatches(matches)
        if len(matches)>0:
            scrapedplot = scrapertools.htmlclean(matches[0])

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        
        if allowblanktitles:
            titulos = scrapedurl.split("/")
            scrapedtitle = titulos[ len(titulos)-2 ]

        # Añade al listado de XBMC
        if scrapedtitle<>"" and scrapedurl<>"":
            patron = 'http://.*?/([0-9]+).shtml'
            matches = re.compile(patron,re.DOTALL).findall(scrapedurl)
            if len(matches)>0:
                itemlist.append( Item(channel="rtve", title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail , plot=scrapedplot , server = "directo" , show = item.title , folder=True) )
            else:
                itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="generico" , url=scrapedurl, thumbnail=scrapedthumbnail , plot=scrapedplot , show = item.title , folder=True) )

    return itemlist