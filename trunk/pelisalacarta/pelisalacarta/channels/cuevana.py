# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cuevana
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "cuevana"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[cuevana.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Películas"  , action="peliculas", url="http://www.cuevana.tv/peliculas/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Series"     , action="series",    url="http://www.cuevana.tv/series/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Buscar"     , action="search_options") )
    
    return itemlist

def peliculas(item):
    logger.info("[cuevana.py] peliculas")
    itemlist = []
     
    itemlist.append( Item(channel=CHANNELNAME, title="Próximas"  , action="novedades", url="http://www.cuevana.tv/peliculas/proximas/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Novedades"  , action="novedades", url="http://www.cuevana.tv/peliculas/?orderby=ano&reverse=true"))
    itemlist.append( Item(channel=CHANNELNAME, title="Más Populares"  , action="novedades", url="http://www.cuevana.tv/peliculas/populares/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Mejor Puntuadas"  , action="novedades", url="http://www.cuevana.tv/peliculas/mejorpuntuadas/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Por Género"     , action="porGenero",    url="http://www.cuevana.tv/peliculas/genero/"))
    itemlist.append( Item(channel=CHANNELNAME, title="Listado Alfabético"     , action="listadoAlfabetico",    url="http://www.cuevana.tv/peliculas/lista/"))	

    return itemlist

def porGenero(item):
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Acción",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=5"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Animación",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=7"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Aventura",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=14"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Bélica",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=19"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Ciencia Ficción",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=6"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Cine Negro",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=23"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=2"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Dramática",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=27"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Musical",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=15"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Negra",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=26"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Romántica",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=16"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Comedia Stand Up",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=24"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Crimen",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=18"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Deporte",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=20"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Documental",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=10"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Dogma",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=22"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Drama",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=1"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Fantasía",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=13"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Humor",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=12"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Infantil",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=8"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Intriga",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=25"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Musical",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=11"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Romance",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=9"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Suspenso",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=3"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Terror",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=4"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Thriller",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=17"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Western",url="http://www.cuevana.tv/peliculas/genero/a=genero&genero=21"))

    return itemlist	

def listadoAlfabetico(item):
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="0-9",url="http://www.cuevana.tv/peliculas/lista/letra=num"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="A",url="http://www.cuevana.tv/peliculas/lista/letra=a"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="B",url="http://www.cuevana.tv/peliculas/lista/letra=b"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="C",url="http://www.cuevana.tv/peliculas/lista/letra=c"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="D",url="http://www.cuevana.tv/peliculas/lista/letra=d"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="E",url="http://www.cuevana.tv/peliculas/lista/letra=e"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="F",url="http://www.cuevana.tv/peliculas/lista/letra=f"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="G",url="http://www.cuevana.tv/peliculas/lista/letra=g"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="H",url="http://www.cuevana.tv/peliculas/lista/letra=h"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="I",url="http://www.cuevana.tv/peliculas/lista/letra=i"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="J",url="http://www.cuevana.tv/peliculas/lista/letra=j"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="K",url="http://www.cuevana.tv/peliculas/lista/letra=k"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="L",url="http://www.cuevana.tv/peliculas/lista/letra=l"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="M",url="http://www.cuevana.tv/peliculas/lista/letra=m"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="N",url="http://www.cuevana.tv/peliculas/lista/letra=n"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="O",url="http://www.cuevana.tv/peliculas/lista/letra=o"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="P",url="http://www.cuevana.tv/peliculas/lista/letra=p"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Q",url="http://www.cuevana.tv/peliculas/lista/letra=q"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="R",url="http://www.cuevana.tv/peliculas/lista/letra=r"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="S",url="http://www.cuevana.tv/peliculas/lista/letra=s"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="T",url="http://www.cuevana.tv/peliculas/lista/letra=t"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="U",url="http://www.cuevana.tv/peliculas/lista/letra=u"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="V",url="http://www.cuevana.tv/peliculas/lista/letra=v"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="W",url="http://www.cuevana.tv/peliculas/lista/letra=w"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="X",url="http://www.cuevana.tv/peliculas/lista/letra=x"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Y",url="http://www.cuevana.tv/peliculas/lista/letra=y"))
    itemlist.append( Item(channel=CHANNELNAME , action="novedades" , title="Z",url="http://www.cuevana.tv/peliculas/lista/letra=z"))

    return itemlist

def novedades(item):
    if (DEBUG): logger.info("[cuevana.py] novedades login")
    try:
        post = urllib.urlencode({'usuario' : 'pelisalacarta','password' : 'pelisalacarta','recordarme':'si','ingresar':'true'})
        data = scrapertools.cache_page("http://www.cuevana.tv/login_get.php",post=post)
    except:
        pass
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    '''
    <tr class='row2'>
    <td valign='top'><a href='/peliculas/2933/alpha-and-omega/'><img src='/box/2933.jpg' border='0' height='90' /></a></td>
    <td valign='top'><div class='tit'><a href='/peliculas/2933/alpha-and-omega/'>Alpha and Omega</a></div>
    <div class='font11'>Dos pequeÃ±os carrochos de lobo se ven obligados a convivir por determinadas circunstancias.
    <div class='reparto'><b>Reparto:</b> <a href='/buscar/?q=AnimaciÃ³n&cat=actor'>AnimaciÃ³n</a></div>
    </div></td>
    '''
    patronvideos  = "<tr class='row[^<]+"
    patronvideos += "<td valign='top'><a href='([^']+)'><img src='([^']+)'[^>]+></a></td>[^<]+"
    patronvideos += "<td valign='top'><div class='tit'><a[^>]+>([^<]+)</a></div>[^<]+"
    patronvideos += "<div class='font11'>([^<]+)<"

    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[2]
        scrapedplot = match[3]
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )

    # Extrae el paginador
    patronvideos  = "<a class='next' href='([^']+)' title='Siguiente'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="novedades", title="Pagina siguiente" , url=scrapedurl) )

    return itemlist

def series(item):
    logger.info("[cuevana.py] series")
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas
    patron  = 'serieslist.push\(\{id\:([0-9]+),nombre\:"([^"]+)"\}\);'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = ""
        code = match[0]
        scrapedurl = "http://www.cuevana.tv/list_search_id.php?serie="+code
        scrapedthumbnail = "http://www.cuevana.tv/box/"+code+".jpg"
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+scrapedtitle)

        itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle, fulltitle=scrapedtitle , extra=code, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=scrapedtitle) )

    return itemlist

def temporadas(item,data):
    logger.info("[cuevana.py] temporadas")

    ## <-- Obtengo plot y thumbnail
    code = item.extra
    nombre = scrapertools.slugify(item.title)
    data2 = scrapertools.cache_page("http://www.cuevana.tv/series/%s/%s" % (code, nombre))
    patron  = '<h4>Sinopsis</h4>\s*?<p>([^<]+?)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data2)
    if len(matches) > 0: 
        scrapedplot = matches[0]
    else: scrapedplot = item.plot
    scrapedthumbnail = "http://www.cuevana.tv/box/"+code+".jpg" 
    ## <--
    
    # Extrae las entradas
    patron  = '<li onclick=\'listSeries\(2,"([^"]+)"\)\'>([^<]+)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        temporada = scrapedtitle.replace("Temporada ","")
        code = match[0]
        scrapedurl = "http://www.cuevana.tv/list_search_id.php?temporada="+code
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], temporada=["+temporada+"] show="+item.show)

        itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=temporada , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show=item.show , extra=item.extra + "|" + temporada) )

    return itemlist

def episodios(item):
    logger.info("[cuevana.py] episodios")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    
    # Extrae las temporadas
    temporadas_itemlist = temporadas(item,data)
    
    for temporada_item in temporadas_itemlist:
        data = scrapertools.cache_page(temporada_item.url)

        # Extrae las entradas
        #<li onclick='listSeries(3,"5099")'><span class='nume'>1</span> Truth Be Told</li>
        patron  = '<li onclick=\'listSeries\(3,"([^"]+)"\)\'><span class=\'nume\'>([^<]+)</span>([^<]+)</li>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        
        for match in matches:
            code = match[0]
            episodio = match[1]
            if len(episodio)==1:
                episodio = "0" + episodio
            scrapedtitle = temporada_item.title + "x" + episodio + " "+match[2].strip()
            scrapedplot = temporada_item.plot
            scrapedurl = "http://www.cuevana.tv/list_search_info.php?episodio="+code
            scrapedthumbnail = temporada_item.thumbnail
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"] show="+item.show)
    
            itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle, fulltitle=item.fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , show = item.show) )

    if config.get_platform().startswith("xbmc"):
        itemlist.append( Item(channel=item.channel, title="Añadir estos episodios a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )

    return itemlist

def findvideos(item):
    logger.info("[cuevana.py] findvideos")

    isSerie = True
    code =""
    if (item.url.startswith("http://www.cuevana.tv/list_search_info.php")):
        data = scrapertools.cachePage(item.url)
        #logger.info("data="+data)
        patron = "window.location\='/series/([0-9]+)/"
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            code = matches[0]
        logger.info("code="+code)
        # HD - http://www.cuevana.tv/player/source?id=12043&subs=,ES,EN&onstart=yes&tipo=s&sub_pre=ES&hd=1#
        url = "http://www.cuevana.tv/player/source?id=%s&subs=,ES&onstart=yes&tipo=s&sub_pre=ES" % matches[0]
        isSerie = True
    else:
        # http://www.cuevana.tv/peliculas/2553/la-cienaga/
        logger.info("url1="+item.url)
        if "/peliculas/" in item.url:
            patron = "http://www.cuevana.tv/peliculas/([0-9]+)/"
            isSerie = False
        else: 
            patron = "http://www.cuevana.tv/series/([0-9]+)/"
            isSerie = True
        matches = re.compile(patron,re.DOTALL).findall(item.url)
        if len(matches)>0:
            code = matches[0]
        logger.info("code="+code)
        # HD - http://www.cuevana.tv/player/source?id=12043&subs=,ES,EN&onstart=yes&tipo=s&sub_pre=ES&hd=1#
        url = "http://www.cuevana.tv/player/source?id=%s&subs=,ES&onstart=yes&sub_pre=ES#" % code
    
    logger.info("url2="+url)
    data = scrapertools.cachePage(url)
    #logger.info("data="+data)

    # goSource('ee5533f50eab1ef355661eef3b9b90ec','megaupload')
    patron = "goSource\('([^']+)','megaupload'\)"
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        data = scrapertools.cachePagePost("http://www.cuevana.tv/player/source_get","key=%s&host=megaupload&vars=&id=2933&subs=,ES&tipo=&amp;sub_pre=ES" % matches[0])
    logger.info("data="+data)

    # Subtitulos
    if isSerie:
        suburl = "http://www.cuevana.tv/files/s/sub/"+code+"_ES.srt"
    else:
        suburl = "http://www.cuevana.tv/files/sub/"+code+"_ES.srt"
    logger.info("suburl="+suburl)
    
    # Elimina el archivo subtitulo.srt de alguna reproduccion anterior
    ficherosubtitulo = os.path.join( config.get_data_path(), 'subtitulo.srt' )
    if os.path.exists(ficherosubtitulo):
        try:
          os.remove(ficherosubtitulo)
        except IOError:
          logger.info("Error al eliminar el archivo subtitulo.srt "+ficherosubtitulo)
          raise

    listavideos = servertools.findvideos(data)
    
    itemlist = []
    
    for video in listavideos:
        server = video[2]
        scrapedtitle = item.title + " [" + server + "]"
        scrapedurl = video[1]
        
        itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scrapedtitle, fulltitle=item.fulltitle , url=scrapedurl, thumbnail=item.thumbnail, plot=item.plot, server=server, subtitle=suburl, folder=False))

    return itemlist

def search_options(item):
    logger.info("[cuevana.py] search_options")
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, title="Titulo"   , action="search", url="http://www.cuevana.tv/buscar/?q=%s&cat=Titulo"))
    itemlist.append( Item(channel=CHANNELNAME, title="Episodio" , action="search", url="http://www.cuevana.tv/buscar/?q=%s&cat=Episodio"))
    itemlist.append( Item(channel=CHANNELNAME, title="Actor"    , action="search", url="http://www.cuevana.tv/buscar/?q=%s&cat=Actor"))
    itemlist.append( Item(channel=CHANNELNAME, title="Director" , action="search", url="http://www.cuevana.tv/buscar/?q=%s&cat=Director"))
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto, categoria="*"):
    logger.info("[cuevana.py] search")
    
    try:
        # La URL puede venir vacía, por ejemplo desde el buscador global
        if item.url=="":
            item.url="http://www.cuevana.tv/buscar/?q=%s&cat=Titulo"
    
        # Reemplaza el texto en la cadena de búsqueda
        item.url = item.url % texto

        # Devuelve los resultados
        return listar(item, categoria)
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
    
def listar(item, categoria="*"):
    logger.info("[cuevana.py] listar")

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)

    patronvideos  = "<div class='result'>[^<]+"
    patronvideos += "<div class='right'><div class='tit'><a href='([^']+)'>([^<]+)</a>"
    patronvideos += ".*?<div class='txt'>([^<]+)<div class='reparto'>.*?"
    patronvideos += "<div class='img'>.*?<img src='([^']+)'[^>]+></a>"


    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedtitle = match[1]
        scrapedplot = match[2]
        scrapedurl = urlparse.urljoin("http://www.cuevana.tv/peliculas/",match[0])
        scrapedthumbnail = urlparse.urljoin("http://www.cuevana.tv/peliculas/",match[3])
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        ## <-- Trata diferenciadamente a las series y usa filtro de categoria para búsquedas generales
        if "tv/series/" in scrapedurl and categoria in ("S","*"):
           code = re.compile("/series/([0-9]+)/").findall(scrapedurl)[0]
           scrapedurl = "http://www.cuevana.tv/list_search_id.php?serie="+code
           itemlist.append( Item(channel=CHANNELNAME, action="episodios", title=scrapedtitle, fulltitle=scrapedtitle , extra=code, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )
        elif "tv/peliculas/" in scrapedurl and categoria in ("F","*"):
           itemlist.append( Item(channel=CHANNELNAME, action="findvideos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )

    # Extrae el paginador
    patronvideos  = "<a class='next' href='([^']+)' title='Siguiente'>"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=CHANNELNAME, action="listar", title="Página siguiente" , url=scrapedurl) )

    return itemlist
