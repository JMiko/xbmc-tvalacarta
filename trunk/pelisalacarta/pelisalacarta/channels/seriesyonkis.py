# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesyonkis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por Truenon y Jes�s
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "seriesyonkis"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[seriesyonkis.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="lastepisodes"      , title="�timos cap�tulos" , url="http://www.seriesyonkis.com/ultimos-capitulos"))
    itemlist.append( Item(channel=CHANNELNAME, action="listalfabetico"    , title="Listado alfabetico", url="http://www.seriesyonkis.com"))
    #itemlist.append( Item(channel=CHANNELNAME, action="alltvserieslist"   , title="Listado completo de series"))
    #itemlist.append( Item(channel=CHANNELNAME, action="allcartoonslist"    , title="Listado completo de dibujos animados"))
    #itemlist.append( Item(channel=CHANNELNAME, action="allanimelist"   , title="Listado completo de anime"))
    #itemlist.append( Item(channel=CHANNELNAME, action="allminilist"    , title="Listado completo de miniseries"))
    itemlist.append( Item(channel=CHANNELNAME, action="mostviewed"    , title="Series m�s vistas", url="http://www.seriesyonkis.com/series-mas-vistas"))
    #itemlist.append( Item(channel=CHANNELNAME, action="minivideos"    , title="Listado completo de minivideos", url = BASE_URL + "/minivideos"))
    itemlist.append( Item(channel=CHANNELNAME, action="search"    , title="Buscar", url="http://www.seriesyonkis.com/buscar/serie"))

    return itemlist

def search(item,texto):
    logger.info("[seriesyonkis.py] search")
    itemlist = []

    if item.url=="":
        item.url = "http://www.seriesyonkis.com/buscar/serie"
    url = "http://www.seriesyonkis.com/buscar/serie" # write ur URL here
    post = 'keywords='+texto 
    
    data = scrapertools.cache_page(url,post=post)
    patron = '<li class="[^"]+"> <a title="([^"]+)" href="([^"]+)"><img width="[^"]+" height="[^"]+" class="thumb" src="([^"]+)"></a> <h3><a[^>]+>[^<]+</a></h3> <p>([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[0]
        scrapedurl = urlparse.urljoin(item.url,match[1])
        scrapedthumbnail = match[2]
        scrapedplot = match[3]
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=CHANNELNAME, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def lastepisodes(item):
    logger.info("[seriesyonkis.py] lastepisodes")

    data = scrapertools.cache_page(item.url)

    #<li class="thumb-episode "> <a href="/capitulo/strike-back/project-dawn-part-3/200215"><img class="img-shadow" src="/img/series/170x243/strike-back.jpg" height="166" width="115"></a> <div class="transparent"> <a href="/capitulo/strike-back/project-dawn-part-3/200215"><span>2x03</span></a> </div> <strong><a href="/serie/strike-back" title="Strike back">Strike back</a></strong> </li>
    matches = re.compile('<li class="thumb-episode ">.*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        
        #<li class="thumb-episode "> <a href="/capitulo/strike-back/project-dawn-part-3/200215"><img class="img-shadow" src="/img/series/170x243/strike-back.jpg" height="166" width="115"></a> <div class="transparent"> <a href="/capitulo/strike-back/project-dawn-part-3/200215"><span>2x03</span></a> </div> <strong><a href="/serie/strike-back" title="Strike back">Strike back</a></strong> </li>
        datos = re.compile('<a href="([^"]+)">.*?src="([^"]+)".*?<span>([^<]+)</span>.*?title="([^"]+)"', re.S).findall(match)
    
        for capitulo in datos:        
            scrapedtitle = capitulo[3] + " " + capitulo[2] 
            scrapedurl = urlparse.urljoin( item.url , capitulo[0] )
            scrapedthumbnail = item.url + capitulo[1]            
            scrapedplot = ""
    
            # Depuracion
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
            itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist  

def mostviewed(item):
    logger.info("[seriesyonkis.py] mostviewed")
    data = scrapertools.cachePage(item.url)

    #<li class="thumb-episode"> <a href="/serie/como-conoci-a-vuestra-madre" title="C�mo conoc� a vuestra madre"><img class="img-shadow" src="/img/series/170x243/como-conoci-a-vuestra-madre.jpg" height="166" width="115"></a> <strong><a href="/serie/como-conoci-a-vuestra-madre" title="C�mo conoc� a vuestra madre">C�mo conoc� a vuestra madre</a></strong> </li> 
    matches = re.compile('<li class="thumb-episode"> <a href="([^"]+)" title="([^"]+)".*?src="([^"]+)".*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:               
        scrapedtitle = match[1] 
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[2])
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=CHANNELNAME, action="episodios" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def series(item):
    logger.info("[seriesyonkis.py] series")
    itemlist = []

    data = scrapertools.cachePage(item.url)
   
    #Paginador
    #<div class="paginator"> &nbsp;<a href="/lista-de-series/C/">&lt;</a>&nbsp;<a href="/lista-de-series/C/">1</a>&nbsp;<strong>2</strong>&nbsp;<a href="/lista-de-series/C/200">3</a>&nbsp;<a href="/lista-de-series/C/200">&gt;</a>&nbsp; </div>
    matches = re.compile('<div class="paginator">.*?<a href="([^"]+)">&gt;</a>.*?</div>', re.S).findall(data)
    if len(matches)>0:
        paginador = Item(channel=CHANNELNAME, action="series" , title="!P�gina siguiente" , url=urlparse.urljoin(item.url,matches[0]), thumbnail=item.thumbnail, plot="", extra = "" , show=item.show)
    else:
        paginador = None
    
    if paginador is not None:
        itemlist.append( paginador )

    #<div id="main-section" class="lista-series">.*?</div>
    #matches = re.compile('<div id="main-section" class="lista-series">.*?</div>', re.S).findall(data)
    matches = re.compile('<ul id="list-container".*?</ul>', re.S).findall(data)    
    #scrapertools.printMatches(matches)
    for match in matches:
        data=match
        break
    
    #<li><a href="/serie/al-descubierto" title="Al descubierto">Al descubierto</a></li>
    matches = re.compile('<li>.*?href="([^"]+)".*?title="([^"]+)".*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)

    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, action="episodios" , title=match[1] , url=urlparse.urljoin(item.url,match[0]), thumbnail="", plot="", extra = "" , show=item.show))

    if paginador is not None:
        itemlist.append( paginador )

    return itemlist

def episodios(item):
    logger.info("[seriesyonkis.py] episodios")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Obtiene el thumbnail
    #<div class="profile-info"> <a href="/serie/el-barco"> <img src="/img/series/170x243/el-barco.jpg" alt="El Barco" class="profile-img img-shadow" height="243" width="170"> </a>  </div>
    matches = re.compile('<div class="profile-info">.*?<img src="([^"]+)".*?</div>', re.S).findall(data)
    if len(matches)>0:
        thumbnail = urlparse.urljoin(item.url,matches[0])

    #<h2 class="header-subtitle">Capítulos</h2> <ul class="menu"> 
    #<h2 class="header-subtitle">Cap.*?</h2> <ul class="menu">.*?</ul>
    matches = re.compile('<h2 class="header-subtitle">Cap.*?</h2> <ul class="menu">.*?</ul>', re.S).findall(data)
    if len(matches)>0:
        data = matches[0]
    #<li.*?
    matches = re.compile('<li.*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)
        
    itemlist = []  

    No = 0
    for match in matches:
        itemlist.extend( addChapters(Item(url=item.url,extra=match, thumbnail=thumbnail)) )
        '''
        if(len(matches)==1):
            itemlist = addChapters(Item(url=match, thumbnail=thumbnail))
        else:
            # A�ade al listado de XBMC
            No = No + 1
            title = "Temporada "+str(No)
            itemlist.append( Item(channel=CHANNELNAME, action="season" , title= title, url=match, thumbnail=thumbnail, plot="", show = title, folder=True))
        '''

    return itemlist

def addChapters(item):
    #<tr > <td class="episode-title"> <span class="downloads allkind" title="Disponibles enlaces a descarga directa y visualizaciones"></span>
    #<a href="/capitulo/bones/capitulo-2/2870"> <strong> 1x02 </strong> - El hombre en la unidad especial de victimas </a> </td> <td> 18/08/2007 </td> <td class="episode-lang">  <span class="flags_peq spa" title="Espa�ol"></span>  </td> <td class="score"> 8 </td> </tr>
    matches = re.compile('<tr[^<]+<td class="episode-title[^<]+<span[^<]+</span[^<]+<a href="([^"]+)"[^<]+<strong>([^<]+)</strong>(.*?)</a>(.*?)</tr>', re.S).findall(item.extra)
    scrapertools.printMatches(matches)
    
    itemlist=[]
    for match in matches:
        url = urlparse.urljoin(item.url,match[0])
        title = match[1].strip()+match[2]

        patron = '<span class="flags[^"]+" title="([^"]+)">'
        flags = re.compile(patron,re.DOTALL).findall(match[3])
        for flag in flags:
            title = title + " ("+flag+")"

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=title, url=url, thumbnail=item.thumbnail, plot="", show = title, folder=True))

    return itemlist

def findvideos(item):
    logger.info("[seriesyonkis.py] findvideos")
    itemlist = []

    try:
        Nro = 0
        fmt=id=""
        
        data = scrapertools.cache_page(item.url)    
        
        #Solo queremos los links de ONLINE
        #matches = re.compile('<h2 class="header-subtitle veronline">.*?<h2 class="header-subtitle descargadirecta">', re.S).findall(data)
        #ONLINE + DESCARGA
        matches = re.compile('<h2 class="header-subtitle veronline">.*?<section class="buy_show">', re.S).findall(data)
        #scrapertools.printMatches(matches)
        
        for match in matches: 
            data = match
        matches = re.compile('<tr>.*?</tr>', re.S).findall(data)
        #scrapertools.printMatches(matches)
    
        for match in matches:
            logger.info(matches)
            #<tr> <td class="episode-server"> <a href="/s/go/674378" title="Reproducir No estamos solos 2x1" target="_blank"><img src="/img/veronline.png" height="22" width="22"> Reproducir</a> </td> <td class="episode-server-img"><a href="/s/go/674378" title="Reproducir No estamos solos 2x1" target="_blank"><span class="server megavideo"></span></a></td> <td class="episode-lang"><span class="flags esp" title="Español">esp</span></td> <td class="center"><span class="flags no_sub" title="Sin subtítulo o desconocido">no</span></td> <td> <span class="episode-quality-icon" title="Calidad del episodio"> <i class="sprite quality5"></i> </span> </td> <td class="episode-uploader">aritzatila</td> <td class="center"><a href="#" class="errorlink" data-id="674378"><img src="/img/icons/bug.png" alt=""></a></td> </tr> 
            datos = re.compile('<a href="/s/go/([^"]+)".*?<span class="server ([^"]+)".*?title="[^"]+">([^<]+)</span>.*?"flags ([^_]+)_sub".*?class="sprite quality([^"]+)"', re.S).findall(match)
            for info in datos:  
                id = info[0]
                servidor = info[1]
                Nro = Nro + 1
                fmt = info[4]      
                audio = "Audio:" + info[2]
                subs = "Subs:" + info[3]
                url = urlparse.urljoin(item.url,"/s/y/"+id)
                scraptedtitle = "%02d) [%s %s] - (Q:%s) [%s] " % (Nro , audio,subs,fmt,servidor)
                itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scraptedtitle , url=url, thumbnail=item.thumbnail, plot=item.plot, folder=False))
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )

    return itemlist

def play(item):
    logger.info("[seriesyonkis.py] play")
    itemlist = []
    '''
    url = urlparse.urljoin(item.url,"/s/go/"+id)
    data = scrapertools.cachePage(item.url)
    matches = re.compile('<td class="title">Duraci.*?</td><td>([^/]+)/ .*?</td></tr>', re.S).findall(data)
    duracion = ""
    try:
        for match in matches: 
            duracion = match.strip()  
            break
    except:
        duration = ""
    '''
    try:
        data = scrapertools.cache_page(item.url)
        videos = servertools.findvideos(data) 
        if(len(videos)>0): 
            url = videos[0][1]
            server=videos[0][2]                   
            itemlist.append( Item(channel=CHANNELNAME, action="play" , title=item.title , url=url, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
    
    return itemlist

def listalfabetico(item):
    logger.info("[seriesyonkis.py] listalfabetico")
       
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="0-9", url="http://www.seriesyonkis.com/lista-de-series/0-9"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="A"  , url="http://www.seriesyonkis.com/lista-de-series/A"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="B"  , url="http://www.seriesyonkis.com/lista-de-series/B"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="C"  , url="http://www.seriesyonkis.com/lista-de-series/C"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="D"  , url="http://www.seriesyonkis.com/lista-de-series/D"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="E"  , url="http://www.seriesyonkis.com/lista-de-series/E"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="F"  , url="http://www.seriesyonkis.com/lista-de-series/F"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="G"  , url="http://www.seriesyonkis.com/lista-de-series/G"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="H"  , url="http://www.seriesyonkis.com/lista-de-series/H"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="I"  , url="http://www.seriesyonkis.com/lista-de-series/I"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="J"  , url="http://www.seriesyonkis.com/lista-de-series/J"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="K"  , url="http://www.seriesyonkis.com/lista-de-series/K"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="L"  , url="http://www.seriesyonkis.com/lista-de-series/L"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="M"  , url="http://www.seriesyonkis.com/lista-de-series/M"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="N"  , url="http://www.seriesyonkis.com/lista-de-series/N"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="O"  , url="http://www.seriesyonkis.com/lista-de-series/O"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="P"  , url="http://www.seriesyonkis.com/lista-de-series/P"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="Q"  , url="http://www.seriesyonkis.com/lista-de-series/Q"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="R"  , url="http://www.seriesyonkis.com/lista-de-series/R"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="S"  , url="http://www.seriesyonkis.com/lista-de-series/S"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="T"  , url="http://www.seriesyonkis.com/lista-de-series/T"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="U"  , url="http://www.seriesyonkis.com/lista-de-series/U"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="V"  , url="http://www.seriesyonkis.com/lista-de-series/V"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="W"  , url="http://www.seriesyonkis.com/lista-de-series/W"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="X"  , url="http://www.seriesyonkis.com/lista-de-series/X"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="Y"  , url="http://www.seriesyonkis.com/lista-de-series/Y"))
    itemlist.append( Item(channel=CHANNELNAME, action="series" , title="Z"  , url="http://www.seriesyonkis.com/lista-de-series/Z"))

    return itemlist

















 


def minivideos(item):
    logger.info("[seriesyonkis.py] minivideos")
    data = scrapertools.cachePage(item.url)

    #<article class="minivideo "> <a href="/minivideo/ver/cine/430365"> <img src="http://blackbird.zoomin.tv/Images/.jpg?imageurl=http://bongo.zoomin.tv/uploaded/assetimages/2011/08/26/430365.jpg&amp;width=169&amp;height=125" alt="Estreno: Dinero f�cil" height="125" width="169"> </a> <p class="titulo">Estreno: Dinero f�cil</p> </article>
    matches = re.compile('<article class="minivideo "> <a href="([^"]+)".*?src="([^"]+)".*?alt="([^"]+)".*?</article>', re.S).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:               
        scrapedtitle = match[2] 
        # URL
        scrapedurl = match[0]            
        # Thumbnail
        scrapedthumbnail = match[1]            
        # procesa el resto
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=CHANNELNAME, action="temporadas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def alltvserieslist(params,url,category):
    allserieslist(params,url,category,"series")

def allcartoonslist(params,url,category):
    allserieslist(params,url,category,"dibujos")

def allanimelist(params,url,category):
    allserieslist(params,url,category,"anime")

def allminilist(params,url,category):
    allserieslist(params,url,category,"miniseries")

def allserieslist(params,url,category,clave):
    logger.info("[seriesyonkis.py] allserieslist")

    title = urllib.unquote_plus( params.get("title") )

    from core.item import Item

    item = Item(channel=CHANNELNAME, title=title , url=url , extra=clave )
    itemlist = getallserieslist(item)
    
    for item in itemlist:
        xbmctools.addnewfolder(item.channel , item.action , category , item.title , item.url , item.thumbnail, item.plot , item.extra )#, totalItems = item.totalItems)

    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    
def getallserieslist(item):
    logger.info("[seriesyonkis.py] getallserieslist")

    from core.item import Item

    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    #logger.info(data)

    # Extrae el bloque de las series
    patronvideos = '<h4><a.*?id="'+item.extra+'".*?<ul>(.*?)</ul>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    data = matches[0]
    #scrapertools.printMatches(matches)

    # Extrae las entradas (carpetas)
    patronvideos  = '<li class="page_item_"><a href="(http://www.seriesyonkis.com/serie[^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    totalItems = len(matches)

    for match in matches:
        scrapedtitle = match[1]
        scrapedurl = match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        Serie = scrapedtitle    # JUR-Añade nombre serie para librería
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="list" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, extra = Serie , show = scrapedtitle ))#, totalItems = totalItems))

    return itemlist

def detail(params,url,category):
    logger.info("[seriesyonkis.py] detail")
    logger.info("[seriesyonkis.py] detail url="+url)

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    Serie = urllib.unquote_plus( params.get("Serie") )
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    #server = "Megavideo"
    server,url = scrapvideoURL(url) 
    logger.info("[seriesyonkis.py] detail url="+url)
   
    if (":" in url):
        match = url.split(":")
        if match[0]!="http":
            url = choiceOnePart(match)
    logger.info("[seriesyonkis.py] detail url="+url)

    if url == "":return
   
    logger.info("[seriesyonkis.py] url="+url)
   
    xbmctools.playvideo(CHANNELNAME,server,url,category,title,thumbnail,plot,Serie=Serie)
    # ------------------------------------------------------------------------------------

def addlist2Library(params,url,category):
    logger.info("[seriesyonkis.py] addlist2Library")

    # Descarga la página
    data = scrapertools.cachePage(url)
    #logger.info(data)

    if params.has_key("Serie"):
        Serie = params.get("Serie")
    else:
        Serie = ""

    if params.has_key("server"):
        server = params.get("server")
    else:
        server = ""

    if params.has_key("thumbnail"):
        thumbnail = params.get("thumbnail")
    else:
        thumbnail = ""

    # Extrae las entradas (carpetas)
    patronvideos  = '<a href="(http://www.seriesyonkis.com/capitulo[^"]+)"[^>]+>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create('pelisalacarta', 'Añadiendo episodios...')
    pDialog.update(0, 'Añadiendo episodio...')
    totalepisodes = len(matches)
    logger.info ("[seriesyonkis.py - addlist2Library] Total Episodios:"+str(totalepisodes))
    i = 0
    errores = 0
    nuevos = 0
    for match in matches:
        # Titulo
        scrapedtitle = match[1]

        # PARTE NUEVA 

        # Nos quedamos por un lado con el nombre de la serie y 
        # por otro con el num capitulo

        mo = re.match("^(.*) ([\d]{1,2}[x|X][\d]{1,3}) (.*)$", scrapedtitle)

        if mo == None:
                errores = errores + 1
                continue        

        if (DEBUG):
                xbmc.output("CAPITULO="+ mo.group(2))                
    
    
        scrapedtitle = mo.group(2)

        # FIN PARTE NUEVA

        i = i + 1
        pDialog.update(i*100/totalepisodes, 'Añadiendo episodio...',scrapedtitle)
        if (pDialog.iscanceled()):
            return

        # URL
        #  Tenemos 2 opciones. Scrapear todos los episodios en el momento de añadirlos 
        #  a la biblioteca o bien dejarlo para cuando se vea cada episodio. Esto segundo
        #  añade los episodios mucho más rápido, pero implica añadir una función
        #  strm_detail en cada módulo de canal. Por el bien del rendimiento elijo la
        #  segunda opción de momento (hacer la primera es simplemente descomentar un par de
        #  líneas.
        #  QUIZÁ SEA BUENO PARAMETRIZARLO (PONER OPCIÓN EN LA CONFIGURACIÓN DEL PLUGIN)
        #  PARA DEJAR QUE EL USUARIO DECIDA DONDE Y CUANDO QUIERE ESPERAR.
        url = match [0]
        # JUR-Las 3 líneas siguientes son para OPCIÓN 1
        #scrapedurl = scrapvideoURL(url)
        #if scrapedurl == "":
        #    errores = errores + 1
            
        # Thumbnail
        scrapedthumbnail = ""
        
        # procesa el resto
        scrapedplot = ""
        # Depuracion
        if (DEBUG):
            logger.info("scrapedtitle="+scrapedtitle)
#            logger.info("scrapedurl="+scrapedurl) #OPCION 1.
            logger.info("url="+url) #OPCION 2.
            logger.info("scrapedthumbnail="+scrapedthumbnail)
            logger.info("Serie="+Serie)
            logger.info("Episodio "+str(i)+" de "+str(totalepisodes)+"("+str(i*100/totalepisodes)+"%)")

        # Añade a la librería #Comentada la opción 2. Para cambiar invertir los comentarios
        #OPCION 1:
        #library.savelibrary(scrapedtitle,scrapedurl,scrapedthumbnail,server,scrapedplot,canal=CHANNELNAME,category="Series",Serie=Serie,verbose=False)
        #OPCION 2
        try:
            nuevos = nuevos + library.savelibrary(scrapedtitle,url,scrapedthumbnail,server,scrapedplot,canal=CHANNELNAME,category="Series",Serie=Serie,verbose=False,accion="strm_detail",pedirnombre=False)
        except IOError:
            logger.info("Error al grabar el archivo "+scrapedtitle)
            errores = errores + 1
        
#    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
    pDialog.close()
    
    #Actualización de la biblioteca
    if errores > 0:
        logger.info ("[seriesyonkis.py - addlist2Library] No se pudo añadir "+str(errores)+" episodios") 
    library.update(totalepisodes,errores,nuevos)

    return nuevos
    

def strm_detail (params,url,category):
    logger.info("[seriesyonkis.py] strm_detail")

    title = urllib.unquote_plus( params.get("title") )
    thumbnail = urllib.unquote_plus( params.get("thumbnail") )
    plot = unicode( xbmc.getInfoLabel( "ListItem.Plot" ), "utf-8" )
    #server = "Megavideo"
    # ------------------------------------------------------------------------------------
    # Busca los enlaces a los videos
    # ------------------------------------------------------------------------------------
    server,url = scrapvideoURL(url)
    if url == "":
        
        return
    logger.info("[seriesyonkis] strm_detail url="+url)
    
    xbmctools.playvideo("STRM_Channel",server,url,category,title,thumbnail,plot,1)
#<td><div align="center"><span style="font-size: 10px"><em><img src="http://simages.peliculasyonkis.com/images/tmegavideo.png" alt="Megavideo" style="vertical-align: middle;" /><img src='http://images.peliculasyonkis.com/images/tdescargar2.png' title='Tiene descarga directa' alt='Tiene descarga directa' style='vertical-align: middle;' /><a onmouseover="window.status=''; return true;" onmouseout="window.status=''; return true;" title="Seleccionar esta visualizacion" href="http://www.seriesyonkis.com/player/visor_pymeno4.php?d=1&embed=no&id=%CB%D8%DC%DD%C0%D3%E2%FC&al=%A6%B2%AC%B8%AC%A4%BD%A4" target="peli">SELECCIONAR ESTA</a> (flash desde megavideo)</em>          </span></div></td>          <td><div align="center"><img height="30" src="http://simages.seriesyonkis.com/images/f/spanish.png" alt="Audio Español" title="Audio Español" style="vertical-align: middle;" /></div></td>
#          <td><div align="center"><span style="font-size: 10px">Español (Spanish)</span></div></td>          <td><div align="center"><span style="font-size: 10px">no</span></div></td>          <td><div align="center"><span style="font-size: 10px">Formato AVI 270mb</span></div></td>          <td><div align="center"><span style="font-size: 10px">MasGlo<br />masglo</span></div></td>        </tr><tr>
 

def scrapvideoURL(urlSY):
    logger.info("[seriesyonkis.py] scrapvideoURL")
    data = scrapertools.cachePage(urlSY)
    patronvideos  = 'href="' + BASE_URL + '/s/go/(mv)\/([^"]+)".*?alt="([^"]+)".*?'
    patronvideos += '<td><div[^>]+><[^>]+>[^<]+</span></div></td>[^<]+<td><div[^>]+><[^>]+>[^<]+</span></div></td>[^<]+'
    patronvideos += '<td><div[^>]+><[^>]+>(.*?)</tr>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    patronvideos  = 'href="' + BASE_URL + '/player/visor_([^\.]+).php.*?id=([^"]+)".*?alt="([^"]+)".*?'
    patronvideos += '<td><div[^>]+><[^>]+>[^<]+</span></div></td>[^<]+<td><div[^>]+><[^>]+>[^<]+</span></div></td>[^<]+'
    patronvideos += '<td><div[^>]+><[^>]+>(.*?)</tr>'
    matches0 = re.compile(patronvideos,re.DOTALL).findall(data)
    matches = matches + matches0
    patronvideos1  = BASE_URL + '/s/go/(d)/(.+?)".*?alt="([^"]+)".*?'
    patronvideos1 += 'Durac.+?:\s?([^>]+?)>'
    matches1 = re.compile(patronvideos1,re.DOTALL).findall(data)
    if (len(matches1) > 0):
        for j in matches1:
            matches.append(j)
    scrapertools.printMatches(matches)
    id=""
    #newdec = Yonkis.DecryptYonkis()
    #xbmc.output(newdec.ccM(newdec.charting(newdec.unescape("%B7%AC%A6%B1%B7%AD%A9%B1"))))
    
    if len(matches)==0:
        xbmctools.alertnodisponible()
        return "",""
        
    elif len(matches)==1:
        if  matches[0][0] == "d":
            player = "descargar"
            url = BASE_URL + "/s/go/%s/%s" % (matches[0][0],matches[0][1])
            id = getId(url)
        elif matches[0][0] == "mv":
            player = "pymeno2"
            url = BASE_URL + "/go/%s/%s" % (matches[0][0],matches[0][1])
            id = getId(url)
        else:
            player = matches[0][0]
            id = matches[0][1]
        server = SERVER[player]
        #print matches[0][1]
        if player == "svueno":
            id = matches[0][1]
            logger.info("[seriesyonkis.py]  id="+id)
            dec = Yonkis.DecryptYonkis()
            id = dec.decryptALT(dec.charting(dec.unescape(id)))
            id = "http://stagevu.com/video/" + id
        elif player in ["pymeno2","pymeno3","pymeno4","pymeno5","pymeno6"]:
            cortar = matches[0][1].split("&")
            id = cortar[0]
            logger.info("[seriesyonkis.py]  id="+id)
            dec = Yonkis.DecryptYonkis()
            id = dec.decryptID_series(dec.unescape(id))
        
        elif player == "descargar":
            cortar = matches[0][1].split("&")
            id = cortar[0]
            logger.info("[seriesyonkis.py]  id="+id)
            dec = Yonkis.DecryptYonkis()
            id = dec.ccM(dec.unescape(id))

        else:pass
        #print 'codigo :%s' %id
        return server,id        
    else:
        
        
            
        server,id = choiceOne(matches)
        if len(id)==0:return "",""
        print 'codigo :%s' %id
        return server,id
        
        
def choiceOne(matches):
    logger.info("[seriesyonkis.py] choiceOne")
    opciones = []
    IDlist = []
    servlist = []
    Nro = 0
    fmt=duracion=id=""
    
    for server,codigo,audio,data in matches:
        try:
            print server
            if server in SERVER:
                servidor = SERVER[server]
                player = server
                id = codigo
            else:
                if server == "d":
                    player = "descargar"
                    id = BASE_URL + "/go/%s/%s" % (server,codigo)
                    
                    servidor = "Megaupload"
                    Server = "megaupload"
                elif server == "mv":
                    player = "pymeno2"
                    id = BASE_URL + "/go/%s/%s" % (server,codigo)
                    
                    servidor = "Megavideo"
                    Server = "megavideo"
                else:
                    servidor = "desconocido ("+server+")"
            Nro = Nro + 1
            
            regexp = re.compile(r"title='([^']+)'")
            match = regexp.search(data)
            if match is not None:
                fmt = match.group(1)
                fmt = fmt.replace("Calidad","").strip()
            regexp = re.compile(r"Duraci\xc3\xb3n:([^<]+)<")
            match = regexp.search(data)
            if match is not None:
                duracion = match.group(1).replace(".",":")        
            audio = audio.replace("Subt\xc3\xadtulos en Espa\xc3\xb1ol","Subtitulado") 
            audio = audio.replace("Audio","").strip()
            opciones.append("%02d) [%s] - (%s) - %s  [%s] " % (Nro , audio,fmt,duracion,servidor))
            IDlist.append(id)
            servlist.append(player)
        except:
            logger.info("[seriesyonkis.py] error (%s)" % server)
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Nº)[AUDIO]-(CALIDAD)-DURACION", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 : return "",""
    
    if servlist[seleccion]  in ["pymeno2","pymeno3","pymeno4","pymeno5","pymeno6"]:
        if "http" in IDlist[seleccion]:
            id = getId(IDlist[seleccion])
        else:
            id = IDlist[seleccion]
        cortar = id.split("&")
        id = cortar[0]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        if(len(id)==51):                     
            id = dec.decryptID(dec.charting(dec.unescape(id)))
        else:
            id = dec.decryptID_series(dec.unescape(id))
    elif servlist[seleccion] == "descargar":
        if "http" in IDlist[seleccion]:
            id = getId(IDlist[seleccion])
        else:
            id = IDlist[seleccion]
        cortar = id.split("&")
        id = cortar[0]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        id = dec.ccM(dec.unescape(id))        
    elif servlist[seleccion] == "svueno":
        id = IDlist[seleccion]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        id = dec.decryptALT(dec.charting(dec.unescape(id)))
        id = "http://stagevu.com/video/" + id
    elif servlist[seleccion] == "movshare":
        id = IDlist[seleccion]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        id = dec.decryptALT(dec.charting(dec.unescape(id)))
    elif servlist[seleccion] == "videoweed":
        id = IDlist[seleccion]
        logger.info("[seriesyonkis.py]  id="+id)
        dec = Yonkis.DecryptYonkis()
        id = dec.decryptID(dec.charting(dec.unescape(id)))
        id = "http://www.videoweed.com/file/%s" %id                
    else:
        pass
    return SERVER[servlist[seleccion]],id

def choiceOnePart(matches):
    logger.info("[seriesyonkis.py] choiceOnePart")
    opciones = []
    Nro = 0
    for codigo in matches:
        Nro = Nro + 1
        opciones.append("Parte %s " % Nro)
       
    dia = xbmcgui.Dialog()
    seleccion = dia.select("Selecciona uno ", opciones)
    logger.info("seleccion=%d" % seleccion)
    if seleccion == -1 : return ""
    id = matches[seleccion]
    return id
    
def getId(url):
    logger.info("[seriesyonkis.py] getId")

    #print url
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        opener = urllib2.build_opener(SmartRedirectHandler())
        response = opener.open(req)
    except ImportError, inst:    
        status,location=inst
        logger.info(str(status) + " " + location)    
        movielink = location
    #print movielink

    try:
        id = re.compile(r'id=([A-Z0-9%]{0,})').findall(movielink)[0]
    except:
        id = ""
    
    return id
    
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        raise ImportError(302,headers.getheader("Location"))