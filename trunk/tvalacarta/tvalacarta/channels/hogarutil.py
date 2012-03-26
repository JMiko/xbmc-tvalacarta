# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para hogarutil
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------

import urlparse,urllib,re

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[hogarutil.py] init")

DEBUG = True
CHANNELNAME = "hogarutil"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[hogarutil.py] channel")

    item.url = "http://www.hogarutil.com/tv/programas/"
    return programas(item)

def programas(item):
    logger.info("[hogarutil.py] programas")
    
    #print item.tostring()
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron  = '<img src="([^"]+)" alt="([^"]+)"/>[^<]*<h2 class="ms-titulo"><a href="([^"]+)">([^<]+)</a></h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for thumbnail,alt,url,title in matches:
        scrapedtitle = title.strip()
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle, folder=True) )

    return itemlist

def episodios(item):
    logger.info("[hogarutil.py] episodios")
    
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # episodios
    '''
    <span>
    <img src="/archivos/201203/bricomania-686-mesa-revistero-xl-173x125x80xX.jpg?1" alt="Crear mesa revistero" />							<h3 class="ms-antetitulo">Bricomanía</h3>
    <h3 class="ms-antetitulo" style="text-align: right; color: #89BA2A;">24/03/2012</h3>
    <h2 class="ms-titulo"><a href="/tv/programas/bricomania/201203/24/index.html" title="Crear mesa revistero">Crear mesa revistero</a></h2>
    </span>
    '''

    patron  = '<span>[^<]+'
    patron += '<img src="([^"]+)" alt="[^"]+"[^>]+>[^<]*<h3 class="ms-antetitulo">([^<]+)</h3>[^<]+'
    patron += '<h3 class="ms-antetitulo" style="[^"]+">([^<]+)</h3>[^<]+'
    patron += '<h2 class="ms-titulo"><a href="([^"]+)" title="[^"]+">([^<]+)</a></h2>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for thumbnail,show,fecha,url,titulo in matches:
        scrapedtitle = titulo + " " + fecha
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = urlparse.urljoin(item.url,thumbnail)
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="detalle" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , folder=True) )

    # Otras temporadas
    '''
    <dl id="fechas-programas">
    <dt class="ms-anno">AÑO</dt>
    <dd class="seleccion">
    <ul class="anos">
    <li class="ano 2011"><a href="/tv/programas/decogarden/index.html?201106" title="Vídeos de Decogarden - Año 2011">2011</a></li>
    <li class="ano 2012"><a href="/tv/programas/decogarden/index.html?201201" title="Vídeos de Decogarden - Año 2012">2012</a></li>
    </ul>
    </dd>
    <dt class="ms-anno"></dt>
    <dd class="ms-paginar">
    <ul class="meses 2011" style="display: none;">
    <li class="mes 06"><a title="Vídeos de Decogarden - Año 2011 - Mes Junio" href="/tv/programas/decogarden/index.html?201106">Junio</a></li>
    <li class="mes 09"><a title="Vídeos de Decogarden - Año 2011 - Mes Septiembre" href="/tv/programas/decogarden/index.html?201109">Septiembre</a></li>
    <li class="mes 10"><a title="Vídeos de Decogarden - Año 2011 - Mes Octubre" href="/tv/programas/decogarden/index.html?201110">Octubre</a></li>
    <li class="mes 11"><a title="Vídeos de Decogarden - Año 2011 - Mes Noviembre" href="/tv/programas/decogarden/index.html?201111">Noviembre</a></li>
    <li class="mes 12"><a title="Vídeos de Decogarden - Año 2011 - Mes Diciembre" href="/tv/programas/decogarden/index.html?201112">Diciembre</a></li>
    </ul>
    <ul class="meses 2012" style="display: none;">
    <li class="mes 01"><a title="Vídeos de Decogarden - Año 2012 - Mes Enero" href="/tv/programas/decogarden/index.html?201201">Enero</a></li>
    <li class="mes 02"><a title="Vídeos de Decogarden - Año 2012 - Mes Febrero" href="/tv/programas/decogarden/index.html?201202">Febrero</a></li>
    <li class="mes 03"><a title="Vídeos de Decogarden - Año 2012 - Mes Marzo" href="/tv/programas/decogarden/index.html?201203">Marzo</a></li>
    </ul>
    </dd>
    </dl>
    '''
    patron = '<dd class="ms-paginar">(.*?)</dd>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    if len(matches)>0:
        subdata = matches[0]
        patron  = '<li[^<]+<a\s+title="([^"]+)"\s+href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.compile(patron,re.DOTALL).findall(subdata)
        
        #if DEBUG: scrapertools.printMatches(matches)
        for titulo,url,etiqueta in matches:
            scrapedtitle = titulo
            scrapedurl = urlparse.urljoin(item.url,url)
            scrapedthumbnail = item.thumbnail
            scrapedplot = ""
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
            # Añade al listado
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show , folder=True) )

    return itemlist

def detalle(item):
    logger.info("[hogarutil.py] detalle")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    patron  = 'GENERAL.videoKewego.".ms-player2-in-([^"]+)","([^"]+)","100.","100.","".'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for parte,id in matches:
        scrapedtitle = "Parte "+parte
        scrapedurl = "http://www.hogarutil.com/backend/kewego.php?accion=player&id="+id+"&ancho=100%25&alto=100%25&preview="
        scrapedthumbnail = item.thumbnail
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show , folder=False) )
    
    return itemlist

def play(item):
    logger.info("[hogarutil.py] play")
    itemlist=[]
    
    # De esta URL
    # http://www.hogarutil.com/backend/kewego.php?accion=player&id=fc0d7bbd18es&ancho=100%25&alto=100%25&preview=
    # Saco el playerkey y el sig
    '''
    <div id="flash_kplayer_fc0d7bbd18es" class="flash_kplayer" name="flash_kplayer" data-sig="fc0d7bbd18es" data-playerkey="d09a64ff5131" style="width:100%px; height:100%px;"><object  width="100%" height="100%" type="application/x-shockwave-flash" data="http://sa.kewego.com/swf/kp.swf" name="kplayer_fc0d7bbd18es" id="kplayer_fc0d7bbd18es"><param name="bgcolor" value="0x000000" />
    <param name="allowfullscreen" value="true" />
    <param name="allowscriptaccess" value="always" />
    <param name="flashVars" value="language_code=es&amp;playerKey=d09a64ff5131&amp;configKey=&amp;suffix=&amp;sig=fc0d7bbd18es&amp;autostart=false" />
    <param name="movie" value="http://sa.kewego.com/swf/kp.swf" />
    <param name="wmode" value="opaque" /><video  poster="http://api.kewego.com/video/getHTML5Thumbnail/?playerKey=d09a64ff5131&amp;sig=fc0d7bbd18es" height="100%" width="100%" preload="none"  controls="controls"></video><script src="http://sa.kewego.com/embed/assets/kplayer-standalone.js"></script><script defer="defer">kitd.html5loader("flash_kplayer_fc0d7bbd18es");</script></object></div>
    '''
    data = scrapertools.cache_page(item.url)
    player_key = scrapertools.get_match(data,'data-playerkey="([^"]+)"')
    sig = scrapertools.get_match(data,'data-sig="([^"]+)"')
    
    # De esta URL
    # http://api.kewego.com/config/getStreamInit/ con POST "playerKey=d09a64ff5131&request%5Fverbose=false&player%5Ftype=kp&sig=fc0d7bbd18es&language%5Fcode=es"
    # Saco el apptoken
    '''
    <?xml version="1.0" encoding="UTF-8"?>
    <kewego_response>
    <message><type>kp</type><playerAppToken>2f9c9e5dff567e05a6a820fb630166f91667eefda9080c0303898e2ed29601be0fefd9b3fc15e20d9d611a333218f5d5fc5e8621728584c469c880bbb53023f8</playerAppToken>
    '''
    url = "http://api.kewego.com/config/getStreamInit/"
    data = scrapertools.cache_page(url,post="playerKey="+player_key+"&request%5Fverbose=false&player%5Ftype=kp&sig="+sig+"&language%5Fcode=es")
    app_token = scrapertools.get_match(data,'<playerAppToken>([^<]+)</playerAppToken>')

    # De esta URL
    # http://api.kewego.com/video/getStream/?appToken=2f9c9e5dff567e05a6a820fb630166f91667eefda9080c0303898e2ed29601be0fefd9b3fc15e20d9d611a333218f5d5fc5e8621728584c469c880bbb53023f8&sig=fc0d7bbd18es&format=sd&v=101610
    # Saco el vídeo del location
    # Location	http://v.kewego.com/v/5/0733/G3EDLB9Y.mp4?key%3D2a194af64a517e64
    url = "http://api.kewego.com/video/getStream/?appToken="+app_token+"&sig="+sig+"&format=sd&v=101610"
    location = scrapertools.get_header_from_response(url,header_to_get="location")

    #Esto sí funciona
    from core import downloadtools, config
    import thread
    temp_file = config.get_temp_file("hogarutil.mp4")
    thread.start_new_thread(downloadtools.downloadfile, (location,temp_file), {'silent':True})
    import xbmc
    logger.info("sleep")
    xbmc.sleep(1000)
    logger.info("fin sleep")

    # Añade al listado
    itemlist.append( Item(channel=CHANNELNAME, title=item.title,  action="play" , url=temp_file, thumbnail=item.thumbnail, plot=item.plot, show=item.show) )
    
    return itemlist