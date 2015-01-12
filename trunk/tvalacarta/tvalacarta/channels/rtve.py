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
    itemlist.append( Item(channel=CHANNELNAME, title="Destacados" , action="destacados" , url=item.url , extra=item.extra))
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

def destacados(item):
    logger.info("[rtve.py] destacados")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    '''
    <div class="dest_title">Destacados versi&iquest;n libre</div>
    <div class="dest_page oculto">        <div  bourne:iseditable="false" class="unit c100 last">            <div  class="unit c100 last"><div class="mark">
    <div class="news  comp">
    <span class="tipo video">v&iacute;deo</span><span class="imgT"><a href="/alacarta/videos/informe-semanal/informe-semanal-soberanismo-suspenso/1814688/" title="Informe Semanal - Soberanismo en suspenso"><img src="http://img.irtve.es/imagenes/jpg/1368305081366.jpg" alt="Imagen Informe Semanal - Soberanismo en suspenso" title="Informe Semanal - Soberanismo en suspenso"/></a></span>
    </div>
    </div>
    </div>          </div>      </div>        <div class="dest_title">Destacados versi&iquest;n libre</div>    <div class="dest_page oculto">        <div  bourne:iseditable="false" class="unit c100 last">            <div  class="unit c100 last">              <div class="mark"><div class="news  comp"><span class="tipo video">v&iacute;deo</span><span class="imgT"><a href="/alacarta/videos/completos/cuentame-cap-251-150313/1768614/" title="Cu&eacute;ntame c&oacute;mo pas&oacute; - T14 - No hay cuento de Navidad - C
    '''
    logger.info("data="+data)
    patron  = '<div class="dest_title[^<]+</div[^<]+'
    patron += '<div class="dest_page oculto"[^<]+<div[^<]+<div[^<]+<div[^<]+'
    patron += '<div class="news[^<]+'
    patron += '<span class="tipo.*?</span><span class="imgT"><a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'

    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        url=urlparse.urljoin(item.url,scrapedurl)
        title=scrapertools.htmlclean(scrapedtitle)
        thumbnail=scrapedthumbnail
        thumbnail = thumbnail.replace("&amp;","&")
        plot=""

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        try:
            logger.info("url="+url)

            #http://www.rtve.es/alacarta/videos/cocina-con-sergio/cocina-sergio-quiche-cebolla-queso-curado/1814210/
            episodio = scrapertools.get_match(url,'http\://www.rtve.es/alacarta/videos/[^\/]+/([^\/]+)/')
            logger.info("es episodio")
            itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , server="rtve" , url=url, thumbnail=thumbnail, plot=plot, fanart=thumbnail, folder=False) )
        except:
            logger.info("es serie")
            itemlist.append( Item(channel=CHANNELNAME, title=title , action="episodios" , url=url, thumbnail=thumbnail, plot=plot, fanart=thumbnail, folder=True) )

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
    '''
    <li class="odd">
    <span class="col_tit" id="2851919" name="progname">
    <a href="/alacarta/videos/atencion-obras/atencion-obras-josep-maria-flotats-ferran-adria-sanchis-sinisterra/2851919/">Atención Obras - 07/11/14</a>
    </span>
    <span class="col_tip">
    <span>Completo</span>
    </span>
    <span class="col_dur">55:35</span>
    <span class="col_pop"><span title="32% popularidad" class="pc32"><em><strong><span>32%</span></strong></em></span></span>
    <span class="col_fec">07 nov 2014</span>

    <div id="popup2851919" class="tultip hddn"> 
    <span id="progToolTip" class="tooltip curved">
    <span class="pointer"></span>
    <span class="cerrar" id="close2851919"></span>
    <span class="titulo-tooltip"><a href="/alacarta/videos/atencion-obras/atencion-obras-josep-maria-flotats-ferran-adria-sanchis-sinisterra/2851919/" title="Ver Atención Obras - 07/11/14">Atención Obras - 07/11/14</a></span>
    <span class="fecha">07 nov 2014</span>
    <span class="detalle">Josep María Flotats&#160;trae al Teatro María Guerrero de Madrid&#160;&#8220;El juego del amor y del azar&#8221;&#160;de Pierre de Marivaux. Un texto que ya ha sido estrenado en el Teatre Nacional de Catalunya. C...</span>
    '''
    patron  = '<li class="[^"]+">.*?'
    patron += '<span class="col_tit"[^<]+'
    patron += '<a href="([^"]+)">(.*?)</a[^<]+'
    patron += '</span>[^<]+'
    patron += '<span class="col_tip"[^<]+<span>([^<]+)</span[^<]+</span[^<]+'
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

    if len(itemlist)>0:
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

        if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
            itemlist.append( Item(channel=item.channel, title=">> Opciones para esta serie", url=item.url, action="serie_options##episodios", thumbnail=item.thumbnail, extra = item.extra , show=item.show, folder=False))

    else:

        # Extrae los vídeos
        patron  = '<div class="mark"[^<]+'
        patron += '<a href="([^"]+)" title="([^"]+)"[^<]+'
        patron += '<span class="[^<]+'
        patron += '<img src="([^"]+)".*?'
        patron += '<div class="apiCall summary"[^<]+'
        patron += '<p[^<]+'
        patron += '<span class="time">([^<]+)</span[^<]+'
        patron += '<span class="date">([^<]+)</span>([^<]+)<'
        
        matches = re.findall(patron,data,re.DOTALL)
        if DEBUG: scrapertools.printMatches(matches)

        # Crea una lista con las entradas
        for scrapedurl,scrapedtitle,scrapedthumbnail,duracion,fecha,plot in matches:
            title = scrapedtitle+" ("+duracion+")("+fecha+")"
            url = urlparse.urljoin(item.url,scrapedurl)
            plot = plot
            thumbnail = scrapedthumbnail
            
            if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
            itemlist.append( Item(channel=CHANNELNAME, title=title , action="play" , server="rtve" , url=url, thumbnail=thumbnail, plot=plot , show=item.show, category = item.category, fanart=thumbnail, viewmode="movie_with_plot", folder=False) )

        if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
            itemlist.append( Item(channel=item.channel, title=">> Opciones para esta serie", url=item.url, action="serie_options##episodios", thumbnail=item.thumbnail, extra = item.extra , show=item.show, folder=False))

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():

    # Todas las opciones tienen que tener algo
    items = mainlist(Item())

    # Lista de series
    la1_items = canal(items[1])

    la1_destacados = destacados(la1_items[0])
    if len(la1_destacados)==0:
        print "No hay destacados de La1"
        return False

    la1_programas = programas(la1_items[1])
    if len(la1_programas)==0:
        print "No programas en La1"
        return False

    la1_episodios = episodios(la1_programas[0])
    if len(la1_episodios)==0:
        print "La serie "+la1_programas[0].title+" no tiene episodios en La1"
        return False

    return True
