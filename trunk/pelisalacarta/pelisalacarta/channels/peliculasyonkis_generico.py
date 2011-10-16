# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasyonkis
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Adaptado por Boludiko basado en el canal seriesyonkis V7 Por Truenon y Jesus
# v8
#------------------------------------------------------------
import urlparse,urllib2,urllib,re

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

CHANNELNAME = "peliculasyonkis_generico"
DEBUG = True

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasyonkis_generico.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="lastepisodes"      , title="Utimas Peliculas" , url="http://www.peliculasyonkis.com/ultimas-peliculas"))
    itemlist.append( Item(channel=CHANNELNAME, action="listalfabetico"    , title="Listado alfabetico", url="http://www.peliculasyonkis.com/lista-de-peliculas"))
    itemlist.append( Item ( channel=CHANNELNAME , action="listcategorias" , title="Listado por Categorias",url="http://www.peliculasyonkis.com/") )
    itemlist.append( Item(channel=CHANNELNAME, action="mostviewed"    , title="Peliculas mas vistas", url="http://www.peliculasyonkis.com/peliculas-mas-vistas"))
    itemlist.append( Item(channel=CHANNELNAME, action="search"    , title="Buscar", url="http://www.peliculasyonkis.com/buscar/pelicula"))

    return itemlist

def listcategorias(item):
    logger.info("[peliculasyonkis_generico.py] listcategorias")
    itemlist=[]
    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    #logger.info(data)
    
    # Extrae las entradas (carpetas)
    patronvideos  = '<li><a href="(/genero/[^"]+)" title="([^"]+)".*?</li>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for match in matches:
        try:
           scrapedtitle = unicode( match[1], "utf-8" ).encode("iso-8859-1")
        except:
           scrapedtitle = match[1]
        scrapedurl = "http://www.peliculasyonkis.com"+match[0]
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item ( channel=CHANNELNAME , action="peliculascat" , title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot ) )

    return itemlist
   
def peliculascat(item):
    logger.info("[peliculasyonkis_generico.py] series")
    itemlist = []

    data = scrapertools.cachePage(item.url)
   
    #Paginador
    matches = re.compile('<div class="paginator">.*?<a href="([^"]+)">&gt;</a>.*?</div>', re.S).findall(data)
    if len(matches)>0:
        paginador = Item(channel=CHANNELNAME, action="peliculascat" , title="!Pagina siguiente" , url=urlparse.urljoin(item.url,matches[0]), thumbnail=item.thumbnail, plot="", extra = "" , show=item.show)
    else:
        paginador = None
    
    if paginador is not None:
        itemlist.append( paginador )

    matches = re.compile('<li class=.*?title="([^"]+)" href="([^"]+)".*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)

    for match in matches:
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=match[0] , fulltitle=match[0], url=urlparse.urljoin(item.url,match[1]), thumbnail="", plot="", extra = "" , show=match[1] ))

    if paginador is not None:
        itemlist.append( paginador )

    return itemlist
   
def search(item,texto):
    logger.info("[peliculasyonkis_generico.py] search")
    itemlist = []

    if item.url=="":
        item.url = "http://www.peliculasyonkis.com/buscar/pelicula"
    url = "http://www.peliculasyonkis.com/buscar/pelicula" # write ur URL here
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

        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def lastepisodes(item):
    logger.info("[peliculasyonkis_generico.py] lastepisodes")

    data = scrapertools.cache_page(item.url)
  
    matches = re.compile('<li class="thumb-episode"> <a href="([^"]+)".*?src="([^"]+)".*?title="([^"]+)".*?</li>', re.S).findall(data)
    #scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:               
        scrapedtitle = match[2] 
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = urlparse.urljoin(item.url,match[1])
        scrapedplot = ""

        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist  

def mostviewed(item):
    logger.info("[peliculasyonkis_generico.py] mostviewed")
    data = scrapertools.cachePage(item.url)

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
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle))

    return itemlist

def peliculas(item):
    logger.info("[peliculasyonkis_generico.py] series")
    itemlist = []

    data = scrapertools.cachePage(item.url)
   
    #Paginador
    matches = re.compile('<div class="paginator">.*?<a href="([^"]+)">&gt;</a>.*?</div>', re.S).findall(data)
    if len(matches)>0:
        paginador = Item(channel=CHANNELNAME, action="peliculas" , title="!Pagina siguiente" , url=urlparse.urljoin(item.url,matches[0]), thumbnail=item.thumbnail, plot="", extra = "" , show=item.show)
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
        itemlist.append( Item(channel=CHANNELNAME, action="findvideos" , title=match[1] , fulltitle=match[1], url=urlparse.urljoin(item.url,match[0]), thumbnail="", plot="", extra = "" , show=match[1] ))

    if paginador is not None:
        itemlist.append( paginador )

    return itemlist


def findvideos(item):
    logger.info("[peliculasyonkis_generico.py] findvideos")
    itemlist = []

    try:
        Nro = 0
        fmt=id=""
        
        data = scrapertools.cache_page(item.url)    
        
        #Solo queremos los links de ONLINE
        #matches = re.compile('<h2 class="header-subtitle veronline">.*?<h2 class="header-subtitle descargadirecta">', re.S).findall(data)
        #ONLINE + DESCARGA <h2 class="header-subtitle veronline">Ver Online</h2><h2 class="header-subtitle descargadirecta">Descarga directa</h2> 
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
            #<tr> <td class="episode-server"> <a href="/s/ngo/1/1/8/7/869" title="Reproducir Colombiana (2011) " target="_blank"><img src="http://s.staticyonkis.com/img/veronline.png" height="22" width="22">Reproducir</a> </td> <td class="episode-server-img"><a href="/s/ngo/1/1/8/7/869" title="Reproducir Colombiana (2011) " target="_blank"><span class="server megavideo"></span></a></td> <td class="episode-lang"><span class="flags esp" title="Espa�ol">esp</span></td> <td class="center"><span class="flags -_sub" title="Sin subt�tulo o desconocido">-</span></td> <td> <span class="episode-quality-icon" title="Calidad de la pel�cula"> <i class="sprite quality5"></i> </span> </td> <td class="episode-notes"><span class="icon-info"></span> <div class="tip hidden"> <h3>Informaci�n v�deo</h3> <div class="arrow-tip-right-dark sprite"></div> <ul> <li>No hay datos</li> </ul> </div> </td> <td class="center"><span title="TS-Screener (TS, TS-Screener o Screener)">TS-Scr</span></td> <td class="episode-uploader">Carioca</td> <td class="center"><a href="#" class="errorlink" data-id="1187869" ><img src="http://s.staticyonkis.com/img/icons/bug.png" alt="" /></a></td> </tr>
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
                itemlist.append( Item(channel=CHANNELNAME, action="play" , title=scraptedtitle , fulltitle=item.fulltitle, url=url, thumbnail=item.thumbnail, plot=item.plot, folder=False))
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )

    return itemlist

def play(item):
    logger.info("[peliculasyonkis_generico.py] play")
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
        location = scrapertools.getLocationHeaderFromResponse(item.url)
        if "fileserve.com" in location:
            itemlist.append( Item(channel=CHANNELNAME, action="play" , title=item.title , fulltitle=item.fulltitle, url=location, thumbnail=item.thumbnail, plot=item.plot, server="fileserve", folder=False))
        else:
            data = scrapertools.cache_page(item.url)
            videos = servertools.findvideos(data) 
            if(len(videos)>0): 
                url = videos[0][1]
                server=videos[0][2]                   
                itemlist.append( Item(channel=CHANNELNAME, action="play" , title=item.title , fulltitle=item.fulltitle, url=url, thumbnail=item.thumbnail, plot=item.plot, server=server, folder=False))
            else:
                patron='<ul class="form-login">(.*?)</ul'
                matches = re.compile(patron, re.S).findall(data)
                if(len(matches)>0):
                    data = matches[0]
                    #buscamos la public key
                    patron='src="http://www.google.com/recaptcha/api/noscript\?k=([^"]+)"'
                    pkeys = re.compile(patron, re.S).findall(data)
                    if(len(pkeys)>0):
                        pkey=pkeys[0]
                        #buscamos el id de challenge
                        data = scrapertools.cache_page("http://www.google.com/recaptcha/api/challenge?k="+pkey)
                        patron="challenge.*?'([^']+)'"
                        challenges = re.compile(patron, re.S).findall(data)
                        if(len(challenges)>0):
                            challenge = challenges[0]
                            image = "http://www.google.com/recaptcha/api/image?c="+challenge
                            
                            #CAPTCHA
                            exec "import pelisalacarta.captcha as plugin"
                            tbd = plugin.Keyboard("","",image)
                            tbd.doModal()
                            confirmed = tbd.isConfirmed()
                            if (confirmed):
                                tecleado = tbd.getText()
                                sendcaptcha(item.url,challenge,tecleado)
                            del tbd 
                            #tbd ya no existe
                            if(confirmed and tecleado != ""):
                                itemlist = play(item)
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
    
    return itemlist

def sendcaptcha(url,challenge,text):
    values = {'recaptcha_challenge_field' : challenge,
          'recaptcha_response_field' : text}
    form_data = urllib.urlencode(values)
    request = urllib2.Request(url,form_data)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    response = urllib2.urlopen(request)
    html = response.read()
    response.close()
    return html

def listalfabetico(item):
    logger.info("[peliculasyonkis_generico.py] listalfabetico")
       
    itemlist = []
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="0-9", url="http://www.peliculasyonkis.com/lista-de-peliculas/0-9"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="A"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/A"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="B"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/B"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="C"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/C"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="D"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/D"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="E"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/E"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="F"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/F"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="G"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/G"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="H"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/H"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="I"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/I"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="J"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/J"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="K"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/K"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="L"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/L"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="M"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/M"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="N"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/N"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="O"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/O"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="P"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/P"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="Q"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/Q"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="R"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/R"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="S"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/S"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="T"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/T"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="U"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/U"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="V"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/V"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="W"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/W"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="X"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/X"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="Y"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/Y"))
    itemlist.append( Item(channel=CHANNELNAME, action="peliculas" , title="Z"  , url="http://www.peliculasyonkis.com/lista-de-peliculas/Z"))

    return itemlist
