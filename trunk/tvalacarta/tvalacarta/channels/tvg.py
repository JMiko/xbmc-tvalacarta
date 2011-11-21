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

logger.info("[tvg.py] init")

DEBUG = False
CHANNELNAME = "tvg"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tvg.py] mainlist")
    itemlist=[]
    itemlist.append( Item(channel=CHANNELNAME, title="Novedades"           , action="novedades" , url="http://www.crtvg.es/tvg/a-carta"))
    itemlist.append( Item(channel=CHANNELNAME, title="Todos los programas" , action="categorias"  , url="http://www.crtvg.es/tvg/a-carta"))
    return itemlist

def novedades(item):
    item.url = "http://www.crtvg.es/ax/tvgalacartahome"
    return videos(item)

def categorias(item):
    logger.info("[tvg.py] categorias")
    itemlist=[]

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae las categorias (carpetas)
    patron  = '<li id="categoria-[^"]+" class="first-level">[^<]+'
    patron += '<a href="" title="[^"]+" onclick="return false;">([^<]+)</a>(.*?)</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[0].strip()
        scrapedurl = ""
        scrapedthumbnail = ""
        scrapedplot = ""
        extra = match[1].strip()
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="programas" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra=extra , category = scrapedtitle , folder=True) )

    return itemlist

def programas(item):
    logger.info("[tvg.py] programas")
    itemlist=[]
    
    # Extrae los programas
    data = item.extra
    #logger.info("data="+data)
    patron  = '<li id="programa-[^"]+" class="second-level">[^<]+'
    patron += '<a href="#" title="[^"]+" onclick="return programaclickTvg\((\d+), (\d+), (\d+)\)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[3].strip()
        scrapedurl = "http://www.crtvg.es/ax/tvgalacarta/programa:%s/pagina:%s/seccion:%s" % (match[0],match[1],match[2])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, page=scrapedurl , thumbnail=scrapedthumbnail, plot=scrapedplot , show=scrapedtitle , category = item.category , folder=True) )

    return itemlist

def videos(item):
    import urllib
    logger.info("[tvg.py] videos")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = data.replace("\\","")
    #logger.info(data)

    # Extrae los videos
    '''
    {"listado":"<div id="programas-33522-tvg">  
    <div class="a-carta-inside">               <h2>De viaxe</h2>                   
    <ul id="programas-a-carta-tvg">       
    <li id="programa-168965" class="listadoimagenes-li">  
    <div id="imagen-programa-168965" class="listadoimagenes-imagen">                  
    <a href="/tvg/a-carta/de-viaxe-13-11-2011" title="De viaxe (13/11/2011)"><img src="/files/single/20111114094844_deviaxeg.jpg" alt="De viaxe (13/11/2011)"/></a>        </div>  
    <div id="info-programa-168965" class="listadoimagenes-info">  
    <div id="titulo-programa-168965"class="listadoimagenes-titulo">  
    <a href="/tvg/a-carta/de-viaxe-13-11-2011" title="De viaxe (13/11/2011)">De viaxe (13/11/2011)</a>                 </div>                  
    <div id="data-programa-168965"class="listadoimagenes-data">                      13/11/2011                 </div>              </div>          </li>       
    <li id="programa-162688" class="listadoimagenes-li">              <div id="imagen-programa-162688" class="listadoimagenes-imagen">                              <a href="/tvg/a-carta/de-viaxe-06-11-2011" title="De viaxe (06/11/2011)"><img src="/files/single/20111107100704_deviaxeg.jpg" alt="De viaxe (06/11/2011)"/></a>             </div>              <div id="info-programa-162688" class="listadoimagenes-info">                  <div id="titulo-programa-162688"class="listadoimagenes-titulo">                      <a href="/tvg/a-carta/de-viaxe-06-11-2011" title="De viaxe (06/11/2011)">De viaxe (06/11/2011)</a>                 </div>                                  <div id="data-programa-162688"class="listadoimagenes-data">                      06/11/2011                 </div>              </div>          </li>               <li id="programa-42111" class="listadoimagenes-li">              <div id="imagen-programa-42111" class="listadoimagenes-imagen">                              <a href="/tvg/a-carta/caion" title="Caiu00f3n"><img src="/files/single/deviaxe2.jpg" alt="Caiu00f3n"/></a>             </div>              <div id="info-programa-42111" class="listadoimagenes-info">                  <div id="titulo-programa-42111"class="listadoimagenes-titulo">                      <a href="/tvg/a-carta/caion" title="Caiu00f3n">Caiu00f3n</a>                 </div>                                  <div id="data-programa-42111"class="listadoimagenes-data">                      19/09/2010                 </div>              </div>          </li>               <li id="programa-42058" class="listadoimagenes-li">              <div id="imagen-programa-42058" class="listadoimagenes-imagen">                              <a href="/tvg/a-carta/poio-1" title="Poio"><img src="/files/single/20110407142628_deviaxe3.jpg" alt="Poio"/></a>             </div>              <div id="info-programa-42058" class="listadoimagenes-info">                  <div id="titulo-programa-42058"class="listadoimagenes-titulo">                      <a href="/tvg/a-carta/poio-1" title="Poio">Poio</a>                 </div>                                  <div id="data-programa-42058"class="listadoimagenes-data">                      09/05/2010                 </div>              </div>          </li>               <li id="programa-42051" class="listadoimagenes-li">              <div id="imagen-programa-42051" class="listadoimagenes-imagen">                              <a href="/tvg/a-carta/a-laracha-1" title="A Laracha"><img src="/files/single/20110407142720_deviaxe3.jpg" alt="A Laracha"/></a>             </div>              <div id="info-programa-42051" class="listadoimagenes-info">                  <div id="titulo-programa-42051"class="listadoimagenes-titulo">                      <a href="/tvg/a-carta/a-laracha-1" title="A Laracha">A Laracha</a>                 </div>                                  <div id="data-programa-42051"class="listadoimagenes-data">                      18/04/2010                 </div>              </div>          </li>               <li id="programa-42048" class="listadoimagenes-li">              <div id="imagen-programa-42048" class="listadoimagenes-imagen">                              <a href="/tvg/a-carta/rio-xubia" title="Ru00edo Xubia"><img src="/files/single/20110407142753_deviaxe3.jpg" alt="Ru00edo Xubia"/></a>             </div>              <div id="info-programa-42048" class="listadoimagenes-info">                  <div id="titulo-programa-42048"class="listadoimagenes-titulo">                      <a href="/tvg/a-carta/rio-xubia" title="Ru00edo Xubia">Ru00edo Xubia</a>                 </div>                                  <div id="data-programa-42048"class="listadoimagenes-data">                      11/04/2010                 </div>              </div>          </li>           </ul> t     </div>      </div> ","paginacion":"     <div id="navegador">          <ul>                                           <li class="paginador-inside active">                       <a href="#" title="1" onclick="return paginaclickTvg(33522, 1, 294);">                           1                      </a>                   </li>                                   <li class="paginador-inside">                       <a href="#" title="2" onclick="return paginaclickTvg(33522, 2, 294);">                           2                      </a>                   </li>                                   <li class="paginador-inside">                       <a href="#" title="3" onclick="return paginaclickTvg(33522, 3, 294);">                           3                      </a>                   </li>
    <li class="next">                  <a href="#" title="Seguinte" onclick="return posteriorpaginaclickTvg(33522, 2, 294);">                                      <img src="/static/img/navegador-siguiente.png" alt="Seguinte" />                  </a>              </li>                                   </ul>      </div>      "}
    '''
    patron  = '<li id="programa-[^<]+'
    patron += '<div id="imagen-programa-[^<]+'
    patron += '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = match[1].strip()
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=True) )

    # <a href="#" title="Seguinte" onclick="return posteriorpaginaclickTvg(33522, 2, 294);">
    patron  = '<a href="\#" title="Seguinte" onclick="return posteriorpaginaclickTvg\((\d+), (\d+), (\d+)\)\;'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for match in matches:
        scrapedtitle = ">>> Página siguiente"
        scrapedurl = "http://www.crtvg.es/ax/tvgalacarta/programa:%s/pagina:%s/seccion:%s" % (match[0],match[1],match[2])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show , category = item.category , folder=True) )

    return itemlist

def play(item):
    logger.info("[tvg.py] play")
    itemlist = []

    #from servers import tvg as conector
    #video_urls = conector.get_video_url(item.url)
    video_urls = get_video_url(item.url)

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=video_urls[0][1], thumbnail=item.thumbnail , plot=item.plot , server = "directo" , show = item.show , category = item.category , folder=False) )

    return itemlist

# Esto está en el conector, para futuras versiones se podrá quitar
def get_video_url( page_url , premium = False , user="" , password="", video_password="", page_data="" ):
    logger.info("[tvg.py] get_video_url(page_url='%s')" % page_url)

    if page_data=="":
        data = scrapertools.cache_page(page_url)
    else:
        data = page_data

    video_urls = []

    '''
    rtmp: {
        url: "http://www.crtvg.es/flowplayer3/flowplayer.rtmp-3.2.3.swf",
        netConnectionUrl: "rtmp://media1.crtvg.es:80/vod" //Para VOD
    },
    clip: {
        url: "mp4:00/0752/0752_20110129153400.mp4",
        provider: "rtmp",
        autoPlay: false,
        //autoBuffering: true,
        ipadUrl: "http://media1.crtvg.es:80/vod/_definst_/mp4:00/0752/0752_20110129153400.mp4/playlist.m3u8", //para ipad vod
        start: 0,
        duration: 0,
        scaling: "fit" //scaling: orig, // fit, half, orig,scale
    }
    '''
    patron  = 'rtmp\: \{.*?netConnectionUrl\: "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0:
        return []
    base = matches[0]
    
    patron  = 'clip\: \{.*?url\: "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0:
        return []
    playpath = matches[0]
    rtmpurl = base+"/"+playpath
    rtmpurl = rtmpurl.replace("mp4:", " playpath=mp4:")
    
    patron  = 'clip\: \{.*?ipadUrl\: "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0:
        return []
    ipad = matches[0]
    
    video_urls.append( [ "RTMP [tvg]" , rtmpurl ] )
    video_urls.append( [ "iPad [tvg]" , ipad ] )

    for video_url in video_urls:
        logger.info("[tvg.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls
