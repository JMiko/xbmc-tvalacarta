# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para buenaisla
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "buenaisla"
__category__ = "A"
__type__ = "generic"
__title__ = "Buena Isla"
__language__ = "ES"
__creationdate__ = "20110509"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[buenaisla.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades", action="novedades", url="http://www.buenaisla.com/anime-online"))
    itemlist.append( Item(channel=__channel__, title="Listado Completo de Animes y Ovas", action="listacompleta", url="http://www.buenaisla.com/series-anime"))
    itemlist.append( Item(channel=__channel__, title="Listado por Géneros", action="cat", url="http://www.buenaisla.com/anime-online"))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item(channel=__channel__, title="Listado de Peliculas y ovas Hentai en Español", action="hentai", url="http://www.buenaisla.com/peliculas-hentai"))
    itemlist.append( Item(channel=__channel__, title="Últimas Series Agregadas" , action="ultimas", url="http://www.buenaisla.com/anime-online"))
    itemlist.append( Item(channel=__channel__, title="En emisión" , action="listacompleta", url="http://www.buenaisla.com/anime-online"))
    itemlist.append( Item(channel=__channel__, title="Buscar" , action="search") )

    return itemlist

def novedades(item):
    logger.info("[buenaisla.py] novedades")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patronvideos  = '<td width="50%"(.*?)</td>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for elemento in matches:
        patronvideos = '<img src="([^"]+)".*?<a.*?href="(.*?)">(.*?)</a>'
        matches2 = re.compile(patronvideos,re.DOTALL).findall(elemento)

        for match in matches2:
            scrapedurl = urlparse.urljoin("http://www.buenaisla.com/",match[1])
            scrapedtitle = match[2]
            scrapedthumbnail = urlparse.urljoin("http://www.buenaisla.com/",match[0])
            scrapedplot = ""
            logger.info(scrapedtitle)

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def videos(item):

    logger.info("[buenaisla.py] videos")
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    patron = '(modules.php\?name=Anime-Online&func=JokeView&jokeid=.*?&amp;Es=\d)'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for match in matches:
        url= urlparse.urljoin('http://www.buenaisla.com/',match)
        url = url.replace('&amp;','&')
        data2= scrapertools.cachePage(url)
        data = data + data2
            
    title = item.title
    extra = item.extra
    contador = 0
    scrapedthumbnail = item.thumbnail
    listavideos = servertools.findvideos(data)

    itemlist = []
    for video in listavideos:
        invalid = video[1]
        invalid = invalid[0:8]
        if invalid!= "FN3WE43K" and invalid!="9CC3F8&e":
            if extra=="hentai":
                contador=contador+1
                scrapedtitle = title+" Parte "+str(contador)+" "+str(video[0])
            else:    
                scrapedtitle = title+video[0]
            scrapedtitle = scrapedtitle.replace("/"," ")
            videourl = video[1]
            server = video[2]
            if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+videourl+"], thumbnail=["+scrapedthumbnail+"]")

            # Añade al listado de XBMC
            itemlist.append( Item(channel=__channel__, action="play", title=scrapedtitle, fulltitle=item.fulltitle , url=videourl , thumbnail=scrapedthumbnail , server=server , folder=False) )

    return itemlist

def cat(item):
    logger.info("[buenaisla.py] categorias")
    itemlist = []

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    '''
    <td class="bordesTt">G&eacute;neros</td>    
    </tr>
    <tr>
    <td><table width="100%" border="0" cellspacing="0" cellpadding="5">
    <tr>
    <td width="20%"><a class="h2_2" href="genero-accion">Accion</a></td>
    <td width="20%"><a class="h2_2" href="genero-aventura">Aventura</a></td>
    <td width="20%"><a class="h2_2" href="genero-ciencia-ficcion">Ciencia Ficcion </a></td>
    <td width="20%"><a class="h2_2" href="genero-comedia">Comedia</a></td>
    <td width="20%"><a class="h2_2" href="genero-drama">Drama</a></td>
    </tr>
    <tr>
    <td><a class="h2_2" href="genero-ecchi">Ecchi</a></td>
    <td><a class="h2_2" href="genero-escolares">Escolares</a></td>
    <td><a class="h2_2" href="genero-horror">Horror</a></td>    
    <td><a class="h2_2" href="genero-misterio">Misterio</a></td>
    <td><a class="h2_2" href="genero-harem">Harem</a></td>
    </tr>
    <tr>
    <td><a class="h2_2" href="genero-romance">Romance</a></td>
    <td><a class="h2_2" href="genero-seinen">Seinen</a></td>
    <td><a class="h2_2" href="genero-shojo">Shojo</a></td>
    
    <td><a class="h2_2" href="genero-shonen">Shonen</a></td>
    <td><a class="h2_2" href="genero-yuri">Yuri</a></td>
    </tr>
    </table>
    '''
    patron = '<td class="bordesTt">G&eacute;neros(.*?)</table>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    data = matches[0]
    patron = '<a class="h2_2" href="([^"]+)">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for match in matches:
        scrapedurl = urlparse.urljoin("http://www.buenaisla.com",match[0])
        scrapedtitle = match[1]
        #scrapedtitle = scrapedtitle.replace("-"," ")
        scrapedthumbnail = ""
        scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="listaseries", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    itemlist = sorted(itemlist, key=lambda Item: Item.title)    
    return itemlist
    
def listaseries(item):
    logger.info("[buenaisla.py] listaseries")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    patronvideos  = '<td width="33%"(.*?)</h2>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for elemento in matches:
        patronvideos = '<a.*?href="([^"]+)">.*?<img src="([^<]+)" alt="([^"]+)"'
        matches2 = re.compile(patronvideos,re.DOTALL).findall(elemento)

        for match in matches2:
            scrapedurl = urlparse.urljoin("http://www.buenaisla.com/",match[0])
            scrapedtitle = match[2].replace("/"," ")
            scrapedthumbnail = urlparse.urljoin("http://www.buenaisla.com/",match[1])
            scrapedplot = ""
            logger.info(scrapedtitle)

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="listacapitulos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

def ultimas(item):
    logger.info("[buenaisla.py] ultimas")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas
    '''
    <td width="33%"  align="center" valign="top">
    <a class="h2_5" href="ver-anime-kamisama-dolls-castellano-784">
    <div>
    <img src="images/series/784.png" alt="Kamisama Dolls" class="img_capitulo" />    
    </div></a>
    <br /> <h2><a class="h2_5" href="ver-anime-kamisama-dolls-castellano-784">Kamisama Dolls</a></h2>
    '''
    patronvideos  = '<td width="33%"(.*?)</h2>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for elemento in matches:
        patronvideos = '<a.*?href="([^"]+)">.*?<img src="([^<]+)" alt="([^"]+)"'
        matches2 = re.compile(patronvideos,re.DOTALL).findall(elemento)

        for match in matches2:
            scrapedurl = urlparse.urljoin("http://www.buenaisla.com/",match[0])
            scrapedtitle = match[2].replace("/"," ")
            scrapedthumbnail = urlparse.urljoin("http://www.buenaisla.com/",match[1])
            scrapedplot = ""
            logger.info(scrapedtitle)

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="listacapitulos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist
    
def listacapitulos(item):
    logger.info("[buenaisla.py] listacapitulos")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    
    # Extrae el thumbnail y el argumento
    patronvideos  = '<img class="img_capitulo" alt="[^"]*" src="([^"]+)" />'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        imagen = "http://www.buenaisla.com/"+matches[0]
    else:
        imagen = item.thumbnail
    patronvideos  = '(<div id="comentariocompleto" align="justify" style="display:none">.*?)</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        sinopsis = scrapertools.htmlclean(matches[0])

    # Extrae las entradas
    '''
    <p class="accContent" >
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-1-21821">Getsumen To Heiki Mina capitulo 1 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-2-21822">Getsumen To Heiki Mina capitulo 2 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-3-21824">Getsumen To Heiki Mina capitulo 3 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-4-21825">Getsumen To Heiki Mina capitulo 4 </a>    
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-5-21826">Getsumen To Heiki Mina capitulo 5 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-6-21827">Getsumen To Heiki Mina capitulo 6 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-7-21828">Getsumen To Heiki Mina capitulo 7 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-8-21829">Getsumen To Heiki Mina capitulo 8 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-9-21830">Getsumen To Heiki Mina capitulo 9 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-10-21831">Getsumen To Heiki Mina capitulo 10 </a>
    <a class="h2_2" href="online-capitulo-anime-espanol-getsumen-to-heiki-mina-11-21832">Getsumen To Heiki Mina capitulo 11 </a>
    </p>
    '''
    patronvideos  = '<p class="accContent"(.*?)</p>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    itemlist = []
    for elemento in matches:
        patronvideos = '<a.*?href="([^"]+)">([^<]+)</a>'
        matches2 = re.compile(patronvideos,re.DOTALL).findall(elemento)

        for match in matches2:
            scrapedurl = urlparse.urljoin("http://www.buenaisla.com/",match[0])
            scrapedtitle = match[1].replace("/"," ")
            logger.info(scrapedtitle)

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle, fulltitle=item.fulltitle , url=scrapedurl , thumbnail=imagen , plot=sinopsis , folder=True) )
            
    # Extrae la marca de siguiente página
    patronvideos = 'Chistes Encontrados(.*?)<b>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    for elemento in matches:
        patronvideos = '[^\d](.*?) paginas.*?</font>.*?<a href=(.*?)>'
        matches2 = re.compile(patronvideos,re.DOTALL).findall(elemento)
        if len(matches2)>0:
            scrapedurl = "http://www.buenaisla.com/" + matches2[0][1][1:]
            scrapedurl = scrapedurl[0:-1]
            paginas= matches2[0][0]
            pagina= scrapedurl[-2:]
            pagina = pagina.replace('=','')
            scrapedtitle = "Página " + pagina + " de "+ paginas[1:]
            if pagina=="1":break
            itemlist.append( Item( channel=__channel__ , title=scrapedtitle, fulltitle=scrapedtitle , action="listacapitulos" , url=scrapedurl , thumbnail="", plot="" , folder=True ) )

    return itemlist
    
def listacompleta(item):
    logger.info("[buenaisla.py] lista")

    # Descarga la página
    data = scrapertools.cachePage(item.url)
    url = item.url

    # Extrae las entradas
    patronvideos  = '<li>[^<]+'
    patronvideos += '<a.+?href="([\D]+)([\d]+)">[^<]+'
    patronvideos += '.*?/>(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    itemlist = []
    for match in matches:
        scrapedurl = urlparse.urljoin(item.url,(match[0]+match[1]))
        scrapedtitle = match[2].strip()
        scrapedthumbnail = urlparse.urljoin("http://www.buenaisla.com/images/series/",(match[1]+".png"))
        scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="listacapitulos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    if url=="http://www.buenaisla.com/anime-online": itemlist = sorted(itemlist, key=lambda Item: Item.title) 
    return itemlist

def hentai(item):
    logger.info("[buenaisla.py] hentai")

    siguiente = True
    itemlist = []
    url = item.url
    while siguiente==True:
        # Descarga la página
        data = scrapertools.cachePage(url)

        # Extrae las entradas <h2><a class="h2_4" href="pelicula-bakunyuu-oyako-1063" style="display:block; padding-bottom:5px; font-weight:bold; overflow:hidden">Bakunyuu Oyako</a></h2>
        patronvideos  = '<h2><a.+?href="([^"]+)" .*?>([^<]+)</a>'
        patronvideos  += '.*? url\S([^)]+)'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)
        
        for match in matches:
            scrapedurl = urlparse.urljoin(url,match[0])
            scrapedtitle = match[1].strip()
            scrapedthumbnail = urlparse.urljoin(url,match[2])
            scrapedplot = ""
            logger.info(scrapedtitle)

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="videos", title=scrapedtitle.title() , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra="hentai" , folder=True) )
        # Revisa si es ultima pagina <a href="peliculas-hentai-2">siguiente</a>
        patronvideos = '<a href="([^"]+)">siguiente</a>'
        encuentra = re.compile(patronvideos,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(encuentra)
        if len(encuentra)>0:
            url = ("http://www.buenaisla.com/"+encuentra[0])

        else:
            siguiente = False
            
    itemlist = sorted(itemlist, key=lambda Item: Item.title) 
    return itemlist    
    
def search(item,texto, categoria="*"):
    logger.info("[buenaisla.py] search")
    itemlist = []
    if categoria not in ("*", "A"): return itemlist
    
    # Descarga la página con todas las series
    url = "http://www.buenaisla.com/series-anime"
    data = scrapertools.cachePage(url)

    # Extrae las entradas de todas series
    patronvideos  = '<li>[^<]+'
    patronvideos += '<a.+?href="([\D]+)([\d]+)">[^<]+'
    patronvideos += '.*?/>(.*?)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        scrapedtitle = match[2].strip()

        # Realiza la busqueda
        if scrapedtitle.lower()==texto.lower() or texto.lower() in scrapedtitle.lower():
            logger.info(scrapedtitle)
            scrapedurl = urlparse.urljoin(url,(match[0]+match[1]))
            scrapedthumbnail = urlparse.urljoin("http://www.buenaisla.com/images/series/",(match[1]+".png"))
            scrapedplot = ""

            # Añade al listado
            itemlist.append( Item(channel=__channel__, action="listacapitulos", title=scrapedtitle, fulltitle=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )

    return itemlist

