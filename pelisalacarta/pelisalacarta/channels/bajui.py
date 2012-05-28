# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para bajui
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "bajui"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Bajui"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[bajui.py] getmainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas"                , action="menupeliculas"))
    itemlist.append( Item(channel=__channel__, title="Series"                   , action="menuseries"))
    itemlist.append( Item(channel=__channel__, title="Documentales"             , action="menudocumentales"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                   , action="search") )
    return itemlist

def menupeliculas(item):
    logger.info("[bajui.py] menupeliculas")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Películas - Novedades"        , action="peliculas"   , url="http://www.bajui.com/categoria/2/peliculas"))
    itemlist.append( Item(channel=__channel__, title="Películas - A-Z"              , action="peliculas"   , url="http://www.bajui.com/categoria/2/peliculas/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Películas - DVDRip-VHSRip"    , action="peliculas"   , url="http://www.bajui.com/subcategoria/1/dvdrip-vhsrip/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Películas - HDRip-BDRip"      , action="peliculas"   , url="http://www.bajui.com/subcategoria/2/hdrip-bdrip/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Películas - HD"               , action="peliculas"   , url="http://www.bajui.com/subcategoria/3/hd/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Películas - TS-SCR-CAM"       , action="peliculas"   , url="http://www.bajui.com/subcategoria/5/ts-scr-cam/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Películas - DVDR-FULL"        , action="peliculas"   , url="http://www.bajui.com/subcategoria/6/dvdr-full/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Películas - VOS"              , action="peliculas"   , url="http://www.bajui.com/subcategoria/7/vos/orden:nombre") )
    itemlist.append( Item(channel=__channel__, title="Películas - Latino"           , action="peliculas"   , url="http://www.bajui.com/subcategoria/35/latino/orden:nombre") )
    itemlist.append( Item(channel=__channel__, title="Buscar"                       , action="search"      , url="") )
    return itemlist

def menuseries(item):
    logger.info("[bajui.py] menuseries")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Series - Novedades"           , action="peliculas"        , url="http://www.bajui.com/categoria/3/series"))
    itemlist.append( Item(channel=__channel__, title="Series - A-Z"                 , action="peliculas"        , url="http://www.bajui.com/categoria/3/series/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Series - HD"                  , action="peliculas"        , url="http://www.bajui.com/subcategoria/11/hd/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                       , action="search"            , url="") )
    return itemlist

def menudocumentales(item):
    logger.info("[bajui.py] menudocumentales")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Documentales - Novedades"         , action="peliculas"     , url="http://www.bajui.com/categoria/7/docus-y-tv"))
    itemlist.append( Item(channel=__channel__, title="Documentales - A-Z"               , action="peliculas"     , url="http://www.bajui.com/categoria/7/docus-y-tv/orden:nombre"))
    itemlist.append( Item(channel=__channel__, title="Buscar"                           , action="search"        , url="") )
    return itemlist

# Al llamarse "search" la función, el launcher pide un texto a buscar y lo añade como parámetro
def search(item,texto,categoria=""):
    logger.info("[bajui.py] "+item.url+" search "+texto)
    itemlist = []
    url = item.url
    texto = texto.replace(" ","+")
    logger.info("categoria: "+categoria+" url: "+url)
    try:
        item.url = "http://www.bajui.com/busqueda/%s"
        item.url = item.url % texto
        itemlist.extend(buscar(item))
        return itemlist
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscar(item,paginacion=True):
    logger.info("[bajui.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a href="([^"]+)" style="display:none;" rel="nofollow"><img src="([^"]+)" width="100" height="144" border="0" alt="" /><br/><br/>[^<]+<b>([^<]+)</b></a>[^<]+<a href="([^"]+)">([^#]+)#888"><b>([^<]+)</b>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        if match[5] == 'Peliculas' or match[5] == 'Series':
            scrapedtitle =  match[2]
            # Convierte desde UTF-8 y quita entidades HTML
            #        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
            scrapedtitle = scrapertools.entityunescape(scrapedtitle)
            fulltitle = scrapedtitle
            # procesa el resto
            scrapedplot = ""

            scrapedurl = urlparse.urljoin("http://www.bajui.com/",match[3])
            scrapedthumbnail = urlparse.urljoin("http://www.bajui.com/",match[1])
            if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
            itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    # Extrae el paginador
    #<a href="categoria/2/peliculas/pag:2/orden:nombre" class="pagina pag_sig">Siguiente »</a>
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin("http://www.bajui.com/",matches[0])
        pagitem = Item(channel=__channel__, action="peliculas", title="!Página siguiente" , url=scrapedurl)
        if not paginacion:
            itemlist.extend( peliculas(pagitem) )
        else:
            itemlist.append( pagitem )

    return itemlist

def peliculas(item,paginacion=True):
    logger.info("[bajui.py] peliculas")
    url = item.url
    # Descarga la página
    data = scrapertools.cachePage(url)
    # Extrae las entradas
    patronvideos = '<a href="([^"]+)" style="display:none;" rel="nofollow"><img src="([^"]+)" width="100" height="144" border="0" alt="" /><br/><br/>[^<]+<b>([^<]+)</b></a>[^<]+<a href="([^"]+)">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedtitle =  match[2]
        # Convierte desde UTF-8 y quita entidades HTML
#        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = scrapertools.entityunescape(scrapedtitle)
        fulltitle = scrapedtitle
        # procesa el resto
        scrapedplot = ""

        scrapedurl = urlparse.urljoin("http://www.bajui.com/",match[3])
        scrapedthumbnail = urlparse.urljoin("http://www.bajui.com/",match[1])
        if DEBUG: logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        # Añade al listado de XBMC
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=fulltitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , extra=scrapedtitle , context="4|5") )

    # Extrae el paginador
    #<a href="categoria/2/peliculas/pag:2/orden:nombre" class="pagina pag_sig">Siguiente »</a>
    patronvideos  = '<a href="([^"]+)" class="pagina pag_sig">'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin("http://www.bajui.com/",matches[0])
        pagitem = Item(channel=__channel__, action="peliculas", title="!Página siguiente" , url=scrapedurl)
        if not paginacion:
            itemlist.extend( peliculas(pagitem) )
        else:
            itemlist.append( pagitem )

    return itemlist

def findvideos(item):
    logger.info("[bajui.py] findvideos")
    
    data = scrapertools.cache_page(item.url)
    itemlist = servertools.find_video_items(data=data)
    for videoitem in itemlist:
        videoitem.channel = __channel__
        videoitem.plot = item.plot
        videoitem.thumbnail = item.thumbnail
        videoitem.fulltitle = item.fulltitle
        
        parsed_url = urlparse.urlparse(videoitem.url)
        fichero = parsed_url.path
        partes = fichero.split("/")
        titulo = partes[ len(partes)-1 ]
        videoitem.title = titulo + " - [" + videoitem.server+"]"
        
    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    # mainlist
    mainlist_items = mainlist(Item())
    
    # Comprueba que todas las opciones tengan algo (excepto los buscadores)
    for mainlist_item in mainlist_items:
        if mainlist_item.action!="search":
            exec "itemlist = "+mainlist_item.action+"(mainlist_item)"
            
            for item in itemlist:
                if item.action!="search":
                    exec "itemlist2 ="+item.action+"(item)"
        
                    if len(itemlist2)==0:
                        return False
    
    
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    menupeliculas_items = menupeliculas(mainlist_items[0])
    peliculas_items = peliculas(menupeliculas_items[0])
    bien = False
    for pelicula_item in peliculas_items:
        mirrors = findvideos(item=pelicula_item)
        if len(mirrors)>0:
            bien = True
            break

    return bien
