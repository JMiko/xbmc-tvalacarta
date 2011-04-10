# -*- coding: utf-8 -*-
#------------------------------------------------------------
# tvalacarta - XBMC Plugin
# Canal para RTVE
# http://blog.tvalacarta.info/plugin-xbmc/tvalacarta/
#------------------------------------------------------------
import urlparse, re

try:
    from core import config
    from core import logger
    from core import scrapertools
    from core.item import Item
except:
    # En Plex Media server lo anterior no funciona...
    from Code.core import config
    from Code.core import logger
    from Code.core import scrapertools
    from Code.core.item import Item

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
    logger.info("[rtve.py] canal")
    
    # En la paginación la URL vendrá fijada, si no se construye aquí la primera página
    if not item.url.startswith("http"):
        item.url = "http://www.rtve.es/alacarta/programas/"+item.extra+"/?pageSize=100&order=1&criteria=asc&emissionFilter=all"
    logger.info("[rtve.py] programas url="+item.url) 

    '''
    <li class="odd">
    <span class="col_fav">
    <input type="hidden" id="urlAddFav43930" value="/alacarta/videos/buscamundos/"/>
    <input type="hidden" id="titleAddFav43930" value="Buscamundos"/>
    <a class="favoritos" name="43930" title="Añadir a favoritos" href="/usuarios/addToFavorite.shtml?programPermLink=43930" target="_blank"></a>
    </span>
    <span class="col_tit" id="43930" name="progname">
    <a href="/alacarta/videos/buscamundos/" title="Ver programa seleccionado">Buscamundos</a>
    </span>
    <span class="col_fec">pasado martes</span>
    <span class="col_med">
    <a href="/alacarta/tve/la1/" title="Ir a portada de 'La 1'" />
    <img src="/css/alacarta20/i/iconos/mini-cadenas/la1.png"> 
    </a>        
    </span>
    <span class="col_cat">Viajes</span>
    <!--EMPIEZA TOOL-TIP-->
    <div id="popup43930" style="display: none" class="tultip"> 
    <span id="progToolTip" class="tooltip curved">
    <span class="pointer"></span>
    <span class="cerrar" id="close43930"></span>
    <span class="titulo-tooltip"><a href="/alacarta/videos/buscamundos/" title="Ver programa seleccionado">Buscamundos</a></span>
    <span class="fecha">pasado martes</span>
    <span class="detalle">Buscamundos es un programa muy distinto de los tradicionales documentales de viajes. Pretende incitar a los espectadores a viajar más allá de los límites del turismo o la aventura, adentrándose en la vida de las ...</span>
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
    <a href="/alacarta/videos/buscamundos/" title="Buscamundos">Buscamundos</a>
    </li>
    </ul></span>
    </span>
    </div>
    <!--FIN TOOL-TIP--></li>
    '''
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
    patron += '<span class="col_cat">([^<]+)</span>.*?'
    patron += '<span class="detalle">([^<]+)</span>'
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
        scrapedplot = match[5]
        scrapedextra = match[0]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra = scrapedextra, show=scrapedtitle, category = item.category) )

    return itemlist

def videos(item):
    logger.info("[rtve.py] videos")
    
    # En la paginación la URL vendrá fijada, si no se construye aquí la primera página
    if item.url=="":
        # El ID del programa está en item.extra (ej: 42610)
        # La URL de los vídeos de un programa es
        # http://www.rtve.es/alacarta/interno/contenttable.shtml?ctx=42610&pageSize=20&pbq=1
        item.url = "http://www.rtve.es/alacarta/interno/contenttable.shtml?ctx="+item.extra+"&pageSize=20&pbq=1"
    data = scrapertools.cachePage(item.url)
    itemlist = []

    '''
    <li class="odd">
    <!--<span class="col_est partially-played"><em>parcialmente reproducido</em></span>-->
    <span class="col_tit">
    <a href="/alacarta/videos/paisajes-de-la-historia/paisajes-de-la-historia-figuras-femeninas-de-los-anos-veinte-a-la-posguerra/639842/">Figuras femeninas</a>
    </span>
    <span class="col_tip">Completo</span>
    <span class="col_dur">58:43</span>
    <span class="col_pop"><span title="8% popularidad" class="pc8"><em><strong><span>8%</span></strong></em></span></span>
    <span class="col_fec">30 nov 2009</span>
    </li>
    '''
    
    # Extrae los vídeos
    patron  = '<li class="[^"]+">.*?'
    patron += '<span class="col_tit">[^<]+'
    patron += '<a href="([^"]+)">([^<]+)</a>[^<]+'
    patron += '</span>[^<]+'
    patron += '<span class="col_tip">([^<]+)</span>[^<]+'
    patron += '<span class="col_dur">([^<]+)</span>.*?'
    patron += '<span class="col_fec">([^<]+)</span>[^<]+'
    patron += '</li>'
    
    matches = re.findall(patron,data,re.DOTALL)
    if DEBUG: scrapertools.printMatches(matches)

    # Crea una lista con las entradas
    for match in matches:
        scrapedtitle = match[1]+" ("+match[2]+") ("+match[3]+") ("+match[4]+")"
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = ""
        scrapedplot = match[0]
        scrapedextra = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="play" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , show=item.show, category = item.category, folder=False) )

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
        itemlist.append( Item(channel=CHANNELNAME, title=scrapedtitle , action="videos" , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot , extra = scrapedextra, category = item.category, show=item.show) )

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
    logger.info("assetid="+codigo)
    
    thumbnail = item.thumbnail

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

    itemlist = []
    if url=="":
        title="No disponible"
    itemlist.append( Item(channel=CHANNELNAME, title=item.title , action="play" , url=url, thumbnail=thumbnail , plot=item.plot , server = "directo" , show = item.title , folder=False) )

    return itemlist