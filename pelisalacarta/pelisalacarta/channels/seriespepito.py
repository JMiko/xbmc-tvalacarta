# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriespepito
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "seriespepito"
__category__ = "S"
__type__ = "generic"
__title__ = "Seriespepito"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriespepito.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="listalfabetico"   , title="Listado alfabético"))
    itemlist.append( Item(channel=__channel__, action="allserieslist"    , title="Listado completo",    url="http://www.seriespepito.com/"))

    return itemlist

def allserieslist(item):
    logger.info("[seriespepito.py] allserieslist")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron = "<li><a href='([^']+)'>([^<]+)</a></li>"

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Ajusta el encoding a UTF-8
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")

        itemlist.append( Item(channel=__channel__, action="episodelist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def listalfabetico(item):
    logger.info("[seriespepito.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="0-9",url="http://www.seriespepito.com/lista-series-num/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="A",url="http://www.seriespepito.com/lista-series-a/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="B",url="http://www.seriespepito.com/lista-series-b/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="C",url="http://www.seriespepito.com/lista-series-c/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="D",url="http://www.seriespepito.com/lista-series-d/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="E",url="http://www.seriespepito.com/lista-series-e/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="F",url="http://www.seriespepito.com/lista-series-f/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="G",url="http://www.seriespepito.com/lista-series-g/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="H",url="http://www.seriespepito.com/lista-series-h/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="I",url="http://www.seriespepito.com/lista-series-i/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="J",url="http://www.seriespepito.com/lista-series-j/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="K",url="http://www.seriespepito.com/lista-series-k/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="L",url="http://www.seriespepito.com/lista-series-l/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="M",url="http://www.seriespepito.com/lista-series-m/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="N",url="http://www.seriespepito.com/lista-series-n/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="O",url="http://www.seriespepito.com/lista-series-o/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="P",url="http://www.seriespepito.com/lista-series-p/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="Q",url="http://www.seriespepito.com/lista-series-q/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="R",url="http://www.seriespepito.com/lista-series-r/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="S",url="http://www.seriespepito.com/lista-series-s/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="T",url="http://www.seriespepito.com/lista-series-t/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="U",url="http://www.seriespepito.com/lista-series-u/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="V",url="http://www.seriespepito.com/lista-series-v/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="W",url="http://www.seriespepito.com/lista-series-w/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="X",url="http://www.seriespepito.com/lista-series-x/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="Y",url="http://www.seriespepito.com/lista-series-y/"))
    itemlist.append( Item(channel=__channel__, action="alphaserieslist" , title="Z",url="http://www.seriespepito.com/lista-series-z/"))

    return itemlist

def alphaserieslist(item):
    logger.info("[seriespepito.py] alphaserieslist")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    '''
    <div class='lista-series'>    
    <div class="imagen">
    <a href="http://abducidos.seriespepito.com" title="Abducidos online">
    <img src='http://www.midatacenter.com/seriespepito/imagenes-serie/abducidos498.jpg' width='90' height='124' border='0' alt='Abducidos online'   />                  </a>
    </div>
    <div class="nombre">
    <a href="http://abducidos.seriespepito.com" title="Abducidos online">Abducidos</a>
    </div>
    <div class="sinopsis">
    Abducidos es una Mini-Serie Estadounidense que consta de 10 capítulos, los cuales los podrás ver online o descargar en SeriesPepito.
    Es una miniserie de ciencia ficción emitida por primera vez en el ...                  </div>
    <div class="enlace">
    '''
    patron  = "<div class='lista-series'>[^<]+"
    patron += '<div class="imagen">[^<]+'
    patron += '<a href="([^"]+)"[^<]+'
    patron += "<img src='([^']+)'[^<]+</a>[^<]+"
    patron += '</div>[^<]+'
    patron += '<div class="nombre">[^<]+'
    patron += '<a[^>]+>([^<]+)</a>[^<]+'
    patron += '</div>[^<]+'
    patron += '<div class="sinopsis">(.*?)</div>[^<]+'
    patron += '<div class="enlace">'


    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2]
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapedplot = match[3].strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Ajusta el encoding a UTF-8
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")

        itemlist.append( Item(channel=__channel__, action="episodelist" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def detalle_programa(item):
    data = scrapertools.cachePage(item.url)

    # Thumbnail
    patron  = "<div class=\"bubble\">[^<]+<img src='([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.thumbnail = matches[0]

    # Argumento
    patron  = '<div class="container">[^<]+'
    patron += '<a name="info"></a><div class="header">[^<]+'
    patron += '<h3 class="bookIcon">[^<]+</h3>[^<]+'
    patron += '</div>[^<]+'
    patron  = '<p>(.*?)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        item.plot = scrapertools.htmlclean(matches[0])

    return item

def episodelist(item):
    logger.info("[seriespepito.py] list")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae los capítulos
    patron  = "<li><a  href='(http://.*?.seriespepito.com.*?)'[^>]+><span>([^<]+)</span></a>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = item.thumbnail
        scrapedplot = item.plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=__channel__, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show , context="4"))

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodelist", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[seriespepito.py] findvideos")
    itemlist = []
    from core.subtitletools import saveSubtitleName
    saveSubtitleName(item)
    try:
        # Descarga la pagina
        data = scrapertools.cachePage(item.url)
        #logger.info(data)
        '''
        <div class="content">
        <div class="viewOnline"><h4>Ver Capitulo 3 Online</h4></div>	
        <div style="clear:both"></div>					
        <table cellpadding="0" cellspacing="0" border="0">
        <thead>
        <tr>
        <th>Idioma</th>
        <th>Fecha</th>
        <th>Servidor</th>
        <th>Enlace</th>
        <th>Colabora</th>									
        <th>Comentario</th>
        </tr>
        </thead>
        <tbody>
        <tr><td><div class='flag vos'></div></td><td>21/11/2010</td><td><img src='http://www.seriespepito.com/seriespepito/servidores/megavideod.jpg' width=45 height=20 class=server></td><td><a class='grayButton' href='http://www.megavideo.com/?d=0I8GDC55' target='_blank' rel='nofollow' alt=''>Ver</a></td><td>lKranich</td><td></td></tr>                    </tbody>
        </table>
        <div style="clear:both"></div>			
        <div class="download"><h4>Descargar Capitulo 3 Gratis</h4></div>
        <div style="clear:both"></div>
        <table cellpadding="0" cellspacing="0" border="0">
        <thead>
        <tr>
        <th>Idioma</th>
        <th>Fecha</th>
        <th>Servidor</th>
        <th>Enlace</th>
        <th>Colabora</th>									
        <th>Comentario</th>
        </tr>
        </thead>
        <tbody>
        <tr><td><div class='flag vos'></div></td><td>21/11/2010</td><td><img src='http://www.seriespepito.com/seriespepito/servidores/megaupload.jpg' width=45 height=20 class=server></td><td><a class='grayButton' href='http://www.megaupload.com/?d=0I8GDC55' target='_blank' rel='nofollow' alt=''>Descargar</a></td><td>lKranich</td><td></td></tr>							</table>    
        </div>
        '''
    
        # Bloque con los enlaces
        patron  = '<div class="downloadContainer">(.*?)<div class="linkContainer">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        data = matches[0]
        
        # Listas de enlaces
        patron  = "<tr><td><div class='([^']+)'></div></td>"
        patron += "<td>[^<]+</td>"
        patron += "<td><img src='([^']+)'[^>]+></td>"
        patron += "<td><a.*?href='([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        numero = 1
        for match in matches:
            scrapedurl = match[2]
            scrapedthumbnail = item.thumbnail
            scrapedplot = item.plot

            if match[0]=="flag vos":
                idioma="SUB"
            else:
                idioma="ESP"
            
            servidor = match[1].lower()
            #print servidor
            if "megaupload" in servidor:
                servidor="megaupload"
            elif "megavideo" in servidor:
                servidor="megavideo"
            else:
                videos = servertools.findvideos(scrapedurl)
                if len(videos)>0:
                    servidor = videos[0][2]
                else:
                    servidor = ""
            #print servidor
    
            if servidor!="":
                scrapedtitle = "Mirror %d - Idioma %s [%s]" % (numero,idioma,servidor)
                itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=servidor, folder=False))
                numero = numero + 1
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )

    return itemlist