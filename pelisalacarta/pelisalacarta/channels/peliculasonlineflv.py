# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para peliculasonlineflv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "peliculasonlineflv"
__category__ = "F,D"
__type__ = "generic"
__title__ = "Peliculas Online FLV"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[peliculasonlineflv.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Novedades",  action="peliculas", url="http://www.peliculasonlineflv.net"))
    itemlist.append( Item(channel=__channel__, title="Por orden alfabético", action="letras", url="http://www.peliculasonlineflv.net"))
    itemlist.append( Item(channel=__channel__, title="Por géneros", action="generos", url="http://www.peliculasonlineflv.net"))
    itemlist.append( Item(channel=__channel__, title="Buscar...", action="search"))
    return itemlist

def search(item,texto):
    logger.info("[peliculasonlineflv.py] search")
    if item.url=="":
        item.url="http://www.peliculasonlineflv.net/buscar/?s="
    
    texto = texto.replace(" ","+")
    item.url = item.url + texto

    try:
        return peliculas(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def letras(item):
    logger.info("[peliculasonlineflv.py] letras")
    itemlist=[]

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'Abecedario\:(.*?)</div>')
    '''
    <select name="genero" id="genbox">
    <option value="">Lista de Generos</option>
    <option value="Action">Action</option><option value="Animation">Animation</option><option value="Adventure">Adventure</option><option value="Biography">Biography</option><option value="Comedy">Comedy</option><option value="Crime">Crime</option><option value="Documentary">Documentary</option><option value="Drama">Drama</option><option value="Family">Family</option><option value="Fantasy">Fantasy</option><option value="Film-Noir">Film-Noir</option><option value="Game-Show">Game-Show</option><option value="History">History</option><option value="Horror">Horror</option><option value="Music">Music</option><option value="Musical">Musical</option><option value="Mystery">Mystery</option><option value="N/A">N/A</option><option value="News">News</option><option value="Reality-TV">Reality-TV</option><option value="Romance">Romance</option><option value="Sci-Fi">Sci-Fi</option><option value="Short">Short</option><option value="Sport">Sport</option><option value="Thriller">Thriller</option><option value="War">War</option><option value="Western">Western</option> </select>
    Abecedario: <a class="jq" href="http://www.peliculasonlineflv.net/letra/a/">A</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/b/">B</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/c/">C</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/d/">D</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/e/">E</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/f/">F</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/g/">G</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/h/">H</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/i/">I</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/j/">J</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/k/">K</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/l/">L</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/m/">M</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/n/">N</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/o/">O</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/p/">P</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/q/">Q</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/r/">R</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/s/">S</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/t/">T</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/u/">U</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/v/">V</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/w/">W</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/x/">X</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/y/">Y</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/z/">Z</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/num/">#</a>
    </div></div>
    '''

    # Patron de las entradas
    patron  = '<a class="jq" href="([^"]+)">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    # Añade las entradas encontradas
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = scrapedurl
        scrapedplot = ""
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def generos(item):
    logger.info("[peliculasonlineflv.py] generos")
    itemlist=[]

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    data = scrapertools.get_match(data,'<option value="">Lista de Generos</option>(.*?)</select>')
    '''
    <select name="genero" id="genbox">
    <option value="">Lista de Generos</option>
    <option value="Action">Action</option><option value="Animation">Animation</option><option value="Adventure">Adventure</option><option value="Biography">Biography</option><option value="Comedy">Comedy</option><option value="Crime">Crime</option><option value="Documentary">Documentary</option><option value="Drama">Drama</option><option value="Family">Family</option><option value="Fantasy">Fantasy</option><option value="Film-Noir">Film-Noir</option><option value="Game-Show">Game-Show</option><option value="History">History</option><option value="Horror">Horror</option><option value="Music">Music</option><option value="Musical">Musical</option><option value="Mystery">Mystery</option><option value="N/A">N/A</option><option value="News">News</option><option value="Reality-TV">Reality-TV</option><option value="Romance">Romance</option><option value="Sci-Fi">Sci-Fi</option><option value="Short">Short</option><option value="Sport">Sport</option><option value="Thriller">Thriller</option><option value="War">War</option><option value="Western">Western</option> </select>
    Abecedario: <a class="jq" href="http://www.peliculasonlineflv.net/letra/a/">A</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/b/">B</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/c/">C</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/d/">D</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/e/">E</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/f/">F</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/g/">G</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/h/">H</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/i/">I</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/j/">J</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/k/">K</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/l/">L</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/m/">M</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/n/">N</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/o/">O</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/p/">P</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/q/">Q</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/r/">R</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/s/">S</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/t/">T</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/u/">U</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/v/">V</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/w/">W</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/x/">X</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/y/">Y</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/z/">Z</a> <a class="jq" href="http://www.peliculasonlineflv.net/letra/num/">#</a>
    </div></div>
    '''

    # Patron de las entradas
    patron  = '<option value="([^"]+)">([^<]+)</option>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    # Añade las entradas encontradas
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle
        url = "http://www.peliculasonlineflv.net/genero/"+scrapedurl+"/"
        scrapedplot = ""
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    return itemlist

def peliculas(item):
    logger.info("[peliculasonlineflv.py] peliculas")
    itemlist=[]

    # Descarga la pagina
    data = scrapertools.cachePage(item.url)
    '''
    <div class="pelibox">
    <div class="pelicont">
    <a href="http://www.peliculasonlineflv.net/pelicula/pequenos-invasores/" class="jq" title="Peque?os Invasores"><img class="port" src="http://2.bp.blogspot.com/_VgjDunqv6LE/TAPJWEn8V6I/AAAAAAAACXs/uEIkLhDYrnA/s320/1.jpg" alt="Peque?os Invasores" /></a>

    <div class="pelibox">
    <div class="pelicont">

    <a href="http://www.peliculasonlineflv.net/pelicula/la-vida-de-flynn/" class="jq" title="La vida de Flynn"><img class="port" src="http://4.bp.blogspot.com/-lBMNTCg5X8I/UbUHQQC8K1I/AAAAAAAAAN0/9nKMv0MVsNg/s320/7.jpg" alt="La vida de Flynn" /></a>
    '''

    # Patron de las entradas
    patron  = '<div class="pelibox"[^<]+'
    patron += '<div class="pelicont"[^<]+'
    patron += '<a href="([^"]+)" class="[^"]+" title="([^"]+)"><img class="[^"]+" src="([^"]+)"'

    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    # Añade las entradas encontradas
    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        title = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        url = scrapedurl
        scrapedplot = ""
        thumbnail = scrapedthumbnail
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    patron = '<span class="actual">[^<]+</span[^<]+<a href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        siguiente_url = urlparse.urljoin(item.url,"/"+matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Página siguiente" , url=siguiente_url , folder=True) )

    return itemlist

def findvideos(item):
    logger.info("[peliculasonlineflv.py] findvideos")
    itemlist=[]

    # Descarga la p?gina
    data = scrapertools.cachePage(item.url)

    from servers import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=__channel__
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "Ver en "+videoitem.server
        videoitem.fulltitle = item.fulltitle

    # Ahora busca patrones manuales
    try:
        vk_code = scrapertools.get_match(data,"vklat\=([a-zA-Z0-9]+)")
        vk_url = scrapertools.get_header_from_response("http://goo.gl/"+vk_code,header_to_get="location")
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en VK (Latino)" , server="vk" , url=vk_url , folder=False ) )
    except:
        logger.info("No encontrado enlace VK")

    try:
        putlocker_code = scrapertools.get_match(data,"plat\=([A-Z0-9]+)")
        putlocker_url = "http://www.putlocker.com/embed/"+putlocker_code
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en Putlocker (Latino)" , server="putlocker" , url=putlocker_url , folder=False ) )
    except:
        logger.info("No encontrado enlace PUTLOCKER")

    try:
        vk_code = scrapertools.get_match(data,"vksub\=([a-zA-Z0-9]+)")
        vk_url = scrapertools.get_header_from_response("http://goo.gl/"+vk_code,header_to_get="location")
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en VK (Subtitulado)" , server="vk" , url=vk_url , folder=False ) )
    except:
        logger.info("No encontrado enlace VK")

    try:
        putlocker_code = scrapertools.get_match(data,"plsub\=([A-Z0-9]+)")
        putlocker_url = "http://www.putlocker.com/embed/"+putlocker_code
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en Putlocker (Subtitulado)" , server="putlocker" , url=putlocker_url , folder=False ) )
    except:
        logger.info("No encontrado enlace PUTLOCKER")

    try:
        vk_code = scrapertools.get_match(data,"vk\=([a-zA-Z0-9]+)")
        vk_url = scrapertools.get_header_from_response("http://goo.gl/"+vk_code,header_to_get="location")
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en VK" , server="vk" , url=vk_url , folder=False ) )
    except:
        logger.info("No encontrado enlace VK")

    try:
        putlocker_code = scrapertools.get_match(data,"put\=([A-Z0-9]+)")
        putlocker_url = "http://www.putlocker.com/embed/"+putlocker_code
        itemlist.append( Item( channel=__channel__ , action="play" , title="Ver en Putlocker" , server="putlocker" , url=putlocker_url , folder=False ) )
    except:
        logger.info("No encontrado enlace PUTLOCKER")

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    mainlist_items = mainlist(Item())
    peliculas_items = peliculas(mainlist_items[0])

    for pelicula_item in peliculas_items:
        mirrors = findvideos( item=pelicula_item )
        if len(mirrors)>0:
            return True

    return False