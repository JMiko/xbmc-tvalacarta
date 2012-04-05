# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para antena 3
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse,re
import urllib

from core import logger
from core import scrapertools
from core.item import Item

DEBUG = False
CHANNELNAME = "antena3"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[antena3.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Los más vistos" , action="losmasvistos" , url="http://www.antena3.com/videos/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Últimos vídeos" , action="ultimosvideos", url="http://www.antena3.com/videos/", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Última semana"  , action="ultimasemana" , url="http://www.antena3.com/videos/ultima-semana.html", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Series"         , action="series"       , url="http://www.antena3.com/videos/series.html", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Noticias"       , action="noticias"     , url="http://www.antena3.com/videos/noticias.html", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Programas"      , action="programas"    , url="http://www.antena3.com/videos/programas.html", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Infantil"       , action="series"       , url="http://www.antena3.com/videos/series-infantiles.html", folder=True) )
    #itemlist.append( Item(channel=CHANNELNAME, title="TV Movies"      , action="tvmovies"     , url="http://www.antena3.com/videos/tv-movies.html", folder=True) )

    return itemlist

def losmasvistos(item):
    logger.info("[antena3.py] losmasvistos")
    return videosportada(item,"masVistos")

def ultimosvideos(item):
    logger.info("[antena3.py] ultimosvideos")
    return videosportada(item,"ultimosVideos")

def videosportada(item,id):
    logger.info("[antena3.py] videosportada")
    
    #print item.tostring()
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas
    patron = '<div id="'+id+'"(.*?)</div><!-- .visor -->'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    data = matches[0]
    
    '''
    <div>
    <a title="Vídeos de El Internado - Capítulo 8 - Temporada 7" href="/videos/el-internado/temporada-7/capitulo-8.html">
    <img title="Vídeos de El Internado - Capítulo 8 - Temporada 7" 
    src="/clipping/2010/07/21/00048/10.jpg"
    alt="El último deseo"
    href="/videos/el-internado/temporada-7/capitulo-8.html"
    />
    <strong>El Internado</strong>
    <p>El último deseo</p></a>  
    </div>
    '''

    patron  = '<div>[^<]+'
    patron += '<a title="([^"]+)" href="([^"]+)">[^<]+'
    patron += '<img.*?src="([^"]+)"[^<]+'
    patron += '<strong>([^<]+)</strong>[^<]+'
    patron += '<h2><p>([^<]+)</p></h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[3]+" - "+match[4]+" ("+match[0]+")"
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def ultimasemana(item):
    logger.info("[antena3.py] ultimasemana")
    
    #print item.tostring()
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas (series)
    '''
    <div>
    <em class="play_video"><img title="ver video" src="/static/modosalon/images/button_play_s1.png" alt="ver video"/></em>
    <a title="Vídeos de Noticias 1 - 19 de Agosto de 2.010" href="/videos/noticias/noticias-1-19-agosto.html">
    <img title="Vídeos de Noticias 1 - 19 de Agosto de 2.010"  
    src="/clipping/2010/05/21/00055/10.jpg"
    alt="19 de agosto"
    href="/videos/noticias/noticias-1-19-agosto.html"
    />
    </a>
    <a title="Vídeos de Noticias 1 - 19 de Agosto de 2.010" href="/videos/noticias/noticias-1-19-agosto.html">
    <strong>Noticias 1</strong>
    <p>19 de agosto</p></a>  
    </div>
    '''
    patron  = '<div>[^<]+'
    patron += '<em[^>]+><img[^>]+></em>[^<]+'
    patron += '<a title="([^"]+)" href="([^"]+)">[^<]+'
    patron += '<img title="[^"]+"[^<]+'  
    patron += 'src="([^"]+)"[^>]+>[^<]+'
    patron += '</a>[^<]+'
    patron += '<a[^>]+>[^<]+'
    patron += '<strong>([^<]+)</strong>[^<]+'
    patron += '<p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[3]+" - "+match[4]+" ("+match[0]+")"
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist

def series(item):
    logger.info("[antena3.py] series")
    
    #print item.tostring()
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas (series)
    '''
    <div>
    <a title="Vídeos de Share - Capítulos Completos" href="/videos/share.html">
    <img title="Vídeos de Share - Capítulos Completos" href="/videos/share.html"
    src="/clipping/2010/08/06/00246/10.jpg"
    alt="Share"	
    />
    <a title="Vídeos de Share - Capítulos Completos" href="/videos/share.html"><h2><p>Share</p></h2></a>                    
    </a>
    </div>
    </li>
    '''
    patron  = '<div>[^<]+'
    patron += '<a\W+title="[^"]+" href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)"[^<]+'
    patron += '<a[^<]+<h2><p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2].strip()
        # Hace un quote porque algunas URL están con acentos
        #/videos/Deberías saber de mi .html
        #/videos/Deber%C3%ADas%20saber%20de%20mi%20.html
        scrapedurl = urlparse.urljoin(item.url,urllib.quote(match[0]))
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=True) )

    return itemlist

def episodios(item):
    logger.info("[antena3.py] episodios")
    logger.info(item.tostring())
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # episodios
    '''
    <div>
    <a  title="Vídeos de El Internado - Capítulo 8 - Temporada 7"
    href="/videos/el-internado/temporada-7/capitulo-8.html">
    <img title="Vídeos de El Internado - Capítulo 8 - Temporada 7" 
    src="/clipping/2010/07/21/00048/10.jpg"
    alt="EL INTERNADO T7 C8"
    href="/videos/el-internado/temporada-7/capitulo-8.html"
    />
    <em class="play_video"><img title="ver video" src="/static/modosalon/images/button_play_s1.png" alt="ver video"/></em>
    <strong>EL INTERNADO T7 C8</strong>
    <p>El último deseo</p>
    </a>    
    </div>
    '''
    patron  = '<div>[^<]+'
    patron += '<a.*?href="([^"]+)"[^<]+'
    patron += '<img.*?src="([^"]+)".*?'
    patron += '<strong>([^<]+)</strong>[^<]+'
    patron += '<h2><p>([^<]+)</p></h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2]+" - "+match[3]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , folder=True) )

    # Otras temporadas
    patron = '<dd class="paginador">(.*?)</dd>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    if len(matches)>0:
        subdata = matches[0]
        
        '''
        <ul>
        <li  class="active" >
        <a     title="Vídeos de El Internado - Temporada 7 - Capítulos Completos"
        href="/videos/el-internado.html" >7
        </a>
        </li>
        '''
        patron  = '<li[^<]+<a\s+title="([^"]+)"\s+href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(subdata)
        
        #if DEBUG: scrapertools.printMatches(matches)
        for titulo,url,etiqueta in matches:
            if "emporada" in titulo:
                scrapedtitle = "Temporada "+etiqueta.strip()
            else:
                scrapedtitle = etiqueta.strip()
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = item.thumbnail
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show , folder=True) )

    # Otras temporadas
    patron = '<dd class="seleccion">(.*?)</dd>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    if len(matches)>0:
        subdata = matches[0]
        
        '''
        <dd class="seleccion">
        <ul>
        <li  class="active" ><a title="Vídeos de El Hormiguero 3.0 - Año 2012" href="/videos/el-hormiguero.html" >2012</a></li>
        <li ><a title="Vídeos de El Hormiguero 3.0 - Año 2011" href="/videos/el-hormiguero/2011.html" >2011</a></li>
        </ul>
        </dd>
        '''
        patron  = '<li[^<]+<a\s+title="([^"]+)"\s+href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(subdata)
        
        #if DEBUG: scrapertools.printMatches(matches)
        for titulo,url,etiqueta in matches:
            if "emporada" in titulo:
                scrapedtitle = "Temporada "+etiqueta.strip()
            else:
                scrapedtitle = etiqueta.strip()
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = item.thumbnail
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show , folder=True) )

    return itemlist

def noticias(item):
    logger.info("[antena3.py] noticias")
    return series(item)
    '''
    print item.tostring()
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las entradas (series)
    '''
    '''
    <div>
    <a title="Vídeos de Noticias Fin de Semana - 22 de Agosto de 2.010" 
    href="/videos/noticias/noticias-fin-semana-22082010.html">
    <img title="Vídeos de Noticias Fin de Semana - 22 de -1 de 2.010" 
    src="/clipping/2010/06/01/00105/10.jpg"
    alt="Noticias fin de semana 22-08-2010 "
    href="/videos/noticias/fin-de-semana-completo/2010-agosto-22.html"
    />
    <em class="play_video"><img title="ver video" src="/static/modosalon/images/button_play_s1.png" alt="ver video"/></em>
    <a 
    title="Vídeos de Noticias Fin de Semana - 22 de Agosto de 2.010"
    href="/videos/noticias/noticias-fin-semana-22082010.html"
    >
    <strong>Noticias Fin de Semana</strong>
    <p>22 de agosto 15.00h</p>
    </a>                    
    '''
    '''
    patron  = '<div>[^<]+'
    patron += '<a.*?href="([^"]+)">[^<]+'
    patron += '<img.*?src="([^"]+)"[^>]+>.*?'
    patron += '<strong>([^<]+)</strong>[^<]+'
    patron += '<h2><p>([^<]+)</p></h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2]+" - "+match[3]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , folder=True) )

    return itemlist
    '''
def programas(item):
    logger.info("[antena3.py] programas")
    return series(item)
    
def tvmovies(item):
    logger.info("[antena3.py] tvmovies")
    return series(item)

def detalle(item):
    logger.info("[antena3.py] detalle")
    #print item.tostring()

    itemlist = []
    '''
    try:
        # Descarga la página de detalle
        data = scrapertools.cachePage(item.url)
    
        patron="<source src='([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=scrapedurl, page = item.url, thumbnail=item.thumbnail , plot=item.plot , server = "directo" , folder=False) )
    except:
        logger.info("[antena3.py] nada encontrado en "+item.url)
    '''
    data = scrapertools.cachePage(item.url)

    # Extrae el xml
    patron = "player_capitulo.xml='([^']+)';"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    scrapedurl = urlparse.urljoin(item.url,matches[0])
    logger.info("url="+scrapedurl)
    
    # Descarga la página del xml
    data = scrapertools.cachePage(scrapedurl)

    # Extrae las entradas del video y el thumbnail
    patron = '<urlVideoMp4><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    baseurlvideo = matches[0]
    logger.info("baseurlvideo="+baseurlvideo)
    
    patron = '<urlImg><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    baseurlthumb = matches[0]
    logger.info("baseurlthumb="+baseurlthumb)
    
    patron  = '<archivoMultimediaMaxi>[^<]+'
    patron += '<archivo><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapedthumbnail = urlparse.urljoin(baseurlthumb,matches[0])
    logger.info("scrapedthumbnail="+scrapedthumbnail)
    
    patron  = '<archivoMultimedia>[^<]+'
    patron += '<archivo><\!\[CDATA\[([^\]]+)\]\]>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []
    i = 1
    for match in matches:
        scrapedurl = baseurlvideo+match
        logger.info("scrapedurl="+scrapedurl)
        itemlist.append( Item(channel=CHANNELNAME, title="(%d) %s" % (i,item.title) , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail , plot=item.plot , server = "directo" , folder=False) )
        i=i+1
    return itemlist
