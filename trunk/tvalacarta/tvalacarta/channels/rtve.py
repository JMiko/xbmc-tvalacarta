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
    '''
    <div class="basicmod modVideo">
    <span class="ico">vídeo</span>
    <span class="img">
    <a id="PS4" name="thumbID" href="/alacarta/videos/sorteos/" title='Ver Sorteos'>
    <img title='Ver Sorteos' alt="Sorteos" src="/imagenes/la-suerte-en-tus-manos-18-03-11/1300483695180.jpg"/>
    </a>
    </span>
    <div class="txt">
    <h4>
    <span class="titu">
    <a href="/alacarta/videos/sorteos/" title='Ver Sorteos'>Sorteos</a>
    </span>
    </h4>
    <h5>
    <span class="titu">
    <em>Último: </em><strong><a title='Ver La suerte en tus...' href="/alacarta/videos/sorteos/la-suerte-en-tus-manos-18-03-11/1049398/">La suerte en tus...</a></strong>
    </span>
    </h5>
    <p>15:52 - ayer</p>
    </div>
    <div id="popupPS4" style="display: none" class="tultip"> 
    <span class="tooltip curved"> 
    <span class="pointer"></span>
    <span class="cerrar" id="closePS4"></span> 
    <span class="titulo-tooltip"><a href="/alacarta/videos/sorteos/">Sorteos</a></span> 
    <span class="fecha">ayer</span> 
    <span class="detalle"> </span>
    <span class="miga">
    <ul>
    <li>
    <a href="/alacarta/tve/" title="Televisión">Televisión</a>
    </li>
    <li>
    <span> &rsaquo; </span>
    <a href="/alacarta/tve/la2/" title="La 2">La 2</a>
    </li>
    <li>
    <span> &rsaquo; </span>
    <a href="/alacarta/videos/sorteos/" title="Sorteos">Sorteos</a>
    </li>
    </ul></span>
    </span>
    </div>
    '''
    
    '''
    <div class="basicmod modVideo">
    <span class="ico">vídeo</span>
    <span class="img">
    
    <a id="PS2" name="thumbID" href="/alacarta/videos/el-tiempo/" title='Ver El tiempo'>
    <img title='Ver El tiempo' alt="El tiempo" src="/imagenes/el-tiempo-la-primavera-llega-con-un-descenso-ligero-de-las-temperaturas/1300628498031.jpg"/>
    </a>
    </span>
    <div class="txt">
    <h4>
    <span class="titu">
    <a href="/alacarta/videos/el-tiempo/" title='Ver El tiempo'>El tiempo</a>
    
    </span>
    </h4>
    <h5>
    <span class="titu">
    <em>Último: </em><strong><a title='Ver La primavera llega con nubes ' href="/alacarta/videos/el-tiempo/el-tiempo-la-primavera-llega-con-un-descenso-ligero-de-las-temperaturas/1050008/">La primavera llega con nubes </a></strong>
    </span>
    </h5>
    <p>3:00 - hoy</p>
    
    </div>
    <div id="popupPS2" style="display: none" class="tultip"> 
    <span class="tooltip curved"> 
    <span class="pointer"></span>
    <span class="cerrar" id="closePS2"></span> 
    <span class="titulo-tooltip"><a href="/alacarta/videos/el-tiempo/">El tiempo</a></span> 
    <span class="fecha">hoy</span> 
    <span class="detalle">Las próximas horas destacan una permanencia anticiclónica pero con un aumento de la nubosidad, sobre todo de evolución por las tardes que podrán traer tormentas en los sistemas montañosos. El lunes las precipitac...</span>
    <span class="miga">
    <ul>
    
    <li>
    <a href="/alacarta/tve/" title="Televisión">Televisión</a>
    </li>
    <li>
    <span> &rsaquo; </span>
    <a href="/alacarta/tve/la1/" title="La 1">La 1</a>
    </li>
    
    <li>
    <span> &rsaquo; </span>
    <a href="/alacarta/videos/el-tiempo/" title="El tiempo">El tiempo</a>
    </li>
    </ul></span>
    </span>
    </div>

    '''
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
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = item.thumbnail
        scrapedplot = scrapertools.unescape(match[5].strip())
        scrapedplot = scrapertools.htmlclean(scrapedplot).strip()
        scrapedextra = match[2]
        
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show, category = item.category, extra=scrapedextra, folder=False) )

    # Extrae la paginación
    patron = '<a name="paginaIR" href="([^"]+)"><span>Siguiente</span></a>'
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    # Crea una lista con las entradas
    for match in matches:
        scrapedtitle = "!Página siguiente"
        scrapedurl = urlparse.urljoin(item.url,match).replace("&amp;","&")
        scrapedthumbnail = ""
        scrapedplot = ""
        scrapedextra = item.extra
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="episodios" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra = scrapedextra, category = item.category, show=item.show) )

    return itemlist

def play(item):
    logger.info("[rtve.py] play")

    # Extrae el código
    #http://www.rtve.es/mediateca/videos/20100410/telediario-edicion/741525.shtml
    #http://www.rtve.es/alacarta/videos/espana-entre-el-cielo-y-la-tierra/espana-entre-el-cielo-y-la-tierra-la-mancha-por-los-siglos-de-los-siglos/232969/
    logger.info("url="+item.url)
    patron = 'http://.*?/([0-9]+)/'
    data = item.url
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    codigo = matches[0]
    url=""
    itemlist = []
    logger.info("assetid="+codigo)
    
    thumbnail = item.thumbnail

    if url=="":
        logger.info("[rtve.py] Probando nuevo sistema")

        # Ponemos el id en el siguiente enlace
        url = "http://www.rtve.es/ztnr/?idasset="+codigo
        logger.info("url="+url)
        data = scrapertools.cache_page(url)
        logger.info("data="+data)

        # Cuando la página carga nos muestra el nuevo id
        category = scrapertools.get_match(data,"<td>Category</td>[^<]+<th>([^<]+)</th>")
        
        patron  = '<td\s+class="s\d+">(\d+)</td>[^<]+'
        patron += '<td\s+class="s\d+">([^<]+)</td>[^<]+'
        patron += '<td\s+class="s\d+">([^<]+)</td>[^<]+'
        patron += '<td\s+class="s\d+">([^<]+)</td>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        for idpreset,videoaudio,tipo,lenguaje in matches:
            
            # Ponemos el nuevo id en el siguiente enlace:
            #http://www.rtve.es/ztnr/preset.jsp?idpreset=910988&lenguaje=es&tipo=video
            url = "http://www.rtve.es/ztnr/preset.jsp?idpreset="+idpreset+"&lenguaje="+lenguaje+"&tipo="+videoaudio
            logger.info("url="+url)
            data = scrapertools.cache_page(url)
            logger.info("data="+data)

            # De ahí sacamos el video
            # <li><em>File Name</em>&nbsp;<span class="titulo">mp4/4/1/1340907208714.mp4</span></li>
            finalurl = scrapertools.get_match(data,'<li><em>File Name</em>&nbsp;<span class="titulo">([^<]+)</span></li>')
            
            # Ahora solo nos falta el principio del enlace y quedaría así:
            url = "http://www.rtve.es/resources/"+category+"/"+finalurl
            logger.info("url="+url)
            
            itemlist.append( Item(channel=CHANNELNAME, title=tipo+" "+item.title , action="play" , url=url, thumbnail=thumbnail , plot=item.plot , server = "directo" , show = item.title , folder=False) )
    
    if url=="":
        try:
            # Compone la URL
            #http://www.rtve.es/swf/data/es/videos/alacarta/5/2/5/1/741525.xml
            url = 'http://www.rtve.es/swf/data/es/videos/alacarta/'+codigo[-1:]+'/'+codigo[-2:-1]+'/'+codigo[-3:-2]+'/'+codigo[-4:-3]+'/'+codigo+'.xml'
            logger.info("[rtve.py] url="+url)
    
            # Descarga el XML y busca el vídeo
            #<file>rtmp://stream.rtve.es/stream/resources/alacarta/flv/6/9/1270911975696.flv</file>
            data = scrapertools.cachePage(url)
            #print url
            #print data
            patron = '<file>([^<]+)</file>'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            if len(matches)>0:
                #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
                url = matches[0]
            else:
                url = ""
            
            patron = '<image>([^<]+)</image>'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            #print len(matches)
            #url = matches[0].replace('rtmp://stream.rtve.es/stream/','http://www.rtve.es/')
            thumbnail = matches[0]
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

    '''
    if url=="":
        logger.info("[rtve.py] Extrayendo URL tipo iPad")
        headers = []
        headers.append( ["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"] )
        location = scrapertools.get_header_from_response(item.url,headers=headers,header_to_get="location")
        logger.info("[rtve.py] location="+location)
        
        data = scrapertools.cache_page(location,headers=headers)
        logger.info("[rtve.py] data="+data)
        #<a href="/usuarios/sharesend.shtml?urlContent=/resources/TE_SREP63/mp4/4/8/1334334549284.mp4" target
        url = scrapertools.get_match(data,'<a href="/usuarios/sharesend.shtml\?urlContent\=([^"]+)" target')
        logger.info("[rtve.py] url="+url)
        #http://www.rtve.es/resources/TE_NGVA/mp4/4/8/1334334549284.mp4
        url = urlparse.urljoin("http://www.rtve.es",url)
        logger.info("[rtve.py] url="+url)
    '''

    if len(itemlist)==0 and url!="":
        itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=thumbnail , plot=item.plot , server = "directo" , show = item.title , folder=False) )

    return itemlist