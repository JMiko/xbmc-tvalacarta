# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para RTVE
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse, re

from core import config
from core import logger
from core import scrapertools
from core.item import Item

logger.info("[rtve.py] init")

DEBUG = True
CHANNELNAME = "rtve"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[rtve.py] mainlist")

    itemlist = []
    
    # El primer nivel de menú es un listado por canales
    itemlist.append( Item(channel=CHANNELNAME, title="Todas las cadenas" , action="canal" , thumbnail = "" , url="http://www.rtve.es/alacarta/tve/", extra="tve"))
    itemlist.append( Item(channel=CHANNELNAME, title="La 1"              , action="canal" , thumbnail = "" , url="http://www.rtve.es/alacarta/tve/la1/", extra="la1"))
    itemlist.append( Item(channel=CHANNELNAME, title="La 2"              , action="canal" , thumbnail = "" , url="http://www.rtve.es/alacarta/tve/la2/", extra="la2"))
    itemlist.append( Item(channel=CHANNELNAME, title="Canal 24 horas"    , action="canal" , thumbnail = "" , url="http://www.rtve.es/alacarta/tve/24-horas/", extra="24-horas"))
    itemlist.append( Item(channel=CHANNELNAME, title="Teledeporte"       , action="canal" , thumbnail = "" , url="http://www.rtve.es/alacarta/tve/teledeporte/", extra="teledeporte"))

    return itemlist

def canal(item):
    logger.info("[rtve.py] canal")

    itemlist = []
    # El segundo nivel de menú es un listado por categorías
    itemlist.append( Item(channel=CHANNELNAME, title="Novedades" , action="novedades" , url=item.url , extra=item.extra))
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los programas" , action="programas" , url="" , extra=item.extra+"/todos/1"))

    # Descarga la página que tiene el desplegable de categorias de programas
    url = "http://www.rtve.es/alacarta/programas/tve/todos/1/"
    data = scrapertools.cachePage(url)

    # Extrae las categorias de programas
    patron  = '<li><a title="Seleccionar[^"]+" href="/alacarta/programas/tve/([^/]+)/1/"><span>([^<]+)</span></a></li>'
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    # Crea una lista con las entradas
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[1]
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedextra = match[0]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="programas" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra = item.extra + "/" + scrapedextra + "/1" , category = scrapedtitle ) )
    
    return itemlist

def novedades(item):
    logger.info("[rtve.py] novedades "+item.tostring())

    # Descarga la página principal
    itemlist = []
    data = scrapertools.cachePage(item.url)
    patron = '<!-- programs_series.jsp -->(.*?)<!-- end programs_series.jsp -->'
    matches = re.findall(patron,data,re.DOTALL)
    if len(matches)>0:
        data = matches[0]
    else:
        return itemlist

    # Extrae los vídeos
    patron  = '<div class="basicmod modVideo">[^<]+'
    patron += '<span class="ico">[^<]+</span>[^<]+'
    patron += '<span class="img">[^<]+'
    patron += '<a id="PS." name="thumbID" href="([^"]+)"[^>]+>[^<]+'
    patron += '<img title=\'[^\']+\' alt="[^"]+" src="([^"]+)"/>.*?'
    patron += '</a>[^<]+'
    patron += '</span>[^<]+'
    patron += '<div class="txt">[^<]+'
    patron += '<h4>[^<]+'
    patron += '<span class="titu">[^<]+'
    patron += '<a href="/alacarta/videos[^>]+>([^>]+)</a>[^<]+'
    patron += '</span>[^<]+'
    patron += '</h4>[^<]+'
    patron += '<h5>[^<]+'
    patron += '<span class="titu">[^<]+'
    patron += '<em>[^<]+</em><strong><a title=\'[^\']+\' href="([^"]+)">([^<]+)</a></strong>[^<]+'
    patron += '</span>[^<]+'
    patron += '</h5>[^<]+'
    patron += '<p>([^<]+)</p>'
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)
    
    # Crea una lista con las entradas
    for match in matches:
        scrapedtitle = match[2]+" - "+match[4]+" (Duración "+match[5]+")"
        scrapedurl = urlparse.urljoin(item.url,match[3])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        scrapedplot = ""
        scrapedextra = urlparse.urljoin(item.url,match[0])
        scrapedshow = match[2]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedshow, extra=scrapedextra, folder=False ) )

    # Extrae el enlace a la página siguiente
    #<a name="paginaIR" href="?pbq=2&amp;lang=es&amp;modl=LPG"><span>Siguiente</span></a>

    patron = '<a name="paginaIR" href="([^"]+)"><span>Siguiente</span></a>'
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    # Crea una lista con las entradas
    for match in matches:
        scrapedtitle = "!Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,match).replace("&amp;","&")
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedextra = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="novedades" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra = scrapedextra, category = item.category) )

    return itemlist

def programas(item):
    logger.info("[rtve.py] programas")
    
    # En la paginación la URL vendrá fijada, si no se construye aquí la primera página
    if not item.url.startswith("http"):
        item.url = "http://www.rtve.es/alacarta/programas/"+item.extra+"/?pageSize=100&order=1&criteria=asc&emissionFilter=all"
    logger.info("[rtve.py] programas url="+item.url) 

    itemlist = []
    data = scrapertools.cachePage(item.url)
    itemlist.extend(addprogramas(item,data))
    salir = False

    while not salir:
        # Extrae el enlace a la página siguiente
        patron  = '<a name="paginaIR" href="[^"]+" class="active"><span>[^<]+</span></a>[^<]+'
        patron += '<a name="paginaIR" href="([^"]+)"><span>'
    
        matches = re.findall(patron,data,re.DOTALL)
        if DEBUG: scrapertools.printMatches(matches)

        if len(matches)>0:
            # Carga la página siguiente
            url = urlparse.urljoin(item.url,matches[0]).replace("&amp;","&")
            data = scrapertools.cachePage(url)
            
            # Extrae todos los programas
            itemlist.extend(addprogramas(item,data))
        else:
            salir = True

    return itemlist

def addprogramas(item,data):
    
    itemlist = []
    
    # Extrae los programas
    '''
    <li class="odd">
    <span class="col_tit" id="1589" name="progname">
    <a href="/alacarta/videos/el-escarabajo-verde/" title="Ver programa seleccionado">El escarabajo verde</a>
    </span>
    <span class="col_fec">pasado viernes</span>
    <span class="col_med">
    <a href="/alacarta/tve/la2/" title="Ir a portada de 'La 2'" />
    <img src="/css/alacarta20/i/iconos/mini-cadenas/la2.png"> 
    </a>		
    </span>
    <span class="col_cat">Ciencia y Tecnología</span>
    <!--EMPIEZA TOOL-TIP-->
    <div id="popup1589" style="display: none" class="tultip"> 
    <span id="progToolTip" class="tooltip curved">
    <span class="pointer"></span>
    <span class="cerrar" id="close1589"></span>    
    <span class="titulo-tooltip"><a href="/alacarta/videos/el-escarabajo-verde/" title="Ver programa seleccionado">El escarabajo verde</a></span>
    <span class="fecha">pasado viernes</span>
    <span class="detalle">Magazine sobre ecología y medio ambiente, que se centra en las relaciones que el hombre establece con su entorno. Desde una perspectiva divulgativa, el programa analiza un tema de actualidad del medio ambiente y ...</span>
    '''
    patron  = '<li class="[^"]+">.*?'
    patron += '<span class="col_tit" id="([^"]+)" name="progname">[^<]+'
    patron += '<a href="([^"]+)" title="Ver programa seleccionado">([^<]+)</a>[^<]+'
    patron += '</span>[^<]+'
    patron += '<span class="col_fec">([^<]+)</span>.*?'
    patron += '<span class="col_cat">([^<]*)</span>'
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    # Crea una lista con las entradas
    for match in matches:
        if config.get_setting("rtve.programa.extendido")=="true":
            scrapedtitle = match[2]+" (Ult. emisión "+match[3]+") ("+match[4]+")"
        else:
            scrapedtitle = match[2]
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = ""
        scrapedplot = ""#match[5]
        scrapedextra = match[0]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra = scrapedextra, show=scrapedtitle, category = item.category) )

    return itemlist

def detalle_programa(item):
    
    data = scrapertools.cache_page(item.url)
    
    # Extrae plot
    patron  = '<p class="intro">(.*?)</div>'
    matches = re.findall(patron, data, re.DOTALL)
    if len(matches)>0:
        item.plot = scrapertools.htmlclean( matches[0] ).strip()

    # Extrae thumbnail
    patron  = '<span class="imgPrograma">.*?'
    patron += '<img title="[^"]+" alt="[^"]+" src="([^"]+)" />'
    matches = re.findall(patron, data, re.DOTALL)
    if len(matches)>0:
        item.thumbnail = urlparse.urljoin(item.url,matches[0])
    
    # Extrae title
    patron  = '<div class="false_cab">[^<]+'
    patron += '<h2>[^<]+'
    patron += '<a[^>]+>[^<]+'
    patron += '<span>([^<]+)</span>'
    matches = re.findall(patron, data, re.DOTALL)
    if len(matches)>0:
        item.title = matches[0].strip()
    
    return item

def episodios(item):
    logger.info("[rtve.py] episodios")

    # En la paginación la URL vendrá fijada, si no se construye aquí la primera página
    if item.url=="":
        # El ID del programa está en item.extra (ej: 42610)
        # La URL de los vídeos de un programa es
        # http://www.rtve.es/alacarta/interno/contenttable.shtml?ctx=42610&pageSize=20&pbq=1
        item.url = "http://www.rtve.es/alacarta/interno/contenttable.shtml?ctx="+item.extra+"&pageSize=20&pbq=1"
    data = scrapertools.cachePage(item.url)

    itemlist = []

    # Extrae los vídeos
    patron  = '<li class="[^"]+">.*?'
    patron += '<span class="col_tit"[^>]+>[^<]+'
    patron += '<a href="([^"]+)">(.*?)</a>[^<]+'
    patron += '</span>[^<]+'
    patron += '<span class="col_tip">([^<]+)</span>[^<]+'
    patron += '<span class="col_dur">([^<]+)</span>.*?'
    patron += '<span class="col_fec">([^<]+)</span>.*?'
    patron += '<span class="detalle">([^>]+)</span>'
    
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    # Crea una lista con las entradas
    for match in matches:
        if not "developer" in config.get_platform():
            scrapedtitle = match[1]+" ("+match[2].strip()+") ("+match[3].strip()+") ("+match[4]+")"
        else:
            scrapedtitle = match[1]
        scrapedtitle = scrapedtitle.replace("<em>Nuevo</em>&nbsp;","")
        scrapedtitle = scrapertools.unescape(scrapedtitle)
        scrapedtitle = scrapedtitle.strip()
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        scrapedplot = scrapertools.unescape(match[5].strip())
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()
        scrapedextra = match[2]
        
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="rtve" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show, category = item.category, extra=scrapedextra, folder=False) )

    # Extrae la paginación
    patron = '<a name="paginaIR" href="([^"]+)"><span>Siguiente</span></a>'
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    # Crea una lista con las entradas
    for match in matches:
        scrapedtitle = "!Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,match).replace("&amp;","&")
        #http://www.rtve.es/alacarta/interno/contenttable.shtml?pbq=2&modl=TOC&locale=es&pageSize=15&ctx=36850&advSearchOpen=false
        if not scrapedurl.endswith("&advSearchOpen=false"):
            scrapedurl = scrapedurl + "&advSearchOpen=false"
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedextra = item.extra
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra = scrapedextra, category = item.category, show=item.show) )

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title=">> Añadir toda la página a la lista de descargas", url=item.url, action="download_all_episodes##episodios", extra = item.extra , show=item.show) )

    return itemlist
