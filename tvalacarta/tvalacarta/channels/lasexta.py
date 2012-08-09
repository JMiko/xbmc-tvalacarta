# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Canal para la sexta
#------------------------------------------------------------
import urlparse,re,urllib

from core import logger
from core import scrapertools
from core.item import Item

logger.info("[sexta.py] init")

DEBUG = True
CHANNELNAME = "lasexta"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[sexta.py] mainlist")

    # Descarga la pagina
    url = "http://www.lasexta.com/sextatv"
    data = scrapertools.cachePage(url)

    itemlist = []
    salir = False
    pagina = 0
    while not salir:
        pageitems = getprogramaspagina("http://www.lasexta.com/sextatv/reload_programs","item_id=1&show_id=1&bd_id=1&pagina=%d&limit=3" % pagina)
        itemlist.extend( pageitems )
        pagina = pagina + 15
        salir = len(pageitems)<15
    
    return itemlist

def getprogramaspagina(url,post):
    logger.info("[sexta.py] getprogramaspagina post="+post)
    
    headers = [
            ['User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],
            ['X-Requested-With','XMLHttpRequest'],
            ['X-Prototype-Version','1.6.0.3'],
            ['Referer','http://www.lasexta.com/sextatv']
            ]
    
    # Esta peticion no se puede cachear
    data = scrapertools.cachePage(url,post,headers)
    #logger.info(data)

    # Extrae las entradas
    '''
    <div class="capaseccionl item_vip">
    <div class="player">
    <a href="http://www.lasexta.com/sextatv/seloquehicisteis">
    <img src="http://www.lasexta.com/media/sextatv/img/sextatv_logo_slqh.jpg" width="230" height="129" title="VÃ­deos de SÃ© lo que HicÃ­steis" alt="logotipo de SÃ© lo que hicÃ­steis" />
    <label class="item_vip_player_label">SÃ© lo que HicÃ­steis</label>
    <img src="http://www.lasexta.com/media/common/img/1pxtrans.gif" class="item_vip_player_link" alt="Ir a videos de SÃ© lo que HicÃ­steis"/>
    </a>
    </div>
    '''
    patron  = '<div class="capaseccionl item_vip">[^<]+'
    patron += '<div class="player">[^<]+'
    patron += '<a href="([^"]+)">[^<]+'
    patron += '<img src="([^"]+)"[^>]+>[^<]+'
    patron += '<label class="item_vip_player_label">([^<]+)</label>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2]
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = urlparse.urljoin(url,match[1])
        scrapedplot = ""
        scrapedshow = scrapedtitle
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # AÃ±ade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="secciones" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedshow , folder=True) )

    return itemlist

def secciones(item):
    logger.info("[sexta.py] secciones")
    
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Ahora extrae las pestaÃ±as
    patron  = '<li class="lsv_pestanas_li"><a id="[^"]+" href="javascript.change_videos.\'([^\']+)\',\'([^\']+)\'.."[^>]+><b class="left"></b>([^<]+)<b class="right"></b></a></li>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []

    for match in matches:
        scrapedurl = "http://www.lasexta.com/sextatv/change_videos/"+match[0]+"/"+match[1]
        scrapedtitle = match[2]
        # AÃ±ade al listado
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, show=item.show , folder=True) )

    return itemlist

def videos(item):
    logger.info("[sexta.py] videos")
    
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    itemlist = parsevideos(item,data)

    # Paginacion
    # El id es 11_ultimos_15
    # La pagina es un POST a http://www.lasexta.com/sextatv/reload con "seccion=11&pagina=15&tipo=ultimos&section_id"
    while True:
        patron = '<a href="javascript.reload.\'([^\']+)\'.;" class="siguiente" title="P&aacute;gina siguiente">P&aacute;gina siguiente</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        if len(matches)>0:
            partes = matches[0].split("_")
            url = "http://www.lasexta.com/sextatv/reload"
            post = "seccion=%s&pagina=%s&tipo=%s&section_id" % (partes[0],partes[2],partes[1])
            data = scrapertools.cachePage(url,post)
            newitems = parsevideos(item,data)
            itemlist.extend(newitems)
        else:
            break

    # Caso especial "Ver todos los videos"
    patron = '<a href="javascript.reload.\'([^\']+)\'.;">Ver todos'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
        return itemlist
    
    partes = matches[0].split("_")
    url = "http://www.lasexta.com/sextatv/reload"
    post = "seccion=%s&pagina=%s&tipo=%s&section_id=%s" % (partes[0],partes[2],partes[1],partes[3])
    data = scrapertools.cachePage(url,post)
    
    # Paginacion
    # El id es 11_ultimos_15_1234
    # La pagina es un POST a http://www.lasexta.com/sextatv/reload con "seccion=11&pagina=15&tipo=ultimos&section_id=1234"
    while True:
        patron = '<a href="javascript.reload.\'([^\']+)\'.;" class="siguiente" title="P&aacute;gina siguiente">P&aacute;gina siguiente</a>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
    
        if len(matches)>0:
            partes = matches[0].split("_")
            url = "http://www.lasexta.com/sextatv/reload"
            post = "seccion=%s&pagina=%s&tipo=%s&section_id=%s" % (partes[0],partes[2],partes[1],partes[3])
            data = scrapertools.cachePage(url,post)
            newitems = parsevideos(item,data)
            itemlist.extend(newitems)
        else:
            break


    return itemlist

def parsevideos(item,data):
    logger.info("[sexta.py] parsevideos")
    #print data
    
    # Extrae los videos
    '''
    <div class="capaseccionl item">
    <div class="player_programas">
    <a href="http://www.lasexta.com/sextatv/quienviveahi/completos/quien_vive_ahi___jueves__21_de_octubre/315352/1"><img src="http://www.sitios.lasexta.com/pictures/215481/pictures_20101020_1601215481_crop1.jpg" width="170" height="127" title="quien_vive_ahi___jueves__21_de_octubre" alt="quien_vive_ahi___jueves__21_de_octubre" /></a>
    <a href="http://www.lasexta.com/sextatv/quienviveahi/completos/quien_vive_ahi___jueves__21_de_octubre/315352/1" class="item_cortina">
    <img src="http://www.lasexta.com/media/common/img/1pxtrans.gif" width="170" height="127" title="quien_vive_ahi___jueves__21_de_octubre" alt="quien_vive_ahi___jueves__21_de_octubre" />
    <label class="item_cortina_text">El programa visit del campo o un&#8230;</label>
    <label class="item_cortina_play">PLAY</label>
    </a>
    </div>
    <h6 class="fecha">22/10/2010 </h6>
    <h5 class="titulo"><a href="http://www.lasexta.com/sextatv/quienviveahi/completos/quien_vive_ahi___jueves__21_de_octubre/315352/1" title="quien_vive_ahi___jueves__21_de_octubre">aaaaaJueves, 21 de octubre</a></h5>
    </div>
    '''
    patron  = '<div class="capaseccionl item">[^<]+'
    patron += '<div class="player_programas">[^<]+'
    patron += '<a href="([^"]+)"><img src="([^"]+)"[^>]+></a>.*?'
    patron += '<label class="item_cortina_text">([^<]*)</label>.*?'
    patron += '<h6 class="fecha">([^<]+)</h6>[^<]+'
    patron += '<h5 class="titulo"><a[^>]+>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    
    for match in matches:
        scrapedtitle = match[4]+" "+match[3]
        scrapedurl = match[0]
        scrapedthumbnail = match[1]
        scrapedplot = match[2] 
        scrapedpage = scrapedurl
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getVideos" , url=scrapedurl, page=scrapedpage, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , folder=True) )
    
    return itemlist

def getVideos(item):
    logger.info("[lasexta.py] getVideos")
    itemlist = []
    post = urllib.urlencode({"web":item.url})

    headers = []
    headers.append( [ "User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:14.0) Gecko/20100101 Firefox/14.0.1" ] )

    location = scrapertools.get_header_from_response("http://www.descargavideos.tk/",post=post,header_to_get="location",headers=headers)
    
    headers = []
    headers.append( [ "Referer","http://www.descargavideos.tk/" ] )
    headers.append( [ "User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:14.0) Gecko/20100101 Firefox/14.0.1" ] )

    data = scrapertools.cache_page(location)
    logger.info("data="+data)
    patron = '<a id=resenl[^>]+>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)

    i=1
    for scrapedurl in matches:
        url = scrapedurl
        #scrapedVideoUrl = scrapedVideoUrl.replace("mp4:", " playpath=mp4:")
        #scrapedVideoUrl = scrapedVideoUrl + " swfvfy=true swfurl=http://www.lasexta.com/media/swf/reproductor_sextatv/player_overlay.swf"
        itemlist.append( Item(channel=CHANNELNAME, title="Parte %d"%i , action="play", server="Directo" , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=False) )
        i=i+1

    return itemlist
