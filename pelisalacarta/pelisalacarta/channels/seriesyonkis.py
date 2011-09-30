# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesyonkis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por Truenon y Jesus, modificada por Boludiko
# v8
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
    itemlist.append( Item(channel=CHANNELNAME, action="lastepisodes"      , title="Útimos capítulos" , url="http://www.seriesyonkis.com/ultimos-capitulos"))
    itemlist.append( Item(channel=CHANNELNAME, action="listalfabetico"    , title="Listado alfabetico", url="http://www.seriesyonkis.com"))
    itemlist.append( Item(channel=CHANNELNAME, action="mostviewed"    , title="Series más vistas", url="http://www.seriesyonkis.com/series-mas-vistas"))
    itemlist.append( Item(channel=CHANNELNAME, action="search"    , title="Buscar", url="http://www.seriesyonkis.com/buscar/serie"))

    return itemlist

def search(item,texto):
    logger.info("[seriesyonkis.py] search")
    itemlist = []

    if item.url=="":
        item.url = "http://www.seriesyonkis.com/buscar/serie"
    url = "http://www.seriesyonkis.com/buscar/serie" # write ur URL here
    post = 'keywords='+texto[0:18]
    
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

    #<li class="thumb-episode"> <a href="/serie/como-conoci-a-vuestra-madre" title="Cómo conocí a vuestra madre"><img class="img-shadow" src="/img/series/170x243/como-conoci-a-vuestra-madre.jpg" height="166" width="115"></a> <strong><a href="/serie/como-conoci-a-vuestra-madre" title="Cómo conocí a vuestra madre">Cómo conocí a vuestra madre</a></strong> </li> 
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
        paginador = Item(channel=CHANNELNAME, action="series" , title="!Página siguiente" , url=urlparse.urljoin(item.url,matches[0]), thumbnail=item.thumbnail, plot="", extra = "" , show=item.show)
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
        itemlist.append( Item(channel=CHANNELNAME, action="episodios" , title=match[1] , url=urlparse.urljoin(item.url,match[0]), thumbnail="", plot="", extra = "" , show=match[1] ))

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

    #<h2 class="header-subtitle">CapÃ­tulos</h2> <ul class="menu"> 
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
        itemlist.extend( addChapters(Item(url=item.url,extra=match, thumbnail=thumbnail,show=item.show)) )
        '''
        if(len(matches)==1):
            itemlist = addChapters(Item(url=match, thumbnail=thumbnail))
        else:
            # Añade al listado de XBMC
            No = No + 1
            title = "Temporada "+str(No)
            itemlist.append( Item(channel=CHANNELNAME, action="season" , title= title, url=match, thumbnail=thumbnail, plot="", show = title, folder=True))
        '''

    if config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee"):
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def addChapters(item):
    #<tr > <td class="episode-title"> <span class="downloads allkind" title="Disponibles enlaces a descarga directa y visualizaciones"></span>
    #<a href="/capitulo/bones/capitulo-2/2870"> <strong> 1x02 </strong> - El hombre en la unidad especial de victimas </a> </td> <td> 18/08/2007 </td> <td class="episode-lang">  <span class="flags_peq spa" title="Español"></span>  </td> <td class="score"> 8 </td> </tr>
    matches = re.compile('<tr[^<]+<td class="episode-title.*?<a href="([^"]+)"[^<]+<strong>([^<]+)</strong>(.*?)</a>(.*?)</tr>', re.S).findall(item.extra)
    scrapertools.printMatches(matches)
    
    itemlist=[]
    for match in matches:
        url = urlparse.urljoin(item.url,match[0])
        title = match[1].strip()+match[2]

        patron = '<span class="flags[^"]+" title="([^"]+)">'
        flags = re.compile(patron,re.DOTALL).findall(match[3])
        for flag in flags:
            title = title + " ("+flag+")"

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=title, url=url, thumbnail=item.thumbnail, plot="", show = item.show, folder=True))

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
        #logger.info("1")
        if len(matches)==0:
            logger.info("no encuentra cabecera 1")
        else:
            data = matches[0]
        #logger.info("2")
        
        matches = re.compile('<tr>.*?</tr>', re.S).findall(data)
        #logger.info("3")
        scrapertools.printMatches(matches)
        #logger.info("4")
        if len(matches)==0:
            logger.info("no encuentra cabecera 2")

        for match in matches:
            #logger.info(match)
            #<tr> <td class="episode-server"> <a href="/s/ngo/2/0/0/4/967" title="Reproducir No estamos solos 2x1" target="_blank"><img src="http://s.staticyonkis.com/img/veronline.png" height="22" width="22"> Reproducir</a> </td> <td class="episode-server-img"><a href="/s/ngo/2/0/0/4/967" title="Reproducir No estamos solos 2x1" target="_blank"><span class="server megavideo"></span></a></td> <td class="episode-lang"><span class="flags esp" title="Español">esp</span></td> <td class="center"><span class="flags no_sub" title="Sin subtítulo o desconocido">no</span></td> <td> <span class="episode-quality-icon" title="Calidad del episodio"> <i class="sprite quality5"></i> </span> </td> <td class="episode-notes"><span class="icon-info"></span> <div class="tip hidden"> <h3>Información vídeo</h3> <div class="arrow-tip-right-dark sprite"></div> <ul> <li>Calidad: 6, Duración: 85.8 min, Peso: 405.79 MB, Resolución: 640x368</li> </ul> </div> </td> <td class="episode-uploader">lksomg</td> <td class="center"><a href="#" class="errorlink" data-id="2004967"><img src="http://s.staticyonkis.com/img/icons/bug.png" alt="" /></a></td> </tr>
            patron = '<a href="/s/ngo/([^"]+)".*?<span class="server ([^"]+)".*?title="[^"]+">([^<]+)</span>.*?"flags ([^_]+)_sub".*?class="sprite quality([^"]+)"'
            datos = re.compile(patron, re.S).findall(match)
            for info in datos:  
                id = info[0]
                servidor = info[1]
                Nro = Nro + 1
                fmt = info[4]      
                audio = "Audio:" + info[2]
                subs = "Subs:" + info[3]
                url = urlparse.urljoin(item.url,"/s/y/"+id.replace("/",""))
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
        logger.info("------------------------------------------------------------")
        #logger.info(data)
        logger.info("------------------------------------------------------------")
        videos = servertools.findvideos(data) 
        logger.info(str(videos))
        logger.info("------------------------------------------------------------")
        if(len(videos)>0): 
            url = videos[0][1]
            server=videos[0][2]                   
            itemlist.append( Item(channel=CHANNELNAME, action="play" , title=item.title , url=url, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
    logger.info("len(itemlist)=%s" % len(itemlist))
    return itemlist

# Pone todas las series del listado alfabético juntas, para no tener que ir entrando una por una
def completo(item):
    logger.info("[seriesyonkis.py] completo()")
    itemlist = []

    # Carga el menú "Alfabético" de series
    item = Item(channel=CHANNELNAME, action="listalfabetico")
    items_letras = listalfabetico(item)
    
    # Carga las series de cada letra
    for item_letra in items_letras:
        items_programas = series(item_letra)

        ultimo_item = items_programas[ len(items_programas)-1 ]
        
        if ultimo_item.action!="series":
            itemlist.extend( items_programas )
        else:
            # Si hay un enlace "Página siguiente"
            while ultimo_item.action=="series":
                
                # Lo quita
                pagina_siguiente_item = items_programas.pop()
                
                # Añade el resto a la lista
                itemlist.extend( items_programas )
                
                # Carga la sigiuente página
                items_programas = series(pagina_siguiente_item)

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
