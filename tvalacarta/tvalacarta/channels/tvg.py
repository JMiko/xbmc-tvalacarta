# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para TVG
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item 

DEBUG = False
CHANNELNAME = "tvg"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tvg.py] mainlist")
    itemlist=[]
    itemlist.append( Item(channel=CHANNELNAME, title="Últimos"     , action="novedades"  , url="http://www.crtvg.es/tvg/a-carta"))
    itemlist.append( Item(channel=CHANNELNAME, title="Do A ao Z"   , action="programas"  , url="http://www.crtvg.es/tvg/a-carta"))
    itemlist.append( Item(channel=CHANNELNAME, title="Categorías"  , action="categorias" , url="http://www.crtvg.es/tvg/a-carta"))
    return itemlist

def novedades(item):
    logger.info("[tvg.py] novedades")
    itemlist = []

    # Lee la página del programa
    data = scrapertools.cache_page(item.url)
    # Descarga la página
    logger.info("data="+data)
    data = data.replace("\\","")

    # Extrae los videos
    '''
    <li id="programa-584354" class="listadoimagenes-li">
    <div id="imagen-programa-584354" class="listadoimagenes-imagen">
    <a href="/tvg/a-carta/telexornal-mediodia-fds-584354"
    title="Telexornal Mediodía FDS">
    <img src="/files/thumbs/tx1.jpg" alt="Telexornal Mediodía FDS" width="175" height="100"/>
    </a>
    </div>
    <div id="info-programa-584354" class="listadoimagenes-info">
    <div id="titulo-programa-584354"class="listadoimagenes-titulo">
    <a href="/tvg/a-carta/telexornal-mediodia-fds-584354"
    title="Telexornal Mediodía FDS">
    Telexornal Mediodía FDS - Telexornal Mediodía FDS
    </a>
    </div>
    <div id="data-programa-584354" class="listadoimagenes-data">
    11/05/2013
    </div>
    </div>
    </li>
    '''
    patron  = '<li id="programa-[^<]+'
    patron += '<div id="imagen-programa-[^<]+'
    patron += '<a href="([^"]+)"\s+title="([^"]+)"[^<]+'
    patron += '<img src="([^"]+)".*?'
    patron += '<div id="data-programa-[^"]+" class="listadoimagenes-data">(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()+" "+match[3].strip()
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="tvg", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=False) )

    return itemlist

def categorias(item):
    logger.info("[tvg.py] categorias")
    itemlist=[]
    
    # Extrae los programas
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,"<!-- LISTADO POR CAT(.*?)</ul>")
    
    '''
    <div class="item-a-carta titulo-a-carta">
    <h3>
    Series												</h3>
    </div>
    '''
    '''
    <div class="item-a-carta">
    <a href="/tvg/a-carta/programa/15-zona-cerco-aos-matalobos"
    title="15 Zona: cerco aos Matalobos">
    15 Zona: cerco aos Matalobos
    </a>
    </div>
    '''
    patron = '<div class="item-a-carta(.*?)</div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for bloque in matches:
        if "<h3>" in bloque:
            scrapedtitle = "[COLOR blue]"+scrapertools.get_match(bloque,"<h3>([^<]+)</h3>").strip().upper()+"[/COLOR]"
            scrapedurl=""
            folder=False
        else:
            scrapedtitle = "  "+scrapertools.get_match(bloque,'<a href="[^"]+"[^>]+>([^<]+)<').strip()
            scrapedurl = urlparse.urljoin(item.url,scrapertools.get_match(bloque,'<a href="([^"]+)"[^>]+>[^<]+<').strip())
            folder=True

        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, page=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , category = item.category , folder=folder) )

    return itemlist

def programas(item):
    logger.info("[tvg.py] programas")
    itemlist=[]
    
    # Extrae los programas
    data = scrapertools.cachePage(item.url)
    #logger.info("data="+data)

    data = scrapertools.get_match(data,"<!-- LISTADO DE LA A A LA Z -->(.*?)<!-- LISTADO POR CAT")
    
    '''
    <div class="item-a-carta">
    <a href="/tvg/a-carta/programa/15-zona-cerco-aos-matalobos"
    title="15 Zona: cerco aos Matalobos">
    15 Zona: cerco aos Matalobos
    </a>
    </div>
    '''
    
    patron  = '<div class="item-a-carta"[^<]+'
    patron += '<a href="([^"]+)"[^>]+>([^<]+)<'
                                                
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    for url,title in matches:
        scrapedtitle = title.strip()
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, page=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , category = item.category , folder=True) )

    return itemlist

def episodios(item):
    logger.info("[tvg.py] episodios")
    itemlist = []

    # Lee la página del programa y extrae el id_programa
    if "/ax/" in item.url:
        headers=[]
        headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0"])
        headers.append(["X-Requested-With","XMLHttpRequest"])
        headers.append(["Referer",item.url])
        data = scrapertools.cache_page(item.url, post="", headers=headers)
        data = data.replace("\\n"," ")
        data = data.replace("\\","")
    else:
        data = scrapertools.cache_page(item.url)
        try:
            id_programa = scrapertools.get_match(data,"initAlaCartaBuscador.(\d+)")
        except:
            id_programa = ""
        
        # Lee la primera página de episodios
        #http://www.crtvg.es/ax/tvgalacartabuscador/programa:33517/pagina:1/seccion:294/titulo:/mes:null/ano:null/temporada:null
        logger.info("[tvg.py] videos - hay programa")
        url = "http://www.crtvg.es/ax/tvgalacartabuscador/programa:"+id_programa+"/pagina:1/seccion:294/titulo:/mes:null/ano:null/temporada:null"
        headers=[]
        headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0"])
        headers.append(["X-Requested-With","XMLHttpRequest"])
        headers.append(["Referer",item.url])
        data = scrapertools.cache_page(url, post="", headers=headers)
        data = data.replace("\\n"," ")
        data = data.replace("\\","")
    logger.info("data="+data)

    # Extrae los videos
    #<tr>                  <td class="a-carta-resultado-imagen">                      <a href="/tvg/a-carta/a-revista-fds-477893"                           title="A Revista FDS">
    #<img src="/files/thumbs/LorenaPose.jpg" alt="A Revista FDS" width="75" height="42"/>                      </a>                                              </td>                  <td class="a-carta-resultado-titulo">                      <a href="/tvg/a-carta/a-revista-fds-477893" title="A Revista FDS">A Revista FDS</a>                 </td>                                     <td class="a-carta-resultado-data">                  02/12/2012 12:10                 </td>                              </tr>
    patron  = '<tr[^<]+<td class="a-carta-resultado-imagen[^<]+'
    patron += '<a href="([^"]+)"\s+title="([^"]+)"[^<]+<img src="([^"]+)".*?'
    patron += '<td class="a-carta-resultado-data">(.*?)</td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()+" "+match[3].strip()
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , server="tvg", url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=False) )

    #<a href=\"#\" title=\"Seguinte\" onclick=\"return posteriorpaginaclick(33517, 2, 294)
    patron  = '<a href="\#" title="Seguinte" onclick="return posteriorpaginaclick\((\d+), (\d+), (\d+)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">>> Página siguiente"
        #http://www.crtvg.es/ax/tvgalacartabuscador/programa:33517/pagina:2/seccion:294/titulo:/mes:null/ano:null/temporada:null
        scrapedurl = "http://www.crtvg.es/ax/tvgalacartabuscador/programa:%s/pagina:%s/seccion:%s/titulo:/mes:null/ano:null/temporada:null" % (match[0],match[1],match[2])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    
    # Menu
    mainlist_items = mainlist(Item())

    # Novedades
    novedades_items = novedades(mainlist_items[0])
    if len(novedades_items)==0:
        return False

    # Categorías
    categorias_items = categorias(mainlist_items[2])
    if len(categorias_items)==0:
        return False

    # Todos los programas
    programas_items = programas(mainlist_items[1])
    if len(programas_items)==0:
        return False

    for programa_item in programas_items:
        episodios_items = episodios(programas_items[0])
        if len(episodios_items)>0:
            return True

    return False
