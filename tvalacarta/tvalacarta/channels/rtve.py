# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para RTVE
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse, re

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
    itemlist.append( Item(channel=CHANNELNAME, title="Recomendados"   , action="videolist" , url="http://www.rtve.es/alacarta/todos/recomendados/index.html", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Últimos 7 días" , action="videolist" , url="http://www.rtve.es/alacarta/todos/ultimos/index.html", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Temas"          , action="videolist" , url="http://www.rtve.es/alacarta/todos/temas/index.html", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Todos A-Z"      , action="videolist" , url="http://www.rtve.es/alacarta/todos/abecedario/index.html", folder=True) )
    itemlist.append( Item(channel=CHANNELNAME, title="Archivo TVE"    , action="videolist" , url="http://www.rtve.es/alacarta/todos/archivo-tve/index.html", folder=True) )

    return itemlist

def videolist(item):
    logger.info("[rtve.py] videolist")

    # Descarga la página
    logger.info("[rtve.py] videolist descarga página principal "+item.url)
    data = scrapertools.cachePage(item.url)

    # Extrae las categorias (carpetas)
    patron  = '<a href="(/alacarta/todos/[^"]+)".*?>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        # Extrae los datos
        scrapedtitle = scrapertools.entityunescape(match[1].strip())
        scrapedurl = urlparse.urljoin("http://www.rtve.es", match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        
        # Ajusta el encoding a UTF-8
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")

        # Añade al listado de XBMC
        #addvideo( scrapedtitle , scrapedurl , category )
        if scrapedtitle=="Recomendados" or scrapedtitle=="Temas" or scrapedtitle=="Todos A-Z" or scrapedtitle=="Archivo TVE" or scrapedtitle=="Ultimos 7 dias" or scrapedtitle=="Adelante":
            pass
        else:
            itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videolist" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.title , folder=True) )

    # Extrae los videos de la página actual
    #patron  = '<li id="video-(\d+)">\W*<div>\W*<a rel="facebox" href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"><img alt="Reproducir" src="/css/i/mediateca/play.png" class="play_mini"></a>\W+<h3>\W+<a[^<]+</a>\W+</h3>\W+<p>([^<]+)</p>[^<]+<span>([^<]+)<'
    patron  = '<li id="video-(\d+)" class="videoThumbnail">[^<]+'
    patron += '<div>[^<]+'
    patron += "<a.*?href='([^']+)'[^>]+>[^<]+"
    patron += '<img src="([^"]+)" alt="([^"]+)"[^>]+>[^<]+'
    patron += '<img alt="Reproducir"[^<]+'
    patron += '</a>[^<]+'
    patron += '<h3>[^<]+'
    patron += '<a[^>]+>([^<]+)</a>[^<]+'
    patron += '</h3>[^<]+'
    patron += '<p>([^<]+)</p>[^<]+'
    patron += '<span>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    anyadevideos(matches,itemlist,item)

    # Extrae los videos del resto de páginas
    logger.info("Paginación...")
    '''
    <a href="/alacarta/todos/recomendados/2.html"  class="">
      Adelante
    </a>
    '''
    patronpaginas = '<a href="([^"]+)"  class="">\s+Adelante\s+</a>'
    paginas = re.compile(patronpaginas,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(paginas)

    # Hay al menos otra página
    while len(paginas)>0:
        urlpagina = urlparse.urljoin(item.url,paginas[0])
        logger.info("urlpagina="+urlpagina)
        datapagina = scrapertools.cachePage(urlpagina)
        matches = re.compile(patron,re.DOTALL).findall(datapagina)
        anyadevideos(matches,itemlist,item)
        paginas = re.compile(patronpaginas,re.DOTALL).findall(datapagina)

    return itemlist

def anyadevideos(matches,itemlist,item):
    #if DEBUG: scrapertools.printMatches(matches)

    '''
    patron  = '<li id="video-(\d+)" class="videoThumbnail">[^<]+'   [0] 244902
    patron += '<div>[^<]+'
    patron += "<a.*?href='([^']+)'[^>]+>[^<]+"                        [1] .shtml
    patron += '<img src="([^"]+)" alt="([^"]+)"[^>]+>[^<]+'            [2] .jpg [3] Telediario Internacional Edición 18 horas (10/04/10)
    patron += '<img alt="Reproducir"[^<]+'
    patron += '</a>[^<]+'
    patron += '<h3>[^<]+'
    patron += '<a[^>]+>([^<]+)</a>[^<]+'                            [4] TD Internacional 18h (10/04/10)
    patron += '</h3>[^<]+'        
    patron += '<p>([^<]+)</p>[^<]+'                                    [5] Polonia, de luto. El presidente del Parlamento asume las funciones de Kaczynski. 
    patron += '<span>([^<]+)<'                                        [6] Emitido: 10/04/2010 / 18:00h
    '''

    for match in matches:
        # Extrae los datos
        patron = "Emitido:\s+([^\s]+)\s+\/\s+(\d+)\:(\d+)h"
        fechahora = re.compile(patron,re.DOTALL).findall(match[6])
        #if DEBUG: scrapertools.printMatches(fechahora)

        if len(fechahora)>0:
            scrapedtitle = scrapertools.entityunescape(match[4] + " ("+fechahora[0][0]+")")# (" + fechahora[0][1]+"'"+fechahora[0][2]+'")')
        else:
            scrapedtitle = scrapertools.entityunescape(match[4])
        scrapedurl = urlparse.urljoin("http://www.rtve.es",match[1])

        scrapedthumbnail = "http://www.rtve.es%s" % match[2]
        scrapedplot = scrapertools.entityunescape(match[3].strip()+"\n"+match[5].strip())

        # Ajusta el encoding a UTF-8
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedplot = unicode( scrapedplot, "iso-8859-1" , errors="replace" ).encode("utf-8")
        
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="getvideo" , url=scrapedurl, thumbnail=scrapedthumbnail , plot=scrapedplot , server = "directo" , show = item.title , folder=True) )

'''
def play(params,url,category):
    logger.info("[rtve.py] play")

    title = unicode( xbmc.getInfoLabel( "ListItem.Title" ), "utf-8" )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    server = "Directo"

    # Abre dialogo
    dialogWait = xbmcgui.DialogProgress()
    dialogWait.create( 'Descargando datos del vídeo...', title )

    # --------------------------------------------------------
    # Descarga pagina detalle
    # --------------------------------------------------------
    data = scrapertools.cachePage(url)
    patron = '<location>([^<]+)</location>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    try:
        #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
        url = matches[0]
    except:
        url = ""
    logger.info("[rtve.py] url="+url)

    # Cierra dialogo
    dialogWait.close()
    del dialogWait

    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot)
'''
def getvideo(item):
    logger.info("[rtve.py] play")

    # Extrae el código
    #http://www.rtve.es/mediateca/videos/20100410/telediario-edicion/741525.shtml
    logger.info("url="+item.url)
    patron = 'http://.*?/([0-9]+).shtml'
    data = item.url
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    codigo = matches[0]
    logger.info("assetid="+codigo)

    try:
        # Compone la URL
        #http://www.rtve.es/swf/data/es/videos/alacarta/5/2/5/1/741525.xml
        url = 'http://www.rtve.es/swf/data/es/videos/alacarta/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/'+codigo+'.xml'
        logger.info("[rtve.py] url="+url)

        # Descarga el XML y busca el vídeo
        #<file>rtmp://stream.rtve.es/stream/resources/alacarta/flv/6/9/1270911975696.flv</file>
        data = scrapertools.cachePage(url)
        patron = '<file>([^<]+)</file>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
        url = matches[0]
    except:
        url = ""
    
    # Hace un segundo intento
    if url=="":
        try:
            # Compone la URL
            #http://www.rtve.es/swf/data/es/videos/video/0/5/8/0/500850.xml
            url = 'http://www.rtve.es/swf/data/es/videos/video/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/'+codigo+'.xml'
            logger.info("[rtve.py] url="+url)

            # Descarga el XML y busca el vídeo
            #<file>rtmp://stream.rtve.es/stream/resources/alacarta/flv/6/9/1270911975696.flv</file>
            data = scrapertools.cachePage(url)
            patron = '<file>([^<]+)</file>'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
            url = matches[0]
        except:
            url = ""
    
    if url=="":

        try:
            # Compone la URL
            #http://www.rtve.es/swf/data/es/videos/video/0/5/8/0/500850.xml
            url = 'http://www.rtve.es/swf/data/es/videos/video/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/'+codigo+'.xml'
            logger.info("[rtve.py] url="+url)

            # Descarga el XML y busca el assetDataId
            #<plugin ... assetDataId::576596"/>
            data = scrapertools.cachePage(url)
            #logger.info("[rtve.py] data="+data)
            patron = 'assetDataId\:\:([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
            codigo = matches[0]
            logger.info("assetDataId="+codigo)
            
            #url = http://www.rtve.es/scd/CONTENTS/ASSET_DATA_VIDEO/6/9/5/6/ASSET_DATA_VIDEO-576596.xml
            url = 'http://www.rtve.es/scd/CONTENTS/ASSET_DATA_VIDEO/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/ASSET_DATA_VIDEO-'+codigo+'.xml'
            logger.info("[rtve.py] url="+url)
            
            data = scrapertools.cachePage(url)
            #logger.info("[rtve.py] data="+data)
            patron  = '<field>[^<]+'
            patron += '<key>ASD_FILE</key>[^<]+'
            patron += '<value>([^<]+)</value>[^<]+'
            patron += '</field>'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            codigo = matches[0]
            logger.info("[rtve.py] url="+url)
            
            #/deliverty/demo/resources/mp4/4/3/1290960871834.mp4
            #http://media4.rtve.es/deliverty/demo/resources/mp4/4/3/1290960871834.mp4
            #http://www.rtve.es/resources/TE_NGVA/mp4/4/3/1290960871834.mp4
            url = "http://www.rtve.es/resources/TE_NGVA"+codigo[-26:]

        except:
            url = ""
    logger.info("[rtve.py] url="+url)

    itemlist = []
    if url=="":
        itemlist.append( Item(channel=CHANNELNAME, title="No disponible" , folder=False) )
    else:
        itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=item.thumbnail , plot=item.plot , server = "directo" , show = item.title , folder=False) )

    return itemlist